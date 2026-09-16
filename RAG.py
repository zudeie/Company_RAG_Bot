
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace,HuggingFaceEndpointEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_pinecone import PineconeVectorStore
from langchain_core.runnables import RunnableLambda,RunnableParallel,RunnablePassthrough,RunnableBranch
from pinecone import Pinecone
import os
from dotenv import load_dotenv
load_dotenv()

llm=HuggingFaceEndpoint(
    repo_id="NousResearch/Hermes-3-Llama-3.1-8B:featherless-ai",
    task="text-generation",
    max_new_tokens=50
)
model = ChatHuggingFace(llm=llm)

embedding=HuggingFaceEndpointEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2",
                                           task='feature-extraction')

# Setting up the vector store and retriever
pc=Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index=pc.Index("nexora-index")
vector_store=PineconeVectorStore(embedding=embedding,index=index)
retriver=vector_store.as_retriever(search_type="mmr",search_kwargs={"k":3})

#formatting the retrived docs to a string & making it runnable
def format_docs(retrived_docs):
    context_text="\n\n".join([doc.page_content for doc in retrived_docs])
    return context_text

format_docs_runnable = RunnableLambda(format_docs)

# Setting up the RAG chain
RAG_prompt = PromptTemplate(
    template="You are a helpful assistant.Who answers the question about the company when aseked by user.If you dont know an answer simpley say you dont know the answer , do not make up an answer by yourself. Use the following context to answer the question Context:{context}\n\nQuestion:{question}.\n",
    input_variables=["context", "question"]
)

Parallel_Chain= RunnableParallel({
    'context': retriver | format_docs_runnable,
    'question': RunnablePassthrough()
})

Rag_chain = Parallel_Chain | RAG_prompt | model

def Use_RAG(query: str)->str:
    response = Rag_chain.invoke(query)
    return response.content

# print(Use_RAG("What is the company policy on remote work?"))
