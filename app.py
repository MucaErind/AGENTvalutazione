import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
from brain import CookingAgentBrain

st.set_page_config(page_title="Chef Agent AI", layout="wide")
if "brain" not in st.session_state: st.session_state.brain = CookingAgentBrain()
if "messages" not in st.session_state: st.session_state.messages = []
if "state" not in st.session_state: st.session_state.state = None

# --- SIDEBAR ---
st.sidebar.title("📊 Sidebar Info")
if st.session_state.state:
    st.sidebar.markdown("### 🛒 Ingredienti")
    for i in st.session_state.state.ingredients:
        st.sidebar.write(f"- {i.name} ({i.quantity}) {'⚠️' if i.is_expiring else ''}")
    st.sidebar.markdown("---")
    st.sidebar.write(f"**Skill:** {st.session_state.state.skill_level if st.session_state.state.skill_level else '?'}")
    st.sidebar.write(f"**Cucina:** {st.session_state.state.favorite_cuisine if st.session_state.state.favorite_cuisine else 'Default'}")

# --- CHAT ---
st.title("👨‍🍳 Il tuo Chef Personale")

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Scrivi qui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    history_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    
    with st.spinner("Lo chef sta pensando..."):
        # Aggiorna stato e ricevi risposta
        st.session_state.state = st.session_state.brain.update_state(history_str)
        response = st.session_state.brain.get_response(history_str, st.session_state.state)
        
        with st.chat_message("assistant"):
            if "IMAGE_PROMPT:" in response:
                text_part, img_part = response.split("IMAGE_PROMPT:")
                st.markdown(text_part)
                prompt_puro = img_part.strip().replace("[", "").replace("]", "").replace(" ", "%20")
                st.image(f"https://image.pollinations.ai/prompt/{prompt_puro}?width=500&height=500&nologo=true")
            else:
                st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})

    st.rerun()
