from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader

with open("/root/github/prior/data/mitnik_brushstrokes.txt", "r") as f:
    text = f.read()

loader = TextLoader(text)
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)
embedding = OpenAIEmbeddings()

persist_directory = "db"
vectordb = Chroma.from_documents(
    documents=docs, 
    embedding=embedding, 
    persist_directory=persist_directory
)

db = Chroma.from_documents(docs, embedding)
query = "How to win a case?"
docs = db.similarity_search(query)

print(docs[0].page_content)