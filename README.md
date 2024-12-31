# ArticleMetrics Analyzer

## Project Overview
A comprehensive article analysis system that processes web content to extract key metrics, sentiment scores, and readability insights. The analyzer performs deep content analysis to provide actionable metrics for understanding article complexity, sentiment, and readability.

## Features

The analysis generates the following metrics for each article:
- Sentiment Scores (Positive, Negative, Polarity, Subjectivity)
- Readability Metrics 
  - Average Sentence Length
  - Percentage of Complex Words 
  - Fog Index
  - Average Words per Sentence
- Word Statistics
  - Complex Word Count
  - Word Count
  - Syllables per Word
  - Personal Pronouns Count
  - Average Word Length

## Dependencies

Install required packages using:
```bash
pip install -r requirements.txt
```

Required packages:
- pandas
- nltk
- beautifulsoup4
- requests
- openpyxl

## How to Run

1. Ensure all dependencies are installed
2. Place your input file named `Input.xlsx` in the project root directory
3. Create a `MasterDictionary` folder with `positive-words.txt` and `negative-words.txt`
4. Run the main script:
```bash
python main.py
```

## Input Format

The Input.xlsx file should contain two columns:
- URL_ID: Unique identifier for each article
- URL: Web URL of the article to analyze

## Output

The script generates:
1. Individual text files for each article in the `extracted_articles` directory
2. An Excel file `Output Data Structure.xlsx` containing all analysis metrics

## Solution Approach

### 1. Text Extraction Strategy
- **Article Identification**: Analyzed various article HTML structures to identify common patterns
- **Data Cleaning**: 
  - Removed HTML tags and scripts
  - Handled special characters and encoding
  - Preserved important punctuation for sentence analysis
- **Content Extraction**: 
  - Focused on main article content using semantic HTML5 tags
  - Filtered out navigation, ads, and footer content
  - Preserved article structure for accurate sentence splitting

### 2. Text Analysis Implementation
- **Sentiment Analysis**:
  - Used custom dictionaries for positive/negative word identification
  - Implemented context-aware scoring to handle negations
  - Calculated normalized sentiment scores for consistent comparison
- **Readability Metrics**:
  - Implemented Gunning Fog Index for complexity measurement
  - Used syllable counting algorithms for word complexity
  - Created custom regex patterns for personal pronoun detection
- **Statistical Analysis**:
  - Word frequency analysis with stop word filtering
  - Sentence length calculation with proper boundary detection
  - Complex word identification using syllable rules

### 3. Performance Optimization
- **Memory Management**:
  - Processed articles sequentially to minimize memory usage
  - Implemented efficient text processing algorithms
  - Used generators where applicable for large datasets
- **Error Handling**:
  - Implemented robust URL fetching with retries
  - Added validation for input data quality
  - Created detailed error logging for troubleshooting

### 4. Data Processing Pipeline
1. **Input Processing**:
   - Excel file reading with data validation
   - URL sanitization and validation
2. **Content Extraction**:
   - Asynchronous URL fetching
   - HTML parsing and content extraction
   - Text cleaning and normalization
3. **Analysis**:
   - Sentiment scoring
   - Readability calculations
   - Statistical computations
4. **Output Generation**:
   - Results aggregation
   - Excel file generation
   - Individual article text storage
