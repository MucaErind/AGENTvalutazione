from pydantic import BaseModel, Field
from typing import List, Optional

class Ingredient(BaseModel):
    name: str = Field(description="Nome dell'ingrediente")
    quantity: Optional[str] = Field(description="Quantità approssimativa (es. 200g, un pacco)")
    is_expiring: bool = Field(default=False, description="Vero se l'ingrediente è vicino alla scadenza")

class UserState(BaseModel):
    ingredients: List[Ingredient] = Field(default_factory=list, description="Lista degli ingredienti rilevati")
    preferences: List[str] = Field(default_factory=list, description="Preferenze o restrizioni alimentari (es. no uova, poco sale)")
    has_enough_info: bool = Field(default=False, description="Vero se abbiamo abbastanza info per dare 3 ricette")

