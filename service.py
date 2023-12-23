# import bentoml

# summarizer_runner = bentoml.models.get("summarization:latest").to_runner()

# svc = bentoml.Service(
#     name="summarization", runners=[summarizer_runner]
# )

# @svc.api(input=bentoml.io.Text(), output=bentoml.io.Text())
# async def summarize(text: str) -> str:
#     generated = await summarizer_runner.async_run(text, max_length=3000)
#     return generated[0]["summary_text"]
#############################################################################################

# import bentoml
# from transformers import GPT2Model, GPT2Tokenizer

# # Load the pre-trained GPT-2 model and tokenizer
# tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
# model = GPT2Model.from_pretrained('gpt2')

# # Get the latest version of the BentoML service and convert it into a runner
# gpt2_runner = bentoml.models.get("gpt2:latest").to_runner()

# # Create a BentoML service with the specified runner
# svc = bentoml.Service(
#     name="gpt2", runners=[gpt2_runner]
# )

# # Define an API endpoint for the service
# @svc.api(input=bentoml.io.Text(), output=bentoml.io.Text())
# async def generate_text(text: str) -> str:
#     # Tokenize the input text using GPT-2 tokenizer
#     tokens = tokenizer.encode(text, return_tensors='pt')
#     # Run the GPT-2 model with the provided tokens
#     outputs = model(tokens)
#     # Get the generated text from the model output
#     generated_text = outputs.last_hidden_state.mean(dim=1).tolist()
#     return generated_text

#####################################################################################################
from __future__ import annotations
import uuid
from typing import Any, AsyncGenerator, Dict, TypedDict, Union

from bentoml import Service
from bentoml.io import JSON, Text
from openllm import LLM

llm = LLM[Any, Any]("HuggingFaceH4/zephyr-7b-alpha", backend="vllm")


svc = Service("tinyllm", runners=[llm.runner])


class GenerateInput(TypedDict):
    prompt: str
    stream: bool
    sampling_params: Dict[str, Any]


@svc.api(
    route="/v1/generate",
    input=JSON.from_sample(
        GenerateInput(
            prompt="What is time?",
            stream=False,
            sampling_params={"temperature": 0.73, "logprobs": 1},
        )
    ),
    output=Text(content_type="text/event-stream"),
)
async def generate(request: GenerateInput) -> Union[AsyncGenerator[str, None], str]:
    n = request["sampling_params"].pop("n", 1)
    request_id = f"tinyllm-{uuid.uuid4().hex}"
    previous_texts = [[]] * n

    generator = llm.generate_iterator(
        request["prompt"], request_id=request_id, n=n, **request["sampling_params"]
    )

    async def streamer() -> AsyncGenerator[str, None]:
        async for request_output in generator:
            for output in request_output.outputs:
                i = output.index
                previous_texts[i].append(output.text)
                yield output.text

    if request["stream"]:
        return streamer()

    async for _ in streamer():
        pass
    return "".join(previous_texts[0])