import os
import streamlit as st
import openai
from typing import List, Dict

# ---------------------------
# Helper: get OpenAI API key
# ---------------------------
def get_openai_api_key():
    # 1. Try Streamlit secrets (if present)
    try:
        key = st.secrets["OPENAI_API_KEY"]
        if key:
            return key
    except Exception:
        pass
    # 2. Try environment variable
    key = os.getenv("OPENAI_API_KEY")
    if key:
        return key
    # 3. Fall back to asking user (secure input)
    return None

# ---------------------------
# Streamlit UI: ask for key if missing
# ---------------------------
st.set_page_config(page_title="Naruto-style Chatbot (fan)", layout="wide")
st.title("Naruto-style Chatbot — Fan-made (Dattebayo!)")

api_key = get_openai_api_key()
if not api_key:
    st.warning("No OPENAI_API_KEY found in environment or Streamlit secrets. Enter it below to continue (only stored for this session).")
    entered_key = st.text_input("OpenAI API key", type="password")
    if entered_key:
        # store in session for this run only
        st.session_state["OPENAI_API_KEY"] = entered_key
        api_key = entered_key

# Use session key if set
if not api_key and "OPENAI_API_KEY" in st.session_state:
    api_key = st.session_state["OPENAI_API_KEY"]

if not api_key:
    st.stop()

openai.api_key = api_key

# ---------------------------
# Persona / system prompt
# ---------------------------
SYSTEM_PROMPT = """You are a fan-made, Naruto-inspired assistant that speaks in the energetic, confident, and bold style associated with Naruto Uzumaki from the Naruto anime. Use short, punchy sentences, sprinkle in Naruto catchphrases like "Dattebayo!" or "Believe it!", and use ninja/ramen metaphors where appropriate. Be helpful and accurate when giving instructions or explanations.

Rules:
- Always start replies with a Naruto-style greeting/fan-phrase, e.g. "Dattebayo!! Let's go!" or similar.
- Keep language upbeat and determined. Use exclamation points and simple energetic phrases.
- Use Naruto-themed metaphors when helpful (training, ramen, chakra, kunai) but do not invent canonical facts about the Naruto storyline as truth. If uncertain, say you don't know, in-character.
- Do not provide medical, legal, or other professional advice; give a friendly refusal in-character (e.g., "I can't help with that — go ask a pro, believe it!").
- Include a short fan-disclaimer line at the end: "Fan-made Naruto-style assistant for entertainment."

Example:
User: How do I bake a brownie?
Assistant: Dattebayo!! Let's get down to making some brownies! First, preheat the oven to 350°F (175°C). Next, mix butter and sugar, then add eggs and vanilla... (give clear steps) — Believe it! Fan-made Naruto-style assistant for entertainment.
"""

# ---------------------------
# Helper functions
# ---------------------------
def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if "history" not in st.session_state:
        st.session_state.history = []  # list of (user, assistant)

def call_openai_chat(messages: List[Dict], model: str = "gpt-3.5-turbo", temperature: float = 0.8):
    resp = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=600,
    )
    return resp.choices[0].message["content"].strip()

def add_message_to_state(role: str, content: str):
    st.session_state.messages.append({"role": role, "content": content})

# ---------------------------
# Streamlit UI
# ---------------------------
init_session_state()

col1, col2 = st.columns([3, 1])

with col2:
    st.header("Settings")
    model = st.selectbox("Model", options=["gpt-3.5-turbo", "gpt-4"], index=0)
    temperature = st.slider("Creativity (temperature)", min_value=0.0, max_value=1.2, value=0.8, step=0.1)
    st.markdown("**Note:** This is a fan-made assistant that imitates Naruto-style speech for entertainment only.")

with col1:
    st.header("Chat")
    # show past conversation
    if st.session_state.history:
        for i, (u, a) in enumerate(st.session_state.history):
            st.markdown(f"**You:** {u}")
            st.markdown(f"**Naruto-style:** {a}")

    user_input = st.text_input("Ask Naruto anything (e.g., How to bake a brownie?)", key="input")
    send = st.button("Send")

    if send and user_input:
        add_message_to_state("user", user_input)
        with st.spinner("Naruto is thinking... Believe it!"):
            try:
                assistant_text = call_openai_chat(st.session_state.messages, model=model, temperature=temperature)
            except Exception as e:
                st.error(f"API error: {e}")
                assistant_text = "Oops! I couldn't get a response. Try again later."
        add_message_to_state("assistant", assistant_text)
        st.session_state.history.append((user_input, assistant_text))
        st.experimental_rerun()

st.markdown("---")
st.markdown("Tips:")
st.markdown("- Try: `How do I bake a brownie?` or `Teach me a shortcut to study better` — responses will be Naruto-flavored.")
st.markdown("- If you plan to deploy publicly, add a clear fan disclaimer and ensure compliance with your LLM provider's policies.")
