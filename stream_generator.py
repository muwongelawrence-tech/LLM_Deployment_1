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

    generated = await translation_runner.async_run(**input_ids)
    output_ids = generated['logits']

    # Set initial values
    past_key_values = generated['past_key_values']
    token = None

    for i in range(max_tokens):
        if i == 0:  # prefill
            logits = output_ids
        else:  # decoding
            out = await translation_runner.async_run(past_key_values=past_key_values, inputs={"input_ids": torch.tensor([[token]])})
            logits = out.logits
            past_key_values = out.past_key_values

        last_token_logits = logits[0, -1, :]
   
        probs = torch.softmax(last_token_logits, dim=-1)
        token = int(torch.multinomial(probs, num_samples=1))
       
        # Decode the current token and yield it
        output_text = tokenizer.decode(
            token,
            skip_special_tokens=True,
            spaces_between_special_tokens=False,
            clean_up_tokenization_spaces=True
        )

        print(f"GENERATED RESPONSE: {output_text}")
        return streamer(output_text)