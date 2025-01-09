import os
import pandas as pd
from pathlib import Path
from collections import Counter

def load_negative_words():
    """Load negative words from master dictionary with robust encoding handling"""
    current_dir = Path(__file__).parent.absolute()
    neg_words_file = current_dir / 'MasterDictionary/negative-words.txt'
    
    if not neg_words_file.exists():
        raise FileNotFoundError("Negative words dictionary not found")
    
    # Try different encodings
    encodings = ['utf-8', 'latin-1', 'ascii', 'utf-16']
    negative_words = set()
    
    for encoding in encodings:
        try:
            with open(neg_words_file, 'r', encoding=encoding) as f:
                for line in f:
                    # Skip empty lines and comments
                    line = line.strip()
                    if line and not line.startswith(';'):
                        # Clean the word and add to set if valid
                        word = ''.join(c for c in line.lower() if c.isalnum() or c.isspace())
                        if word:
                            negative_words.add(word)
            # If successful, break the loop
            break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error with {encoding} encoding: {str(e)}")
            continue
    
    if not negative_words:
        raise ValueError("Could not read negative words with any encoding")
    
    return negative_words

def analyze_article(file_path, negative_words):
    """Analyze an article file for negative words"""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read().lower()
    
    # Split into words and remove special characters
    words = [word.strip('.,!?()[]{}":;') for word in text.split()]
    
    # Count negative words
    negative_word_counts = Counter()
    for word in words:
        if word in negative_words:
            negative_word_counts[word] += 1
            
    return {
        'total_negative_words': sum(negative_word_counts.values()),
        'unique_negative_words': len(negative_word_counts),
        'word_frequencies': dict(negative_word_counts)
    }

def main():
    try:
        current_dir = Path(__file__).parent.absolute()
        articles_dir = current_dir / 'extracted_articles'
        
        if not articles_dir.exists():
            raise FileNotFoundError("Articles directory not found")
        
        # Load negative words
        print("Loading negative words dictionary...")
        negative_words = load_negative_words()
        
        # Analyze each article
        print("Analyzing articles...")
        results = []
        
        for file_path in articles_dir.glob('*.txt'):
            try:
                article_id = file_path.stem
                analysis = analyze_article(file_path, negative_words)
                
                result = {
                    'Article_ID': article_id,
                    'Total_Negative_Words': analysis['total_negative_words'],
                    'Unique_Negative_Words': analysis['unique_negative_words'],
                    'Most_Common_Negative_Words': ', '.join(
                        f"{word}({count})" 
                        for word, count in sorted(
                            analysis['word_frequencies'].items(), 
                            key=lambda x: x[1], 
                            reverse=True
                        )[:5]
                    )
                }
                results.append(result)
                
            except Exception as e:
                print(f"Error analyzing article {file_path.name}: {str(e)}")
                continue
        
        # Create and save results DataFrame
        if results:
            df = pd.DataFrame(results)
            output_file = current_dir / 'negative_words_analysis.csv'
            df.to_csv(output_file, index=False)
            print(f"\nAnalysis complete. Results saved to {output_file}")
            
            # Print summary statistics
            print("\nSummary Statistics:")
            print(f"Total articles analyzed: {len(df)}")
            print(f"Average negative words per article: {df['Total_Negative_Words'].mean():.2f}")
            print(f"Maximum negative words in an article: {df['Total_Negative_Words'].max()}")
            
        else:
            print("No results were generated. Please check the input data and try again.")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
