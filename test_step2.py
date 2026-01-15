from schema import UserState, Ingredient
from dotenv import load_dotenv
import os

load_dotenv()

def test_schema():
    try:
        sample = UserState(
            ingredients=[Ingredient(name="Pasta", quantity="500g", is_expiring=False)],
            preferences=["Vegetariano"],
            has_enough_info=False
        )
        print(f"✅ Schema Pydantic funzionante: {sample.json()}")
        
        if not os.getenv("GROQ_API_KEY"):
            print("❌ ERRORE: GROQ_API_KEY non trovata nel file .env")
        else:
            print("✅ Variabili d'ambiente caricate correttamente.")
    except Exception as e:
        print(f"❌ Errore: {e}")

if __name__ == "__main__":
    test_schema()
