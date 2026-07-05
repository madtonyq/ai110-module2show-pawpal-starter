from typing import List, Optional

class Pet:  # ✅ Fixed: PascalCase
    _next_id = 1
    
    def __init__(
        self,
        name: str,
        species: str,
        breed: str = "",
        age: int = 0,
        weight: float = 0.0,
        medical_conditions: Optional[List[str]] = None
    ):
        self.id_ = Pet._next_id
        Pet._next_id += 1
        self.name_ = name
        self.species_ = species
        self.breed_ = breed
        self.age_ = age
        self.weight_ = weight
        self.medical_conditions_ = medical_conditions if medical_conditions is not None else []
    
    def get_name(self) -> str:
        return self.name_
    
    def get_species(self) -> str:
        return self.species_
    
    def get_breed(self) -> str:
        return self.breed_
    
    def get_age(self) -> int:
        return self.age_
    
    def get_weight(self) -> float:
        return self.weight_
    
    def get_medical_conditions(self) -> List[str]:
        return self.medical_conditions_.copy()  # ✅ Fixed: return copy
    
    def has_medical_condition(self, condition: str) -> bool:  # ✅ Fixed: method name
        return condition.lower() in [c.lower() for c in self.medical_conditions_]  # ✅ Added case-insensitive
    
    def has_medical_conditions(self) -> bool:  # ✅ Added: check if any conditions exist
        return len(self.medical_conditions_) > 0
    
    def add_medical_condition(self, condition: str) -> None:
        if condition and condition not in self.medical_conditions_:
            self.medical_conditions_.append(condition)
    
    def remove_medical_condition(self, condition: str) -> None:
        if condition in self.medical_conditions_:
            self.medical_conditions_.remove(condition)
    
    def set_name(self, name: str) -> None:
        self.name_ = name
    
    def set_species(self, species: str) -> None:
        self.species_ = species
    
    def set_breed(self, breed: str) -> None:
        self.breed_ = breed
    
    def set_age(self, age: int) -> None:
        self.age_ = age
    
    def set_weight(self, weight: float) -> None:
        self.weight_ = weight
    
    def __repr__(self) -> str:
        return f"Pet(id={self.id_}, name='{self.name_}', species='{self.species_}', breed='{self.breed_}', age={self.age_}, weight={self.weight_}, medical_conditions={self.medical_conditions_})"