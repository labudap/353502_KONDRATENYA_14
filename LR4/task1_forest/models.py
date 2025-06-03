"""Forest data models"""
from dataclasses import dataclass
from typing import List

@dataclass
class TreeSpecies:
    name: str
    total: int
    healthy: int

    @property
    def sick_count(self) -> int:
        return self.total - self.healthy

    @property
    def sick_percentage(self) -> float:
        return (self.sick_count / self.total) * 100 if self.total else 0.0

class ForestData:
    def __init__(self, species_data: List[dict]):
        self.species = [
            TreeSpecies(
                name=item['species'],
                total=int(item['total']),
                healthy=int(item['healthy'])
            ) for item in species_data
        ]
    
    @property
    def total_trees(self) -> int:
        return sum(t.total for t in self.species)
    
    @property
    def total_healthy(self) -> int:
        return sum(t.healthy for t in self.species)
    
    @property
    def total_sick_percentage(self) -> float:
        return ((self.total_trees - self.total_healthy) / self.total_trees) * 100 if self.total_trees else 0.0