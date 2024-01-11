# import bentoml

# model = "aceuganda/HEAL-BMG-grant-translation-english-luganda-v10"
# task = "text2textgeneration"

# # # Import the model directly without loading it into memory
# bentoml.transformers.import_model(
#    name=task,
#    model_name_or_path=model,
#    clone_repository=True, 
#    metadata=dict(model_name=model),
# )

import bentoml
import transformers

model = "aceuganda/HEAL-BMG-grant-translation-english-luganda-v10"

bentoml.transformers.save_model('heal-tokenizer', transformers.AutoTokenizer.from_pretrained(model))
bentoml.transformers.save_model('heal-model', transformers.AutoModelForSeq2SeqLM.from_pretrained(model))
