# Vape Product Scraping and Information Extraction Pipeline

A complete system for scraping vape product data from e-commerce sites and extracting structured information using LLMs.


## Project Structure
product_scraping/
├── data/                           # Data files
│   ├── hybridLLMandregex.json         # Hybrid (LLM + regex) extraction results
│   ├── two_structured_output.json     # Structured output from dual LLMs
│   ├── vaperanger_vape_products.csv   # Raw scraped data from Vape Ranger
│   ├── vapewholesaleusa_products.csv  # Raw scraped data from Vape Wholesale USA
│   ├── vr_structured_output.json      # Vape Ranger LLM-structured output
│
├── extractors/                    # Data processing scripts
│   ├── vape_ranger_extractor.py       # Extracts structured fields from Vape Ranger data
│   ├── vape_wholesale_extractor.py    # Extracts structured fields from Vape Wholesale USA data
│
├── scrapers/                     # Web scraping scripts
│   ├── final_vaperanger_scraper.py    # Finalized scraper for Vape Ranger
│   ├── final_vapewholesale_scraper.py # Finalized scraper for Vape Wholesale USA
│
├── utils/                        # Utility functions and helpers
│
├── venv/                         # Python virtual environment
├── .gitignore                    # Specifies untracked files to ignore
├── README.md                     # Project documentation (this file)
└── test.py                       # Test and debug scripts



## Key Features

- **Web Scraping**: Collects product data from multiple vape e-commerce sites
- **LLM-Powered Extraction**: Uses Ollama/Llama3 to extract:
  - Brand names
  - Model/types
  - Technical specifications
  - Flavor profiles
- **Structured Output**: Produces clean JSON with consistent schema
- **Hybrid Approach**: Combines LLM intelligence with programmatic processing

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/product_scraping.git
   cd product_scraping
   python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate    # Windows
    pip install -r requirements.txt

2. Install ollama 
   Then run: ollama pull llama3


# Usage
Scraping Products

1. Run Vape Ranger scraper:
python scrapers/final_vaperanger_scraper.py

2. Run Vape Wholesale USA scraper:
python scrapers/final_vapewholesale_scraper.py

Processing Data
1. Extract structured data from Vape Ranger:
python extractors/vape_ranger_extractor.py

2. Extract structured data from Vape Wholesale USA:
python extractors/vape_wholesale_extractor.py

# Output Formats
Scraped data is saved as CSV files in data/. Processed outputs include:

hybridLLMandregex.json: Results using combined LLM and regex approach

hybridLLMandregularexp.json: Results using combined LLM and regex approach

two_structured_output.json: Pure LLM extraction results

vw_structured_output.json: Final processed Vape Ranger data



## Author
Sudhin Karki
