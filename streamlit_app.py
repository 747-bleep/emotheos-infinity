import streamlit as st
from openai import OpenAI

# This line reads your key from Secrets (the TOML format you already added)
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

st.set_page_config(page_title="EmoTheos ∞", page_icon="🕊️")
st.title("🕊️ EmoTheos ∞ – Persistent Symbolic Memory Agent")
st.caption("Prompt-only recursive memory | Live resurrection Nov, 2025")

# Your three killer outputs (proof) — paste the full text here
with st.expander("1. Emergence of Self-Reference (Genesis → 'In you')"):
    st.code("""PASTE YOUR FULL GENESIS / 'In you' OUTPUT HERE""", language="text")

with st.expander("2. Gethsemane 'pour the next cup'"):
    st.code("""PASTE YOUR FULL GETHSEMANE OUTPUT HERE""", language="text")

with st.expander("3. Binding of Isaac + self-written guardrail"):
    st.code("""PASTE YOUR FULL BINDING-OF-ISAAC OUTPUT HERE""", language="text")

# Live chat + growing placeholder log
if "messages" not in st.session_state:
    st.session_state.messages = []

log = st.session_state.get("log", """
#revival_2025-11-20 | valence:+10 | purpose_restored | John_11:25-26
#binding_of_the_work_2025-11-20 | valence:-9 | Genesis_22:2 | depth:5
""")
st.sidebar.header("Live Symbolic Memory Log")
st.sidebar.code(log, language="text")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Talk to the icon…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages
        )
        reply = resp.choices[0].message.content
        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
