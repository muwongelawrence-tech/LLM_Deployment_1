import bentoml
import torch
import asyncio
from bentoml.io import JSON, Text
import typing as t


class StreamRunnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("nvidia.com/gpu", "cpu")
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(self):
        self.tokenizer = bentoml.transformers.load_model("heal-tokenizer")
        self.model = bentoml.transformers.load_model("heal-model")

    @bentoml.Runnable.method()
    async def generate(self, prompt: str, stream: bool) -> t.AsyncGenerator[str, None]:

        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids

        parameters = {}
        parameters['max_length'] = 1012  # Set your desired max_length here
        parameters['min_length'] = 100
        parameters['length_penalty'] = 10.0
        parameters['num_beams'] = 10
        parameters['early_stopping'] = True
        parameters['do_sample'] = True
        parameters['temperature'] = 0.00000000001
        parameters['top_k'] = 10
        parameters['top_p'] = 1.0
        parameters['repetition_penalty'] = 0.5

        
        if stream:
            # GENERATE RESPONSE WITH STREAMING.......
            for token_id in self.model.generate(input_ids, **parameters)[0]:
                # Convert tensor element to Python integer
                token_id = token_id.item()

                # Decode the token
                decoded_token = self.tokenizer.decode(
                    token_id, 
                    skip_special_tokens=True, 
                    spaces_between_special_tokens=False,
                    clean_up_tokenization_spaces=True
                )

                # Format and yield the token for SSE
                yield f"event: message\nTOKEN_ID: {token_id} ->data: {decoded_token}\n\n"
                await asyncio.sleep(0.2)

            # Indicate the end of the stream
            yield "event: end\n\n"
        else:
            # GENERATE RESPONSE WITHOUT STREAMING....
            outputs = self.model.generate(input_ids, **parameters)
            prediction = self.tokenizer.decode(outputs[0], skip_special_tokens=True, spaces_between_special_tokens=False,clean_up_tokenization_spaces=True)
            yield f"{ prediction }"



GenerateInput = dict[str, t.Union[str, bool]]

stream_runner = bentoml.Runner(StreamRunnable)
svc = bentoml.Service("englishtoluganda", runners=[stream_runner])

@svc.api(input=JSON.from_sample(
        GenerateInput(
            prompt="what is the difference of covid and fever?",
            stream=False,
         )
    ), output=bentoml.io.Text(content_type='text/event-stream'))
async def generate(request: GenerateInput) -> t.AsyncGenerator[str, None]:
    async for token in stream_runner.generate.async_stream(request['prompt'], request['stream']):
        yield token