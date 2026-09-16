from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from ForRedis import chat
import os
load_dotenv()
app = FastAPI()

class chat_model(BaseModel):
    session_id: str
    message:str

@app.get("/")
async def root():
    return {"message": "Conversational RAG BOT for Nexora Company. ",
            "instructions": "Please use /chat to query the bot with your question. "}

@app.post("/chat")
async def query_bot(query: chat_model):
    response = chat(query.session_id,query.message)
    return{
        "session_id":query.session_id,
        "response":response
    }




