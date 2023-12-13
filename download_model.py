import bentoml

model = "sshleifer/distilbart-cnn-12-6"
task = "summarization"

# Import the model directly without loading it into memory
bentoml.transformers.import_model(
   name=task,
   model_name_or_path=model,
   metadata=dict(model_name=model)
)