import streamlit as st
import ollama

st.title("AI Tutor Bot")

question = st.text_input("Ask a question:")

if question:
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "system", "content": "You are a helpful AI tutor. Explain things clearly and step by step."},
            {"role": "user", "content": question}
        ]
    )

    st.write(response["message"]["content"])
