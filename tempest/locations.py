from abc import ABC, abstractmethod
from typing import Callable
from tempest.errors import SimulationException


class Location(ABC):
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def value(self) -> int:
        pass

    @property
    @abstractmethod
    def resilience(self) -> int:
        pass
    
    @abstractmethod
    def simulate_damage(self,intensity:float):
        pass
   
    @abstractmethod
    def set_damage_function(self,damage_function):
        pass

    @abstractmethod
    def __str__(self):
        pass

class Village(Location):
    def __init__(self,name,value,resilience):
        self._name = name
        self._value = value
        self._resilience = resilience
        self._next = None

    @property
    def name(self):
        return self._name
    
    @property
    def value(self):
        return self._value
    
    @property
    def resilience(self):
        return self._resilience
    
    def __str__(self):
        return f"Village {self._name}" 
    
    def simulate_damage(self, intensity):
        danni = self._value *(intensity*self._resilience)/10
        if danni <0:
            return 0
        else:
            return danni
        
    def set_damage_function(self, damage_function):
        raise SimulationException()
    
class City(Location):
    def __init__(self,name,value,resilience):
        self._name = name
        self._value = value
        self._resilience = resilience
        self._damage_function = None
        self._next = None

    @property
    def name(self):
        return self._name
    
    @property
    def value(self):
        return self._value
    
    @property
    def resilience(self):
        return self._resilience
    
    def __str__(self):
        return f"City {self._name}"
    
    def simulate_damage(self, intensity):
        if self._damage_function is not None: #se il danno non è none
            damage_percentuale = self._damage_function(intensity) #la percentuale di danno è la funzione danno,gli passo intensita del disastro     
            if self._resilience < intensity:
                return damage_percentuale* self._value
            else:
                return 0
        else:
            raise SimulationException
        
    def set_damage_function(self, damage_function):
        self._damage_function = damage_function
        
    

