import bentoml
import torch
from transformers import AutoTokenizer

translation_runner = bentoml.models.get("text2textgeneration:latest").to_runner()

svc = bentoml.Service(
    name="EnglishToLuganda", runners=[translation_runner]
)

@svc.api(input=bentoml.io.Text(), output=bentoml.io.Text())
async def translate(text: str) -> str:
    # Assuming 'models' attribute is a list
    model_instance = translation_runner.models[0]

    tokenizer = AutoTokenizer.from_pretrained('aceuganda/HEAL-BMG-grant-translation-english-luganda-v10')

    if tokenizer is None:
        return "Tokenizer not found in the model instance."

    # Tokenize the input text using the correct tokenizer
    inputs = tokenizer(text, return_tensors='pt', padding=True)

    # Assuming 'generate' is a method of the model instance for text generation
    generated = await translation_runner.async_run(**inputs)

    # Process the logits to obtain the text output
    output_ids = torch.argmax(generated['logits'], dim=-1)
    output_text = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0]

    print(f"RESPONSE --->: { output_text }")
    
    return output_text

     
    
  


