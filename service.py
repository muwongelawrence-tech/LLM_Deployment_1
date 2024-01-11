import bentoml
import torch
import typing as t

max_new_tokens = 50
stream_interval = 2
context_length = 2048

class StreamRunnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("nvidia.com/gpu", "cpu")
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(self):
        self.tokenizer = bentoml.transformers.load_model("heal-tokenizer")
        self.model = bentoml.transformers.load_model("heal-model")

    @bentoml.Runnable.method()
    async def generate(self, prompt: str) -> t.AsyncGenerator[str, None]:
        input_ids = self.tokenizer(prompt).input_ids
        max_src_len = context_length - max_new_tokens - 1
        input_ids = input_ids[-max_src_len:]
        output_ids = list(input_ids)

        past_key_values = out = token = None

        for i in range(max_new_tokens):
            if i == 0:  # prefill
                out = self.model(torch.as_tensor([input_ids]), use_cache=True, )
                logits = out.logits
                past_key_values = out.past_key_values
            else:  # decoding
                out = self.model(input_ids=torch.as_tensor([[token]]), use_cache=True, past_key_values=past_key_values)
                logits = out.logits
                past_key_values = out.past_key_values

            last_token_logits = logits[0, -1, :]

            probs = torch.softmax(last_token_logits, dim=-1)
            token = int(torch.multinomial(probs, num_samples=1))
            output_ids.append(token)

            decoded_token = self.tokenizer.decode(
                token,
                skip_special_tokens=True,
                spaces_between_special_tokens=False,
                clean_up_tokenization_spaces=True
            )

            # Format and yield the token for SSE
            yield f"event: message\ndata: {decoded_token}\n\n"

        # Indicate the end of the stream
        yield "event: end\n\n"

stream_runner = bentoml.Runner(StreamRunnable)
svc = bentoml.Service("englishtoluganda", runners=[stream_runner])

@svc.api(input=bentoml.io.Text(), output=bentoml.io.Text(content_type='text/event-stream'))
async def generate(prompt: str) -> t.AsyncGenerator[str, None]:
    async for token in stream_runner.generate.async_stream(prompt):
        yield token