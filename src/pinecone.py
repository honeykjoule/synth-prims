from dotenv import load_dotenv
import os
import pinecone
from langchain.vectorstores import Pinecone
from langchain.vectorstores import VectorStore
from langchain.embeddings import OpenAIEmbeddings

def get_vectorstore():
    load_dotenv()
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
    table_name = "PRIOR"
    dimension = 1536
    metric = "cosine"
    pod_type = "p1"
    if table_name not in pinecone.list_tables():
        pinecone.create_index(
            table_name, 
            dimension=dimension, 
            metric=metric, 
            pod_type=pod_type
        )
    index = pinecone.Index(table_name)
    text_key = "page_content"
    embeddings_model =  OpenAIEmbeddings()
    vectorstore = Pinecone(index, embeddings_model.embed_query, text_key)
    return vectorstore