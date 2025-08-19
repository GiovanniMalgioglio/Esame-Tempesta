from tempest.locations import Location
from typing import Tuple, List, Optional, Callable
from tempest.errors import SimulationException

class Village(Location):
    def __init__(self, name, value, resilience):
        self._name=name
        self._value=value
        self._resilience=resilience
        self._next=None
    
    @property
    def name(self):
        return self._name
    
    @property
    def value(self):
        return self._value
    
    @property
    def resilience(self) -> int:
        return self._resilience
    
    def __str__(self):
        return f"Village {self._name}"

    def simulate_damage(self, intensity: float) -> float:
        danni=self._value * (intensity - self._resilience) / 10
        if danni<0:
            return 0
        else:
            return danni

    def set_damage_function(self, damage_function: Callable[[float], float]) -> None:
        raise SimulationException()


class City(Location):
    def __init__(self, name, value, resilience):
        self._name=name
        self._value=value
        self._resilience=resilience
        self._damage_function = None
        self._next = None
        
    @property
    def name(self):
        return self._name
    
    @property
    def value(self):
        return self._value
    
    @property
    def resilience(self) -> int:
        return self._resilience
    
    def __str__(self):
        return f"City {self._name}"

    def simulate_damage(self, intensity: float) -> float:
        if self._damage_function is not None:
            damage_percentage = self._damage_function(intensity)
            if self._resilience < intensity:
                return damage_percentage * self._value
            else:
                return 0
        else:
            raise SimulationException()

    def set_damage_function(self, damage_function: Callable[[float], float]) -> None:
        self._damage_function=damage_function


class TempestSimulator:
    def __init__(self):
        self._locations={}
        
    # R1
    def add_village(self, name: str, value: int, resilience: int) -> None:
        self._locations[name]=Village(name, value, resilience)

    def add_city(self, name: str, value: int, resilience: int) -> None:
        self._locations[name]=City(name, value, resilience)

    def get_location(self, name: str) -> Location:
        return self._locations[name]

    # R3
    def set_next(self, location: str, next_location: str, attenuation: float) -> None:
        self._locations[location]._next=(self._locations[next_location], attenuation)

    def get_next(self, location: str) -> Optional[Tuple[Location, float]]:
        return self._locations[location]._next

    # R4
    def get_affected(self, start_location: str) -> List[Location]:
        current_location=self._locations[start_location]
        affected=[current_location]
        next=self._locations[start_location]._next
        while next is not None:
            affected.append(next[0])
            next=next[0]._next
        return affected
             
    def get_total_damage(self, start_location: str, intensity: float) -> float:
        current_location=self._locations[start_location]
        total_damage=current_location.simulate_damage(intensity)
        while current_location._next is not None:
            current_location, attenuation = current_location._next
            intensity=intensity*attenuation
            total_damage+=current_location.simulate_damage(intensity)
        return total_damage


    # R5
    def add_location(self, to_insert: str, location_before: str, attenuation: float) -> None:
        location_before=self._locations[location_before]
        to_insert=self._locations[to_insert]
        if location_before._next is None:
            self.set_next(location_before.name, to_insert.name, attenuation)
        else:
            self.set_next(to_insert.name, location_before._next[0].name, attenuation)
            self.set_next(location_before.name, to_insert.name, location_before._next[1])