import json
from typing import AsyncGenerator

import httpx

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:3b"


async def stream_chat(messages: list[dict]) -> AsyncGenerator[str, None]:
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": True,
    }

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", OLLAMA_URL, json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if not line:
                    continue
                data = json.loads(line)
                if data.get("done"):
                    break
                content = data.get("message", {}).get("content", "")
                if content:
                    yield content