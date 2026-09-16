from agent import agent
from langchain_core.messages import HumanMessage, AIMessage
from langfuse.langchain import CallbackHandler
import os
import redis

REDIS_URL = os.getenv("REDIS_URL")

redis_client = redis.from_url(
    REDIS_URL,
    decode_responses=True
)

def get_history(session_id: str) -> list[str]:
    """Return the list of previous messages for this session."""
    key = f"chat:{session_id}"
    return redis_client.lrange(key, 0, -1) or []

def save_message(session_id: str, role: str, content: str) -> None:
    """Append a message to the session history."""
    key = f"chat:{session_id}"
    redis_client.rpush(key, f"{role}: {content}")
    # Optional: expire the history after 24 hours
    # redis_client.expire(key, 86400)

def chat(session_id: str, message: str) -> str:
    # Load previous messages
    history = get_history(session_id)

    # # Build a simple prompt that includes the conversation history
    # previous_messages = "\n".join(history)
    # prompt = f"""Previous messages: {previous_messages} Current user message: {message}"""

    messages=[] 

    for msg in history:
        if msg.startswith("Human: "):
            messages.append(HumanMessage(content=msg[7:]))
        elif msg.startswith("AI: "):
            messages.append(AIMessage(content=msg[4:]))

    messages.append(HumanMessage(content=message))

    #adding langfuse tracing 

    langfuse_handler = CallbackHandler()

    # Call the agent
    result = agent.invoke({"messages": messages},config={"callbacks":[langfuse_handler],"metadata":{"langfuse_session_id":session_id}})

    # Extract the actual reply text 
    if isinstance(result, dict) and "messages" in result:
        response = result["messages"][-1].content
    else:
        response = str(result)

    # Persist both sides of the turn
    save_message(session_id, "Human", message)
    save_message(session_id, "AI", response)

    return response