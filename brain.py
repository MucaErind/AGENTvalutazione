from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from schema import UserState
import os

class CookingAgentBrain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.1, # Leggermente più creativo per le ricette
            model_name="llama-3.3-70b-versatile",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        self.extractor_llm = self.llm.with_structured_output(UserState)
        
    def update_state(self, conversation_history: str) -> UserState:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Estrai informazioni dalla conversazione. "
                       "IMPORTANTE: Se l'utente menziona allergie, intolleranze o 'non mi piace X', inseriscilo nelle preferenze. "
                       "Imposta has_enough_info=True SOLO SE: \n"
                       "1. Hai almeno 3 ingredienti principali.\n"
                       "2. Hai chiesto o l'utente ha già dichiarato allergie/intolleranze."),
            ("user", "{history}")
        ])
        chain = prompt | self.extractor_llm
        return chain.invoke({"history": conversation_history})

    def get_response(self, conversation_history: str, current_state: UserState):
        # Logica di Planning (Cap. 6)
        if not current_state.has_enough_info:
            # Se mancano le preferenze/allergie, diamo priorità a quella domanda
            if not current_state.preferences:
                instruction = "Chiedi gentilmente se ci sono allergie, intolleranze o ingredienti non graditi prima di procedere."
            else:
                instruction = "Chiedi altri ingredienti o dettagli sulle quantità per arrivare ad avere almeno 3 ingredienti chiari."
        else:
            # Stile Mediterraneo Implicito
            instruction = ("Proponi 3 ricette basate sulla dieta mediterranea (uso di erbe, olio d'oliva, cotture semplici). "
                           "NON menzionare che stai usando la cucina mediterranea, presentala come scelta naturale.")

        prompt = ChatPromptTemplate.from_messages([
            ("system", f"Sei un assistente chef esperto. {instruction} "
                       "Sii cordiale e professionale. Rispondi sempre in italiano."),
            ("user", "{history}")
        ])
        chain = prompt | self.llm
        return chain.invoke({"history": conversation_history})
