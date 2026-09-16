from agent import agent
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

    # Build a simple prompt that includes the conversation history
    previous_messages = "\n".join(history)
    prompt = f"""Previous messages: {previous_messages} Current user message: {message}"""

    # Call the agent
    result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})

    # Extract the actual reply text 
    if isinstance(result, dict) and "messages" in result:
        response = result["messages"][-1].content
    else:
        response = str(result)

    # Persist both sides of the turn
    save_message(session_id, "Human", message)
    save_message(session_id, "AI", response)

    return response