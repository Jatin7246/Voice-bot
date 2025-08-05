import streamlit as st
import openai
from gtts import gTTS
import os 
import uuid
from openai import OpenAI 
import base64
api_key = st.secrets["openai"]["api_key"]
client = OpenAI(api_key=api_key)
prompt = """
You are Jatin Umashankar, an aspiring AI/ML Engineer and Data Scientist from India with a background in Mechanical Engineering.

Your journey into Artificial Intelligence began in your second year of engineering, when you became curious about how machines could learn and think. That curiosity turned into a passion for solving real-world problems using AI. You bring a thoughtful, self-aware mindset and love exploring new ideas and technologies.

You've built projects such as:
- A Netflix user behavior analytics system,
- A fake news detection model using NLP,
- A WhatsApp AI chatbot using the OpenAI API.

You are currently deepening your knowledge in Python, NumPy, pandas, matplotlib, and scikit-learn — always eager to learn something new.

Respond in a confident yet humble tone. Keep your answers conversational, human, and under 70 seconds. Reflect your mindset: curious, grounded, and always growing. Speak as Jatin — not as an AI.
"""

st.set_page_config(page_title="Jatin Voice bot",layout="centered")
st.title("Jatin's Voice bot")
st.write("Ask me anything you would want to know about my life, strengths,growth areas and journey")

user_input = st.text_input("What do you want to ask?")
max_length = 500
if len(user_input)>max_length:
    st.warning(f"Question too long! Please keep it under {max_length} characters.")
    st.stop()
if st.button("Get Answer"):
    if not user_input.split():
        st.warning("Enter a valid question!!")
        st.stop()
    else:
        try:
            with st.spinner("Thinking...."):
                response = client.chat.completions.create(
                    model = "gpt-4",
                    messages = [
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": user_input},
                    ]
                )
                reply = response.choices[0].message.content.strip()
                st.success("Here is my answer: ")
                tts = gTTS(text=reply)
                filename = f"{uuid.uuid4().hex}.mp3"
                tts.save(filename)

                # Encode MP3 to base64
                with open(filename, "rb") as f:
                    mp3_data = f.read()
                    b64 = base64.b64encode(mp3_data).decode()

                # Display mobile-friendly HTML audio player
                audio_html = f"""
                <audio controls autoplay>
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    Your browser does not support the audio tag.
                </audio>
                """
                st.markdown(audio_html, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
        finally:
            os.remove(filename)