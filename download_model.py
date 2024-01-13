import bentoml
import transformers

model = "aceuganda/HEAL-BMG-grant-translation-english-luganda-v10"

bentoml.transformers.save_model('heal-tokenizer', transformers.AutoTokenizer.from_pretrained(model))
bentoml.transformers.save_model('heal-model', transformers.AutoModelForSeq2SeqLM.from_pretrained(model))
