from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from ollama_client import stream_chat
from memory import get_history, add_message

app = FastAPI()


class ChatRequest(BaseModel):
    message: str
    session_id: str


@app.post("/chat")
async def chat(req: ChatRequest):
    add_message(req.session_id, "user", req.message)
    messages = get_history(req.session_id)

    async def generate():
        full_response = ""
        async for chunk in stream_chat(messages):
            full_response += chunk
            yield chunk
        add_message(req.session_id, "assistant", full_response)

    return StreamingResponse(generate(), media_type="text/plain")


app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")