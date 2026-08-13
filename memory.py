import os
import redis
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.from_url(
    os.getenv("REDIS_URL"),
    decode_responses=True
)


def save_message(session_id, role, message):

    key = f"chat:{session_id}"

    redis_client.rpush(
        key,
        f"{role}: {message}"
    )


def get_history(session_id):

    key = f"chat:{session_id}"

    return redis_client.lrange(key, 0, -1)