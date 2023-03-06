#coding:utf-8
import torch
import openai
# from openai.embeddings_utils import get_embedding, cosine_similarity

openai.api_key = "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"

# choose text to embed
text_a = "我肚子有点饿"
text_b = "Classification using embeddings"

# choose an embedding
model_id = "text-similarity-davinci-001"

# compute the embedding of the text
embedding_a = openai.Embedding.create(input=text_a, model=model_id)['data'][0]['embedding']
embedding_b = openai.Embedding.create(input=text_b, model=model_id)['data'][0]['embedding']

# import pdb;pdb.set_trace()
embedding_a = torch.tensor(embedding_a)
embedding_b = torch.tensor(embedding_b)
similarity = torch.cosine_similarity(embedding_a, embedding_b, dim=0)
similarity = float(similarity)
print('similarity', similarity)