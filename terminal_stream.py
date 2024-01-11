import bentoml
import torch
import uuid
import asyncio
from transformers import AutoTokenizer
from typing import Any, AsyncGenerator, Dict, TypedDict, Union
from bentoml import Service
from bentoml.io import JSON, Text


translation_runner = bentoml.models.get("text2textgeneration:latest").to_runner()

svc = bentoml.Service(
    name="englishtoluganda", runners=[translation_runner]
)

GenerateInput = dict[str, Union[str, bool, dict[str, Any]]]

@svc.api(
    route="/translate",
    input=JSON.from_sample(
        GenerateInput(
            prompt="What is fever?",
            stream=True,
            sampling_params={"temperature": 0.63, "logprobs": 1},
        )
    ),
    output=Text(content_type="text/event-stream"),
)

async def translate(request: GenerateInput) -> Union[AsyncGenerator[str, None], str]:
    n = request["sampling_params"].pop("n", 1)
    request_id = f"englishtoluganda-{uuid.uuid4().hex}"
    temperature = request["sampling_params"]["temperature"]
    

    tokenizer = AutoTokenizer.from_pretrained('aceuganda/HEAL-BMG-grant-translation-english-luganda-v10')

    if tokenizer is None:
        return "Tokenizer not found in the model instance."

    # Tokenize the input text using the correct tokenizer.
    input_ids = tokenizer(request['prompt'], return_tensors='pt', padding=True)

    parameters = {}
    parameters['max_length'] = 1012  # Set your desired max_length here
    parameters['min_length'] = 100
    parameters['length_penalty'] = 10.0
    parameters['num_beams'] = 25
    parameters['early_stopping'] = True
    parameters['temperature'] = 0.5
    parameters['top_k'] = 25
    parameters['top_p'] = 1.0

    generated = await translation_runner.async_run(**input_ids, **parameters)

    print(f"LOGITS: {generated['logits']} ")
  
    async def streamer(text) -> AsyncGenerator[str, None]:
        # Initialize an empty string to accumulate the generated tokens
        accumulated_text = ""

        # Split the input text into lines
        lines = text.strip().split('\n')

        for line in lines:
            # Process each line
            accumulated_text += f"{line}\n"
            # Yield the accumulated text so far
            yield accumulated_text
            # Add a short sleep for demonstration purposes (you can adjust or remove this)
            await asyncio.sleep(0.1)

        # Make sure to yield the final result after processing all lines
        # yield accumulated_text
        # await asyncio.sleep(0)
    
    # Process the logits to obtain the text output
    output_ids = torch.argmax(generated['logits'], dim=-1)

    # Assuming batch_size is 1
    for token_id in output_ids[0]:
        # Make sure token_id is a scalar before using .item()
        max_token_id = token_id.item()
        print(f"MAX_TOKEN_ID: {max_token_id}")
        output_text = tokenizer.decode(max_token_id, skip_special_tokens=True)

        async for partial_response in streamer(output_text):
        # You can send the partial_response to the client
           print(f"Partial Response to Client: {partial_response}")
        # return streamer(output_text)