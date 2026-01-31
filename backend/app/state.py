from typing import Optional

class AppState:
    """
    Holds in-memory session state.
    Cleared on manual reset.
    """

    pinecone_index_name: Optional[str] = None
    retriever = None
    chat_memory = None

    raw_text: Optional[str] = None

app_state = AppState()
