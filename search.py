#coding:utf-8
import torch
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity

openai.api_key = "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"

# choose text to embed
text_a = "我肚子有点饿"
text_b = "Classification using embeddings"

# choose an embedding
model_id = "text-similarity-davinci-001"

# compute the embedding of the text
embedding_a = get_embedding(text_a)
embedding_b = get_embedding(text_b)
sim = cosine_similarity(embedding_a, embedding_b)
print(sim)
