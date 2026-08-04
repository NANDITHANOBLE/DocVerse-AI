#This tracks chat history per session, so conversations have context (follow-up questions work).

from typing import Dict, List

# session_id -> list of {"role": "user"/"assistant", "content": str}
_chat_histories: Dict[str, List[dict]] = {}

def get_history(session_id: str) -> List[dict]:
    return _chat_histories.setdefault(session_id, [])

def add_message(session_id: str, role: str, content: str):
    get_history(session_id).append({"role": role, "content": content})

def clear_history(session_id: str):
    _chat_histories[session_id] = []