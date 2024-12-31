import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import re
import string

class TextAnalyzer:
    def __init__(self, text):
        # Download required NLTK data
        nltk.download('punkt')
        nltk.download('stopwords')
        
        self.text = text
        self.sentences = sent_tokenize(text)
        self.words = self._clean_and_tokenize()
        
        # Load sentiment dictionaries
        self.positive_words = self._load_words('MasterDictionary/positive-words.txt')
        self.negative_words = self._load_words('MasterDictionary/negative-words.txt')
        
        # Calculate all metrics
        self._calculate_metrics()
    
    def _load_words(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return set(file.read().splitlines())
        except:
            return set()
    
    def _clean_and_tokenize(self):
        # Remove punctuation and convert to lowercase
        text = self.text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Tokenize and remove stopwords
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text)
        return [word for word in words if word not in stop_words]
    
    def _count_syllables(self, word):
        word = word.lower()
        count = 0
        vowels = 'aeiouy'
        
        # Handle special cases
        if word.endswith('e'):
            word = word[:-1]
        if word.endswith(('es', 'ed')):
            word = word[:-2]
        
        # Count vowel groups
        prev_char_is_vowel = False
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_char_is_vowel:
                count += 1
            prev_char_is_vowel = is_vowel
        
        return max(1, count)
    
    def _calculate_metrics(self):
        # Sentiment scores
        self.positive_score = sum(1 for word in self.words if word in self.positive_words)
        self.negative_score = sum(1 for word in self.words if word in self.negative_words)
        
        # Polarity and Subjectivity
        denominator = (self.positive_score + self.negative_score) + 0.000001
        self.polarity_score = (self.positive_score - self.negative_score) / denominator
        self.subjectivity_score = (self.positive_score + self.negative_score) / (len(self.words) + 0.000001)
        
        # Readability metrics
        self.word_count = len(self.words)
        self.avg_sentence_length = self.word_count / len(self.sentences)
        
        # Complex words
        self.complex_word_count = sum(1 for word in self.words if self._count_syllables(word) > 2)
        self.percentage_complex_words = self.complex_word_count / self.word_count
        
        # Fog index
        self.fog_index = 0.4 * (self.avg_sentence_length + self.percentage_complex_words)
        
        # Other metrics
        self.avg_words_per_sentence = self.word_count / len(self.sentences)
        self.syllable_per_word = sum(self._count_syllables(word) for word in self.words) / self.word_count
        
        # Personal pronouns
        pronouns_pattern = r'\b(i|we|my|ours|us)\b'
        self.personal_pronouns = len(re.findall(pronouns_pattern, self.text.lower()))
        
        # Average word length
        self.avg_word_length = sum(len(word) for word in self.words) / self.word_count
