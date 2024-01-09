# import bentoml
# import torch
# from transformers import AutoTokenizer

# translation_runner = bentoml.models.get("text2textgeneration:latest").to_runner()

# svc = bentoml.Service(
#     name="englishtoluganda", runners=[translation_runner]
# )

# @svc.api(input=bentoml.io.Text(), output=bentoml.io.Text())
# async def translate(text: str) -> str:
#     # Assuming 'models' attribute is a list
#     # model_instance = translation_runner.models[0]

#     tokenizer = AutoTokenizer.from_pretrained('aceuganda/HEAL-BMG-grant-translation-english-luganda-v10')

#     if tokenizer is None:
#         return "Tokenizer not found in the model instance."

#     # Tokenize the input text using the correct tokenizer
#     inputs = tokenizer(text, return_tensors='pt', padding=True)

#     # Assuming 'generate' is a method of the model instance for text generation
#     generated = await translation_runner.async_run(**inputs)

#     # Process the logits to obtain the text output
#     output_ids = torch.argmax(generated['logits'], dim=-1).squeeze().tolist()

#     # Use the same tokenizer for Decoding the output...
#     output_text = tokenizer.batch_decode([output_ids], skip_special_tokens=True)[0]
    
#     return output_text

import bentoml
import torch
import uuid
from transformers import AutoTokenizer
from typing import Any, AsyncGenerator, Dict, TypedDict, Union
from bentoml import Service
from bentoml.io import JSON, Text

translation_runner = bentoml.models.get("text2textgeneration:latest").to_runner()

svc = bentoml.Service(
    name="englishtoluganda", runners=[translation_runner]
)

# class GenerateInput(TypedDict):
#     prompt: str
#     stream: bool
#     sampling_params: Dict[str, Any]

GenerateInput = dict[str, Union[str, bool, dict[str, Any]]]


@svc.api(
    route="/translate",
    input=JSON.from_sample(
        GenerateInput(
            prompt="What is fever?",
            stream=False,
            sampling_params={"temperature": 0.63, "logprobs": 1},
        )
    ),
    output=Text(content_type="text/event-stream"),
)

async def translate(request: GenerateInput) -> Union[AsyncGenerator[str, None], str]:
    n = request["sampling_params"].pop("n", 1)
    request_id = f"englishtoluganda-{uuid.uuid4().hex}"
    previous_texts = [[]] * n

    tokenizer = AutoTokenizer.from_pretrained('aceuganda/HEAL-BMG-grant-translation-english-luganda-v10')
    if tokenizer is None:
        return "Tokenizer not found in the model instance."

    # Tokenize the input text using the correct tokenizer
    inputs = tokenizer(request['prompt'], return_tensors='pt', padding=True)

    temperature = request["sampling_params"]["temperature"]

    generated = await translation_runner.async_run(**inputs)

    # Process the logits to obtain the text output
    output_ids = torch.argmax(generated['logits'], dim=-1).squeeze().tolist()

    # Use the same tokenizer for Decoding the output...
    output_text = tokenizer.batch_decode([output_ids], skip_special_tokens=True)[0]


    async def streamer() -> AsyncGenerator[str, None]:
        async for request_output in output_text:
            for output in request_output.outputs:
                i = output.index
                previous_texts[i].append(output.text)
                yield output.text

    if request["stream"]:
        return streamer()
    else:
        return output_text
        

    async for _ in streamer():
        pass
    return "".join(previous_texts[0])
