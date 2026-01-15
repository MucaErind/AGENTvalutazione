import streamlit as st
from dotenv import load_dotenv
import os

# Carica le variabili dal file .env PRIMA di importare il brain
load_dotenv()

from brain import CookingAgentBrain
from schema import UserState

st.set_page_config(page_title="Chef Assistant AI", layout="wide")

# Inizializzazione del Cervello e della Memoria
if "brain" not in st.session_state:
    st.session_state.brain = CookingAgentBrain()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_state" not in st.session_state:
    st.session_state.user_state = UserState()

# --- SIDEBAR ---
st.sidebar.title("📊 Stato Informazioni")
st.sidebar.markdown("### Ingredienti rilevati")
if not st.session_state.user_state.ingredients:
    st.sidebar.info("Nessun ingrediente rilevato.")
else:
    for ing in st.session_state.user_state.ingredients:
        status = "⚠️ In scadenza!" if ing.is_expiring else ""
        st.sidebar.write(f"- **{ing.name}**: {ing.quantity if ing.quantity else 'q.b.'} {status}")

st.sidebar.markdown("---")
st.sidebar.markdown("### Preferenze")
for pref in st.session_state.user_state.preferences:
    st.sidebar.write(f"- {pref}")

if st.session_state.user_state.has_enough_info:
    st.sidebar.success("✅ Pronto per le ricette!")
else:
    st.sidebar.warning("⏳ Mancano informazioni...")

# --- MAIN CHAT INTERFACE ---
st.title("👨‍🍳 Assistente Chef (Chip Huyen Style)")
st.write("Seguo i pattern del Cap. 6: Planning, Memory e Extraction.")

# Mostra i messaggi precedenti
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input dell'utente
if prompt := st.chat_input("Es: Ho della pasta e dei pomodori..."):
    # 1. Aggiungi messaggio utente
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepara la storia per il brain
    history_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])

    # 2. Aggiorna lo Stato (Pattern: Structured Extraction)
    with st.spinner("L'agente sta estraendo le informazioni..."):
        st.session_state.user_state = st.session_state.brain.update_state(history_str)

    # 3. Genera Risposta (Pattern: Planning basato sullo stato)
    with st.chat_message("assistant"):
        response = st.session_state.brain.get_response(history_str, st.session_state.user_state)
        st.markdown(response.content)
        st.session_state.messages.append({"role": "assistant", "content": response.content})
    
    # Riavvia per aggiornare la sidebar subito
    st.rerun()
