"""Text analysis data models"""
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class TextStats:
    sentence_counts: Dict[str, int]
    smileys: List[str]
    dates: List[str]
    words: List[str]
    
    @property
    def vowel_start_words(self) -> List[str]:
        return [word for word in self.words if word[0].lower() in 'aeiou']
    
    @property
    def double_letter_words(self) -> List[str]:
        return [word for word in self.words if any(c1 == c2 for c1, c2 in zip(word, word[1:]))]