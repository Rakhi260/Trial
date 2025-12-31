from RAG.llm_local import ask_llm

def rewrite_query(user_query: str) -> str:
    """
    Fixes broken / half / informal user queries
    into a complete meaningful question.
    """
    prompt = f"""
You are an AI assistant for Sunbeam Institute.

The user may:
- write broken English
- write half sentences
- write informal text

Rewrite the query into a clear, complete question.
DO NOT answer the question.

User query:
{user_query}

Rewritten question:
"""
    return ask_llm("", prompt).strip()
