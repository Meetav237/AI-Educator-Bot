import os
import base64
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("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"))

st.title("AI Tutor Bot")
st.write("Upload a screenshot of your work. The AI gives a hint, not the full answer.")

uploaded_file = st.file_uploader("Upload your work", type=["png", "jpg", "jpeg"])

student_question = st.text_area("What are you trying to do?")

if st.button("Get Tutor Help"):
    if uploaded_file is None:
        st.error("Upload an image first.")
    else:
        image_bytes = uploaded_file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "You are an AI tutor. Look at the student's work and give helpful guidance. Do not directly solve the whole problem unless asked. Point out mistakes and give the next best hint."
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": student_question
                        },
                        {
                            "type": "input_image",
                            "image_url": "data:image/png;base64," + image_base64
                        }
                    ]
                }
            ]
        )

        st.subheader("Tutor Feedback")
        st.write(response.output_text)
