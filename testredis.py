import os
import redis
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.from_url(
    os.getenv("REDIS_URL"),
    decode_responses=True
)

redis_client.set("test", "Hello Redis Cloud!")

value = redis_client.get("test")

print(value)