# Company RAG Bot (Nexora Recruitment Assistant)

This is a conversational AI bot I built for **virtual fictional** organization "Nexora Company". It can answer questions about company policies using RAG and also help candidates book interview slots.

## What it does

The bot has three main abilities:

1. Answers questions about company policies, benefits, remote work, leave rules etc by searching the company handbook (stored in Pinecone).
2. Checks if a particular interview slot is free.
3. Books an interview once the slot is confirmed available.

It remembers the conversation using Redis so it doesn't ask for the same information again and again.

I also added Langfuse for observability so I can see the full traces of every conversation and tool call.

## Tech Stack

- FastAPI for the backend API
- LangChain agents + tools
- HuggingFace Hermes-3-Llama-3.1-8B:featherless-ai as the LLM
- Pinecone as the vector database
- MySQL for storing interview bookings
- Redis for chat history
- Langfuse (self hosted) for tracing and observability
- SQLAlchemy for database operations

## Project Structure
```
Company_RAG_Bot/

├── agent.py            # Main agent + system prompt 
├── tools.py            # The three tools (policy, check slot, book slot)
├── Database.py         # MySQL functions for checking and booking
├── RAG.py              # RAG chain using Pinecone
├── ForRedis.py         # Chat history + main chat function + Langfuse
├── main.py             # FastAPI app
├── LoadVectorDB.py     # Script to load documents into Pinecone
├── company_handbook/   # Company policy documents
└── memory.py           # Older redis helper (not used much now)
```
## How to run

1. Clone the repo
```bash
git clone https://github.com/zudeie/Company_RAG_Bot.git
cd Company_RAG_Bot
```
2. Create a virtual environment and install dependencies

```bash
uv sync
(or use pip install -r requirements.txt if you prefer)
```
3. Create a .env file with these variables:
```bash
DATABASE_URL=mysql+pymysql://user:password@host:port/dbname
REDIS_URL=redis://...
PINECONE_API_KEY=your_pinecone_key
HUGGINGFACEHUB_API_TOKEN=your_hf_token
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=http://localhost:3000
```
4. Make sure your MySQL table exists. Something like:
```bash
SQLCREATE TABLE interview_bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    job VARCHAR(100),
    date VARCHAR(50),
    time VARCHAR(50)
);
```
5. Load the company handbook into Pinecone (run once):

```bash
python LoadVectorDB.py
```
6. Start Langfuse (self-hosted)::

```
git clone https://github.com/langfuse/langfuse.git
cd langfuse
docker compose up -d
```
#### Then open http://localhost:3000 and create a project + API keys.
7. Start the server:

```bash
uvicorn main:app --reload
```
#### The API will be available at http://localhost:8000

API Usage

Send a POST request to /chat

``` 
JSON{
  "session_id": "any-unique-id",
  "message": "I want to book a Software Engineer interview"
}
```

Example with curl:

```Bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "user123", "message": "What is the remote work policy?"}'
```
Use the same session_id for the whole conversation so the bot remembers previous messages.
### How the booking flow works

1. User says they want to book an interview
2. Bot collects name, email, job, date and time
3. Bot first calls check_interview_slot
4. If the slot is free, it calls book_interview_slot
5. Confirms the booking to the user
6. The bot is instructed to never book without checking first.

### Observability

#### I integrated Langfuse (self-hosted) so every conversation and tool call is traced. You can see the full flow in the Langfuse UI at http://localhost:3000.

### Notes

* The LLM is currently Qwen2.5-7B through HuggingFace. 
* It works but stronger models give more consistent tool calling.
* Chat history is stored in Redis as plain strings with "Human: " and "AI: " prefixes.
* Make sure the date and time format you pass matches what is stored in the database.

### Future improvements I want to add

* Simple Streamlit or React frontend
* Ability to cancel or reschedule interviews
* Email confirmation after booking
* Better date parsing (so users can say "next Monday at 10am")
* History length limit so Redis doesn't grow forever
* Better error messages when the database is down
* Feel free to open issues or suggest improvements.