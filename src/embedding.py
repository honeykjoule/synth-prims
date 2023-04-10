import openai
#from langchain.embeddings import OpenAIEmbeddings

def get_ada_embedding(text: str):
    text = text.replace("\n", " ")
    return openai.Embedding.create(
        input=[text], 
        model="text-embedding-ada-002"
    )["data"][0]["embedding"]