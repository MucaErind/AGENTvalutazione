from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from schema import UserState
import os

class CookingAgentBrain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile", groq_api_key=os.getenv("GROQ_API_KEY"))
        self.extractor_llm = self.llm.with_structured_output(UserState)
        
    def update_state(self, conversation_history: str) -> UserState:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Estrai le info dalla chat. Se l'utente sceglie una ricetta tra quelle proposte, scrivi il nome in 'selected_recipe'."),
            ("user", "{history}")
        ])
        return (prompt | self.extractor_llm).invoke({"history": conversation_history})

    def get_response(self, conversation_history: str, state: UserState):
        # 1. Ingredienti (almeno 3)
        if len(state.ingredients) < 3:
            return "Ciao! Per iniziare, elencami almeno 3 ingredienti che hai in cucina (specifica se sono in scadenza o le quantità!)."

        # 2. Allergie
        if not state.allergies_checked:
            return "Perfetto. Prima di procedere, hai allergie, intolleranze o alimenti che proprio non sopporti?"

        # 3. Livello Cucina
        if not state.skill_level_checked:
            return "Ottimo. Dimmi un'ultima cosa: qual è il tuo livello in cucina? Sei un principiante o un esperto?"

        # 4. Proposta 3 Opzioni
        if not state.selected_recipe:
            stile = f"cucina {state.favorite_cuisine}" if state.favorite_cuisine else "cucina mediterranea (senza nominarla)"
            prompt_opzioni = f"""Basandoti su questi ingredienti: {[i.name for i in state.ingredients]}. 
            Proponi solo i TITOLI di 3 opzioni diverse seguendo lo stile {stile}. 
            Sii breve e chiedi all'utente di sceglierne una scrivendo il nome."""
            return self.llm.invoke(prompt_opzioni).content

        # 5. Ricetta Finale (Solo se l'utente ha scelto)
        stile_finale = f"stile {state.favorite_cuisine}" if state.favorite_cuisine else "stile mediterraneo (implicito)"
        prompt_finale = f"""L'utente ha scelto: {state.selected_recipe}. 
        Crea una ricetta dettagliata per un {state.skill_level} in {stile_finale}.
        Usa SOLO gli ingredienti: {[i.name for i in state.ingredients]}.
        Includi: Tempo, Ingredienti con dosi, e una PREPARAZIONE MOLTO ESPLICITA.
        Alla fine scrivi esattamente: 'IMAGE_PROMPT: [descrizione del piatto pronto in inglese]'.
        Attribuisci il design a Chip Huyen Cap. 6."""
        return self.llm.invoke(prompt_finale).content
