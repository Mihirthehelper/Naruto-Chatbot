# Naruto-style Chatbot (fan-made) — Streamlit

This repository contains a Streamlit app that uses OpenAI's Chat API to produce Naruto-themed responses (energetic, uses "Dattebayo!" / "Believe it!", ramen and ninja metaphors). It's intended for entertainment and education — a fan-created stylistic assistant.

## Files
- `app.py` — Streamlit app
- `requirements.txt` — Python dependencies

## Setup & Run
1. Create a virtualenv and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Set your OpenAI API key in the environment:
   ```bash
   export OPENAI_API_KEY="sk-..."
   # Windows (PowerShell)
   # $env:OPENAI_API_KEY="sk-..."
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Prompt / Persona Notes
- The app injects a system prompt instructing the model to speak in a Naruto-inspired style and provides a short example.
- Use temperature to control creativity: higher values = more flamboyant Naruto-style language.

## Legal & Safety Notes
- This is a fan-made assistant for entertainment. It imitates speech style and mannerisms but is not an official or exact reproduction of copyrighted characters.
- Do not use the app to impersonate real people.
- The assistant should not be used for professional medical, legal, or other regulated advice. If such questions are asked, it will politely refuse in-character.
- Before deploying publicly, check the LLM provider's policy on generating content in the style of copyrighted characters and ensure you include clear disclaimers for users.

## Improvements you might add
- Conversation trimming to limit token usage (e.g., keep only last N messages).
- Persist chat history (local file, DB) with user consent.
- Rate limits, usage monitoring, and content moderation filters.
- Styling the chat bubbles and adding user avatars.

Enjoy building — Dattebayo!!
