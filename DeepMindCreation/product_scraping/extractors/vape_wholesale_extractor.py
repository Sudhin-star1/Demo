import json
import pandas as pd
from tqdm import tqdm
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3", temperature=0.0)

EXTRACTION_PROMPT = PromptTemplate.from_template("""
You are a product information extraction system for vape products. 
Extract the following fields from the product data below into JSON format:

{{
  "brand": "The manufacturer brand name",
  "model_type": "Specific model name/number",
  "flavor": "Primary flavor or flavor family",
  "puff_count": integer,
  "nicotine_strength": "e.g. 5% or 50mg",
  "battery_capacity": "e.g. 1000mAh",
  "coil_type": "e.g. Dual Mesh"
}}

Rules:
1. Extract brand from product title or phrases like "By [Brand]"
2. Model type should be the specific product identifier
3. For flavors, choose the primary flavor or family if multiple exist
4. Only include specifications explicitly mentioned

Product Data:
Title: {title}
Description: {description}
Price: {price}
Stock: {stock_status}

Return ONLY the JSON object with no additional commentary.
""")

def extract_with_llm(product_data: pd.Series) -> dict:
    """Extract structured fields using LLM"""
    try:
        prompt = EXTRACTION_PROMPT.format(
            title=product_data.get("title", ""),
            description=product_data.get("description", ""),
            price=product_data.get("price", ""),
            stock_status=product_data.get("stock_status", "")
        )
        
        response = llm.invoke(prompt).strip()
        
        json_start = response.find("{")
        json_end = response.rfind("}") + 1
        extracted_data = json.loads(response[json_start:json_end])
        
        return extracted_data
    except Exception as e:
        print(f"Error extracting data for {product_data.get('title', 'unknown product')}: {str(e)}")
        return {}

def main():
    try:
        raw_df = pd.read_csv("data/raw_vapewholesaleusa_products.csv")
    except FileNotFoundError:
        print("Error: data/vapewholesaleusa_products.csv not found. Please run the scraper first.")
        return

    raw_products = raw_df.to_dict('records')
    
    structured_products = []
    for product in tqdm(raw_products, desc="Extracting product info"):
        extracted = extract_with_llm(product)
        
        structured_product = {
            **product, 
            **extracted 
        }
        structured_products.append(structured_product)
    
    with open("data/vw_structured_output.json", "w") as f:
        json.dump(structured_products, f, indent=2)
    
    print(f"\n Successfully processed {len(structured_products)} products")
    print("Saved to data/vw_structured_output.json")

if __name__ == "__main__":
    main()