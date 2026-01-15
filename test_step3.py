from brain import CookingAgentBrain
from dotenv import load_dotenv
import os

load_dotenv()

def test_brain():
    try:
        brain = CookingAgentBrain()
        print("🤖 Test estrazione info con Llama-3.3...")
        test_history = "Utente: Ho della pasta e 200g di pomodori che stanno per scadere. Sono vegetariano."
        state = brain.update_state(test_history)
        
        print(f"✅ Ingredienti trovati: {len(state.ingredients)}")
        for ing in state.ingredients:
            print(f"   - {ing.name} | Quantità: {ing.quantity} | Scade: {ing.is_expiring}")
        print(f"✅ Preferenze: {state.preferences}")
        print(f"✅ Abbastanza info per ricette? {state.has_enough_info}")
    except Exception as e:
        print(f"❌ Errore durante il test: {e}")

if __name__ == "__main__":
    test_brain()
