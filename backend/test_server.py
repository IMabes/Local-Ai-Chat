import httpx

SESSION_ID = "test-session-1"


def send(message: str):
    print(f"\n>>> {message}")
    with httpx.stream(
        "POST",
        "http://127.0.0.1:8000/chat",
        json={"message": message, "session_id": SESSION_ID},
    ) as r:
        for chunk in r.iter_text():
            print(chunk, end="", flush=True)
    print()


send("Merhaba, benim adım İrem.")
send("Benim adım neydi?")