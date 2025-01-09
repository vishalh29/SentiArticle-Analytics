import nltk
import ssl
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import re
import string
from pathlib import Path
from collections import Counter

class TextAnalyzer:
    def __init__(self, text):
        # Disable SSL verification for NLTK downloads
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        
        # Download required NLTK data with error handling
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
        except Exception as e:
            print(f"Warning: NLTK download failed - {str(e)}")
            print("Using basic sentence splitting as fallback...")
            
        self.text = text
        self.words = self._preprocess_text()
        self.sentences = self._get_sentences()
        
        # Load sentiment dictionaries
        self.positive_words = self._load_words('positive-words.txt')
        self.negative_words = self._load_words('negative-words.txt')
        
        # Calculate all metrics
        self._calculate_metrics()
    
    def _load_words(self, filename):
        """Load words from dictionary with robust encoding handling"""
        current_dir = Path(__file__).parent.absolute()
        file_path = current_dir / 'MasterDictionary' / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Dictionary file {filename} not found")
        
        word_set = set()
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'ascii', 'utf-16']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith(';'):
                            # Clean the word and add to set if valid
                            word = ''.join(c for c in line.lower() if c.isalnum() or c.isspace())
                            if word:
                                word_set.add(word)
                break  # If successful, break the loop
            except UnicodeDecodeError:
                continue
            except Exception:
                continue
                
        return word_set
    
    def _preprocess_text(self):
        """Clean and tokenize text"""
        # Convert to lowercase and split into words
        text = self.text.lower()
        # Remove special characters and split
        words = [word.strip('.,!?()[]{}":;') for word in text.split()]
        # Remove empty strings
        return [word for word in words if word]
    
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
        """Calculate text analysis metrics"""
        # Count positive and negative words
        positive_count = sum(1 for word in self.words if word in self.positive_words)
        negative_count = sum(1 for word in self.words if word in self.negative_words)
        
        self.positive_score = positive_count
        self.negative_score = negative_count
        
        # Calculate polarity score
        total_score = positive_count + negative_count
        self.polarity_score = (positive_count - negative_count) / (total_score + 0.000001)
        
        # Calculate subjectivity score
        self.subjectivity_score = total_score / (len(self.words) + 0.000001)
        
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
    
    def _get_sentences(self):
        """Get sentences with fallback if NLTK fails"""
        try:
            return sent_tokenize(self.text)
        except Exception:
            # Fallback to basic sentence splitting
            return [s.strip() for s in re.split(r'[.!?]+', self.text) if s.strip()]
