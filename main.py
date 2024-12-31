import pandas as pd
from text_extractor import extract_article
from text_analyzer import TextAnalyzer
from pathlib import Path
import os
import sys

def verify_file_structure():
    current_dir = Path(__file__).parent.absolute()
    
    # Check required files and directories
    required_files = [
        'Input.xlsx',
        'MasterDictionary/positive-words.txt',
        'MasterDictionary/negative-words.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not (current_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("Missing required files:")
        for file in missing_files:
            print(f"- {file}")
        print("\nPlease ensure all required files are present before running the script.")
        sys.exit(1)

def main():
    # Verify file structure first
    verify_file_structure()
    
    # Get the current directory where the script is located
    current_dir = Path(__file__).parent.absolute()
    
    # Define input and output paths
    input_file = current_dir / 'Input.xlsx'
    output_dir = current_dir / 'extracted_articles'
    
    # Check if input file exists
    if not input_file.exists():
        print(f"Error: Input file not found at {input_file}")
        print("Please ensure 'Input.xlsx' is in the same directory as the script.")
        sys.exit(1)
    
    # Create directories if they don't exist
    output_dir.mkdir(exist_ok=True)
    
    try:
        # Read input Excel file
        input_df = pd.read_excel(input_file)
        
        # Initialize lists to store results
        results = []
        
        # Process each URL
        for index, row in input_df.iterrows():
            try:
                url_id = str(row['URL_ID'])
                url = row['URL']
                
                print(f"Processing URL {url_id}: {url}")
                
                # Extract article text
                article_text = extract_article(url)
                
                if not article_text:
                    print(f"Warning: No text extracted from URL {url_id}")
                    continue
                
                # Save extracted text
                text_file = output_dir / f"{url_id}.txt"
                with open(text_file, 'w', encoding='utf-8') as f:
                    f.write(article_text)
                
                # Analyze text
                analyzer = TextAnalyzer(article_text)
                
                # Get analysis results
                result = {
                    'URL_ID': url_id,
                    'URL': url,
                    'POSITIVE_SCORE': analyzer.positive_score,
                    'NEGATIVE_SCORE': analyzer.negative_score,
                    'POLARITY_SCORE': analyzer.polarity_score,
                    'SUBJECTIVITY_SCORE': analyzer.subjectivity_score,
                    'AVG_SENTENCE_LENGTH': analyzer.avg_sentence_length,
                    'PERCENTAGE_OF_COMPLEX_WORDS': analyzer.percentage_complex_words,
                    'FOG_INDEX': analyzer.fog_index,
                    'AVG_WORDS_PER_SENTENCE': analyzer.avg_words_per_sentence,
                    'COMPLEX_WORD_COUNT': analyzer.complex_word_count,
                    'WORD_COUNT': analyzer.word_count,
                    'SYLLABLE_PER_WORD': analyzer.syllable_per_word,
                    'PERSONAL_PRONOUNS': analyzer.personal_pronouns,
                    'AVG_WORD_LENGTH': analyzer.avg_word_length
                }
                results.append(result)
                
            except Exception as e:
                print(f"Error processing URL {url_id}: {str(e)}")
                continue
        
        # Create output DataFrame and save to Excel
        if results:
            output_df = pd.DataFrame(results)
            output_file = current_dir / 'Output Data Structure.xlsx'
            output_df.to_excel(output_file, index=False)
            print(f"\nAnalysis complete. Results saved to {output_file}")
        else:
            print("No results were generated. Please check the input data and try again.")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
