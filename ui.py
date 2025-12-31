import streamlit as st
from streamlit_pills import pills
import json
from datetime import datetime

from RAG.llm_local import ask_llm
from RAG.rag_pipeline import build_rag, ask_question
from RAG.query_rewriter import rewrite_query

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Sunbeam Chatbot")

CHAT_SAVE_PATH = "chat_history.json"

# ---------------- SESSION STATE ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "show_suggestions" not in st.session_state:
    st.session_state.show_suggestions = True

if "rag" not in st.session_state:
    st.session_state.rag = build_rag()

if "scroll_to" not in st.session_state:
    st.session_state.scroll_to = None

# ---------------- HELPERS ----------------
def is_greeting(text):
    return text.lower().strip() in [
        "hi", "hello", "hey", "good morning", "good evening"
    ]

def is_sunbeam_related(text):
    keywords = [
        "sunbeam", "course", "courses", "internship", "branch",
        "dac", "dbda", "placement", "market yard", "hinjawadi"
    ]
    return any(k in text.lower() for k in keywords)

def get_time_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    elif hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

def save_chat_to_file():
    with open(CHAT_SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(st.session_state.chat_history, f, indent=2, ensure_ascii=False)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("Chat History")

    if st.button("Save Chat"):
        save_chat_to_file()
        st.success("Chat saved to chat_history.json")

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.session_state.show_suggestions = True
        st.session_state.scroll_to = None
        st.session_state.pop("greeted", None)  # reset greeting
        st.rerun()

    st.divider()

# ---------------- MAIN UI ----------------
st.title("Sunbeam Chatbot")

# ---------------- TIME-BASED GREETING (ONCE PER SESSION) ----------------
if "greeted" not in st.session_state:
    st.session_state.greeted = True

    greeting = get_time_greeting()

    st.chat_message("assistant").write(
        f"{greeting}  Welcome to the **Sunbeam Chatbot**!\n\n"
        "You can ask me about:\n"
        "Sunbeam courses\n"
        "Internships & placements\n"
        "Branch details\n"
        "Or general questions like *What is Python?*"
    )

# ---------------- SHOW CHAT HISTORY ----------------
start_index = 0
if st.session_state.scroll_to is not None:
    start_index = st.session_state.scroll_to

for msg in st.session_state.chat_history[start_index:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------- SUGGESTIONS (ONCE) ----------------
selected_pill = None
if st.session_state.show_suggestions:
    selected_pill = pills(
        "Try asking:",
        [
            "Tell me about Sunbeam",
            "What courses does Sunbeam offer?",
            "Which course should I take?",
            "What is Python?"
        ],
        clearable=True,
        index=None,
    )

# ---------------- USER INPUT ----------------
user_input = st.chat_input("Ask your question...")
question = user_input or selected_pill

# ---------------- PROCESS QUESTION ----------------
if question:
    st.session_state.show_suggestions = False
    st.session_state.scroll_to = None

    # Store user message
    st.session_state.chat_history.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.write(question)

    rewritten = rewrite_query(question)

    # ---------- LOGIC ----------
    if is_greeting(question):
        answer = "Hello How can I help you today?"

    elif is_sunbeam_related(rewritten):
        context = ask_question(st.session_state.rag, rewritten)
        answer = ask_llm(context, rewritten)

    else:
        answer = ask_llm("", rewritten)

    # Store assistant message
    st.session_state.chat_history.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.write(answer)
