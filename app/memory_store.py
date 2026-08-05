# This tracks chat history per session, so conversations have context (follow-up questions work).

from typing import Dict, List

# session_id -> list of {"role": "user"/"assistant", "content": str}
_chat_histories: Dict[str, List[dict]] = {}

MAX_HISTORY_MESSAGES = 10  # keeps last 10 messages (5 user + 5 assistant turns)

def get_history(session_id: str) -> List[dict]:
    return _chat_histories.setdefault(session_id, [])

def add_message(session_id: str, role: str, content: str):
    history = get_history(session_id)
    history.append({"role": role, "content": content})

    # Trim history to keep only the most recent MAX_HISTORY_MESSAGES
    if len(history) > MAX_HISTORY_MESSAGES:
        _chat_histories[session_id] = history[-MAX_HISTORY_MESSAGES:]

def clear_history(session_id: str):
    _chat_histories[session_id] = []