"""Text analysis core logic with mixins"""
import re
from typing import List, Dict, Tuple

class TextAnalysisMixin:
    """Mixin for basic text analysis methods"""
    
    @staticmethod
    def split_sentences(text: str) -> List[str]:
        return [s.strip() for s in re.findall(r'[^.!?]+[.!?]', text) if s.strip()]

    @staticmethod
    def extract_words(text: str) -> List[str]:
        return [word.lower() for word in re.findall(r'\b\w+\b', text)]

    @staticmethod
    def count_sentence_types(sentences: List[str]) -> Dict[str, int]:
        return {
            'total': len(sentences),
            'declarative': sum(1 for s in sentences if s.endswith('.')),
            'interrogative': sum(1 for s in sentences if s.endswith('?')),
            'exclamatory': sum(1 for s in sentences if s.endswith('!'))
        }

class PatternAnalysisMixin:
    """Mixin for pattern-based analysis methods"""
    
    @staticmethod
    def find_smileys(text: str) -> List[str]:
        return [s for s in re.findall(r'(?::|;)-*[(\[)\]]+', text) 
                if re.fullmatch(r'[:;]-*[(\[)\]]+', s)]

    @staticmethod
    def find_dates(text: str) -> List[str]:
        return list(set(re.findall(r'\b\d{2}-\d{2}-(\d{4})\b', text)))

    @staticmethod
    def check_double(word: str) -> bool:
        return bool(re.search(r'([A-Za-z])\1', word))

class WordAnalysisMixin:
    """Mixin for word-specific analysis methods"""
    
    @staticmethod
    def check_letters(words: List[str]) -> List[str]:
        return [word for word in words if re.findall(r'\b\w+[^aeiou]{1}[aeiou]{1}\w{1}\b', word)]
    
    @staticmethod
    def get_vowel_words(words: List[str]) -> List[str]:
        return [word for word in words if re.search(r'^[aeiou]', word)]
    
    @staticmethod
    def get_doubles(words: List[str]) -> Dict[int, str]:
        return {
            i: word for i, word in enumerate(words, start=1)
            if TextAnalyzer.check_double(word)
        }

    @staticmethod
    def get_alphabetical(words: List[str]) -> List[str]:
        return sorted(words)

class TextAnalyzer(TextAnalysisMixin, PatternAnalysisMixin, WordAnalysisMixin):
    """Main analyzer class combining all mixins"""
    
    @staticmethod
    def analyze_text(text: str) -> Dict:
        sentences = TextAnalyzer.split_sentences(text)
        words = TextAnalyzer.extract_words(text)
        
        return {
            'sentence_counts': TextAnalyzer.count_sentence_types(sentences),
            'smileys': TextAnalyzer.find_smileys(text),
            'dates': TextAnalyzer.find_dates(text),
            'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0,
            'avg_sentence_length': sum(len(s) for s in sentences) / len(sentences) if sentences else 0,
            'vowel_words': TextAnalyzer.get_vowel_words(words),
            'special_words': TextAnalyzer.check_letters(words),
            'doubles': TextAnalyzer.get_doubles(words),
            'alphabetical': TextAnalyzer.get_alphabetical(words)
        }