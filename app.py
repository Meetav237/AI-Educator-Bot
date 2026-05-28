import streamlit as st
import ollama
import json
import os
from datetime import datetime

# ---------- SETUP ----------
st.set_page_config(page_title="AI Tutor Bot", page_icon="📚")

st.title("AI Tutor Bot")
st.write("Ask questions, get explanations, hints, and quizzes.")

CHAT_FILE = "chats/saved_chats.json"

# Create chats folder if it does not exist
if not os.path.exists("chats"):
    os.makedirs("chats")

# Create saved_chats.json if it does not exist
if not os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "w") as file:
        json.dump([], file)


# ---------- FUNCTIONS ----------
def save_chat(subject, user_message, bot_response):
    with open(CHAT_FILE, "r") as file:
        chats = json.load(file)

    chats.append({
        "time": str(datetime.now()),
        "subject": subject,
        "user": user_message,
        "bot": bot_response
    })

    with open(CHAT_FILE, "w") as file:
        json.dump(chats, file, indent=4)


def get_tutor_response(subject, messages):
    system_prompt = (
        "You are an AI tutor for students. "
        "The selected subject is " + subject + ". "
        "Explain clearly and step by step. "
        "Do not just give the final answer. "
        "Help the student understand the reasoning."
    )

    ollama_messages = [{"role": "system", "content": system_prompt}]

    for message in messages:
        ollama_messages.append(message)

    response = ollama.chat(
        model="llama3.2",
        messages=ollama_messages
    )

    return response["message"]["content"]


# ---------- SESSION STATE ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_response" not in st.session_state:
    st.session_state.last_response = ""


# ---------- SIDEBAR ----------
subject = st.sidebar.selectbox(
    "Choose a subject:",
    ["Math", "Physics", "Chemistry", "Computer Science", "General Homework Help"]
)

if st.sidebar.button("Clear chat"):
    st.session_state.messages = []
    st.session_state.last_response = ""
    st.rerun()


# ---------- DISPLAY CHAT HISTORY ----------
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])


# ---------- CHAT INPUT ----------
question = st.chat_input("Ask a question:")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    with st.spinner("Thinking..."):
        answer = get_tutor_response(subject, st.session_state.messages)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.last_response = answer

    st.chat_message("assistant").write(answer)

    save_chat(subject, question, answer)


# ---------- HELPER BUTTONS ----------
st.divider()
st.subheader("Tutor Tools")

col1, col2, col3 = st.columns(3)

with col1:
    explain_simple = st.button("Explain simpler")

with col2:
    quiz_me = st.button("Quiz me")

with col3:
    give_hint = st.button("Give hint")


if explain_simple:
    prompt = "Explain your last answer in much simpler words."
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Simplifying..."):
        answer = get_tutor_response(subject, st.session_state.messages)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.last_response = answer
    st.chat_message("assistant").write(answer)

    save_chat(subject, prompt, answer)


if quiz_me:
    prompt = "Quiz me with 3 short questions about the topic we are discussing. Do not give the answers immediately."
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Making quiz..."):
        answer = get_tutor_response(subject, st.session_state.messages)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.last_response = answer
    st.chat_message("assistant").write(answer)

    save_chat(subject, prompt, answer)


if give_hint:
    prompt = "Give me a helpful hint, but do not fully solve the problem."
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Giving hint..."):
        answer = get_tutor_response(subject, st.session_state.messages)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.last_response = answer
    st.chat_message("assistant").write(answer)

    save_chat(subject, prompt, answer)
