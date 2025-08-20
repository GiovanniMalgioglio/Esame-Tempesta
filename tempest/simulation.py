from tempest.locations import Location,Village,City
from typing import Tuple, List, Optional, Callable
from tempest.errors import SimulationException


class TempestSimulator:
    def __init__(self):
        self._locations = {}
    # R1
    def add_village(self, name: str, value: int, resilience: int) -> None:
        self._locations[name] = Village(name,value,resilience)
        
    def add_city(self, name: str, value: int, resilience: int) -> None:
        self._locations[name] = City(name,value,resilience)

    def get_location(self, name: str) -> Location:
        return self._locations[name]


    # R3
    def set_next(self, location: str, next_location: str, attenuation: float) -> None:
        self._locations[location]._next = (self._locations[next_location],attenuation) # ._next restituisce una tupla perche viene riepmpito

    def get_next(self, location: str) -> Optional[Tuple[Location, float]]:
        return self._locations[location]._next

    # R4
    def get_affected(self, start_location: str) -> List[Location]:
        affected = []
        current_location = self._locations[start_location]

        while current_location is not None: #fimnche ho locations da cui partire
            affected.append(current_location) #le metto nel dizionario
            if current_location._next is None: 
                break
            current_location = current_location._next[0] #primo elemto della tupl è la location
        return affected
    
    def get_total_damage(self, start_location: str, intensity: float) -> float:
        current_location = self._locations[start_location]
        total_damage = current_location.simulate_damage(intensity)
        while current_location._next is not None:
            current_location,attenuation = current_location._next
            intensity = intensity*attenuation
            total_damage += current_location.simulate_damage(intensity)
        return total_damage
        
           


    # R5
    def add_location(self, to_insert: str, location_before: str, attenuation: float) -> None:
       pass