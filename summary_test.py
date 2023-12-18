import requests

response = requests.post(
   "http://0.0.0.0:3000/summarize",
   headers={
      "accept": "text/plain",
      "Content-Type": "text/plain",
   },
   data='A large language model (LLM) is a computerized language model, embodied by an artificial neural network using an enormous amount of parameters neurons in its layers with up to tens of millions to billions weights between them), that are (pre-)trained on many GPUs in relatively short time due to massive parallel processing of vast amounts of unlabeled texts containing up to trillions of tokens (i.e. parts of words) provided by corpora such as Wikipedia Corpus and Common Crawl, using self-supervised learning or semi-supervised learning, resulting in a tokenized vocabulary with a probability distribution. LLMs can be upgraded by using additional GPUs to (pre-)train the model with even more parameters on even vaster amounts of unlabeled texts.', # Replace $PROMPT here with your prompt.
)

print(response.text)