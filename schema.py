from pydantic import BaseModel, Field
from typing import List, Optional

class Ingredient(BaseModel):
    name: str = Field(default="")
    quantity: Optional[str] = Field(default="da definire")
    is_expiring: bool = Field(default=False)

class UserState(BaseModel):
    ingredients: List[Ingredient] = Field(default_factory=list)
    preferences: List[str] = Field(default_factory=list)
    favorite_cuisine: Optional[str] = Field(default=None)
    skill_level: Optional[str] = Field(default=None)
    
    # Flags di controllo flusso
    allergies_checked: bool = Field(default=False)
    skill_level_checked: bool = Field(default=False)
    
    # Gestione Opzioni
    options_proposed: List[str] = Field(default_factory=list, description="Lista dei nomi delle 3 opzioni proposte")
    selected_recipe: Optional[str] = Field(default=None, description="La scelta finale dell'utente")

