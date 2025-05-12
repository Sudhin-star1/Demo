import json
import pandas as pd
from tqdm import tqdm
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3", temperature=0.0)

FULL_EXTRACTION_PROMPT = PromptTemplate.from_template("""
You are a product information extraction system for vape products. Analyze the following product data and extract:

{{
  "brand": "Manufacturer name extracted from title/description",
  "model_type": "Specific model name/number",
  "flavors": ["list", "of", "all", "flavors"],
  "puff_count": integer,
  "nicotine_strength": "e.g. 5% or 50mg",
  "battery_capacity": "e.g. 1000mAh",
  "coil_type": "e.g. Dual Mesh",
  "e_liquid_capacity": "e.g. 15ml"
}}

Rules:
1. For brand: Extract from phrases like "By [Brand]" or product naming patterns
2. For model_type: Extract specific model codes (e.g. NV30K) or descriptive names
3. List ALL flavors mentioned in the description
4. Only include specifications explicitly mentioned
5. Return null for missing fields

Product Data:
Title: {title}
Description: {description}
Variants: {variants}

Return ONLY the JSON object with no additional text.
""")

def extract_with_llm(product_data: dict) -> dict:
    """Extract all fields using LLM in a single pass"""
    try:
        variants = []
        try:
            variants = json.loads(product_data.get("variants_json", "[]"))
            variants_text = "\n".join([f"- {v.get('flavor', '')}" for v in variants])
        except:
            variants_text = ""
        
        prompt = FULL_EXTRACTION_PROMPT.format(
            title=product_data.get("title", ""),
            description=product_data.get("description", ""),
            variants=variants_text
        )
        
        response = llm.invoke(prompt).strip()
        json_start = response.find("{")
        json_end = response.rfind("}") + 1
        return json.loads(response[json_start:json_end])
    
    except Exception as e:
        print(f"Error processing {product_data.get('title', 'unknown')}: {str(e)}")
        return {}

def main():
    try:
        df = pd.read_csv("data/vaperanger_vape_products.csv")
        raw_products = df.to_dict('records')
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return

    structured_products = []
    for product in tqdm(raw_products, desc="Processing products"):
        extracted = extract_with_llm(product)
        
        structured_product = {
            **{k: v for k, v in product.items() if k != "variants_json"},
            **extracted
        }
        structured_products.append(structured_product)
    
    output_path = "data/vr_structured_output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(structured_products, f, indent=2, ensure_ascii=False)
    
    print(f"\n Successfully processed {len(structured_products)} products")
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()