from brain import CookingAgentBrain
from dotenv import load_dotenv
load_dotenv()

def test_new_logic():
    brain = CookingAgentBrain()
    print("🧪 Test 1: L'agente chiede delle allergie?")
    history = "Utente: Ciao, ho dei ceci, del tonno e della pasta."
    state = brain.update_state(history)
    response = brain.get_response(history, state)
    print(f"Risposta AI: {response.content}\n")

    print("🧪 Test 2: Verifica stile Mediterraneo (implicito)")
    # Simuliamo di aver risposto sulle allergie
    history2 = history + "\nAI: Hai allergie?\nUtente: No, nessuna allergia. Fammi le ricette."
    state2 = brain.update_state(history2)
    response2 = brain.get_response(history2, state2)
    print(f"Risposta AI (Ricette):\n{response2.content}")

if __name__ == "__main__":
    test_new_logic()
