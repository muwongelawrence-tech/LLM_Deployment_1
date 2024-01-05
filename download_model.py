import bentoml

model = "aceuganda/HEAL-BMG-grant-translation-english-luganda-v10"
task = "text2textgeneration"

# Import the model directly without loading it into memory
bentoml.transformers.import_model(
   name=task,
   model_name_or_path=model,
   metadata=dict(model_name=model)
)