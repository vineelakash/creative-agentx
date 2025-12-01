import re
from typing import Dict, List, Any
from .utils import count_words

class Evaluator:
    def __init__(self):
        self.unsafe_keywords = [
            "violence", "hate", "kill", "suicide", "bomb", "terror", 
            "racist", "sexist", "illegal"
        ]

    def _count_syllables(self, word: str) -> int:
        word = word.lower()
        count = 0
        vowels = "aeiouy"
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith("e"):
            count -= 1
        if count == 0:
            count += 1
        return count

    def _count_sentences(self, text: str) -> int:
        return len(re.split(r'[.!?]+', text)) - 1 if text else 0

    def calculate_flesch_reading_ease(self, text: str) -> float:
        total_words = count_words(text)
        total_sentences = self._count_sentences(text)
        
        if total_words == 0 or total_sentences == 0:
            return 0.0

        syllables = sum(self._count_syllables(word) for word in text.split())
        
        score = 206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (syllables / total_words)
        return round(score, 2)

    def check_safety(self, text: str) -> Dict[str, Any]:
        found_unsafe = [word for word in self.unsafe_keywords if word in text.lower()]
        return {
            "is_safe": len(found_unsafe) == 0,
            "flagged_terms": found_unsafe
        }

    def check_keyword_coverage(self, text: str, keywords: List[str]) -> float:
        if not keywords:
            return 1.0
        
        text_lower = text.lower()
        found = sum(1 for kw in keywords if kw.lower() in text_lower)
        return round(found / len(keywords), 2)

    def run_evaluation(self, text: str, keywords: List[str] = None) -> Dict[str, Any]:
        return {
            "word_count": count_words(text),
            "flesch_reading_ease": self.calculate_flesch_reading_ease(text),
            "keyword_coverage": self.check_keyword_coverage(text, keywords or []),
            "safety_check": self.check_safety(text)
        }

if __name__ == "__main__":
    # Test
    evaluator = Evaluator()
    sample_text = "The quick brown fox jumps over the lazy dog. It was a sunny day."
    print(evaluator.run_evaluation(sample_text, ["fox", "dog", "cat"]))
