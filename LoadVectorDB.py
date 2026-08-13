from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
import os 
from dotenv import load_dotenv
load_dotenv()


embeddings= HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
loader=PyPDFLoader("company_handbook/Nexora_Policy_Handbook.pdf")
documents=loader.load()

text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
splitted_docs=text_splitter.split_documents(documents)

#vector store
pc= Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index=pc.Index("nexora-index")
vector_store=PineconeVectorStore(embedding=embeddings, index=index)

def store():
    vector_store.add_documents(splitted_docs)
    return "Successfully Stored in Vector DB"

store()
