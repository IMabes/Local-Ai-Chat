from collections import defaultdict

MAX_HISTORY = 20  # session başına tutulacak maksimum mesaj sayısı

_sessions: dict[str, list[dict]] = defaultdict(list)


def get_history(session_id: str) -> list[dict]:
    return _sessions[session_id]


def add_message(session_id: str, role: str, content: str) -> None:
    history = _sessions[session_id]
    history.append({"role": role, "content": content})
    if len(history) > MAX_HISTORY:
        del history[: len(history) - MAX_HISTORY]