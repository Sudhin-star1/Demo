import time
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from fake_useragent import UserAgent
from tqdm import tqdm

BASE_URL = "https://vapewholesaleusa.com/disposables?p={}"
USER_AGENT = UserAgent()

def get_headers():
    return {
        "User-Agent": USER_AGENT.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

def scrape_listing_page(page_num: int):
    """Scrape product cards from a listing page"""
    url = BASE_URL.format(page_num)
    try:
        r = requests.get(url, headers=get_headers(), timeout=15)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page_num}: {e}")
        return []

    soup = BeautifulSoup(r.text, 'html.parser')
    products = []

    for product in soup.select('li.item.product.product-item'):
        try:
            product_link = product.select_one('a.product-item-link')['href']
            product_title = product.select_one('a.product-item-link').get_text(strip=True)
            price = product.select_one('span.price').get_text(strip=True) if product.select_one('span.price') else None
            
            brand = None
            brand_element = product.select_one('.product-brand')
            if brand_element:
                brand = brand_element.get_text(strip=True)
            
            image_url = product.select_one('img.product-image-photo')['src']
            
            products.append({
                'brand': brand,
                'title': product_title,
                'price': price,
                'link': product_link,
                'image_url': image_url
            })
        except Exception as e:
            print(f"Error parsing product on page {page_num}: {e}")
            continue

    return products

def scrape_detail_page(url: str):
    """Scrape detailed product information"""
    try:
        r = requests.get(url, headers=get_headers(), timeout=15)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching product page {url}: {e}")
        return None, None, []

    soup = BeautifulSoup(r.text, 'html.parser')
    
    description = None
    desc_block = soup.select_one('div.product.attribute.description')
    if desc_block:
        description = desc_block.get_text(strip=True)
    
    stock_status = None
    stock_element = soup.select_one('div.product-info-stock-sku div.stock')
    if stock_element:
        stock_status = stock_element.get_text(strip=True)
    
    variants = []
    variant_rows = soup.select('table#product-options-wrapper tr')
    for row in variant_rows:
        try:
            flavor = row.select_one('td.col.item').get_text(strip=True) if row.select_one('td.col.item') else None
            sku = row.select_one('td.col.sku').get_text(strip=True) if row.select_one('td.col.sku') else None
            price = row.select_one('td.col.price').get_text(strip=True) if row.select_one('td.col.price') else None
            qty = row.select_one('td.col.qty').get_text(strip=True) if row.select_one('td.col.qty') else None
            
            variants.append({
                'flavor': flavor,
                'sku': sku,
                'price': price,
                'quantity': qty
            })
        except Exception as e:
            print(f"Error parsing variant on {url}: {e}")
            continue

    return description, stock_status, variants

def main():
    all_products = []
    page_num = 1
    max_pages = 10  
    max_products = 110

    with tqdm(desc="Scraping Pages", unit="page") as pbar:
        while page_num <= max_pages and len(all_products) < max_products:
            try:
                products = scrape_listing_page(page_num)
                if not products:
                    break  

                for product in tqdm(products, desc=f"Processing Page {page_num}"):
                    if len(all_products) >= max_products:
                        break

                    desc, stock, variants = scrape_detail_page(product['link'])
                    product['description'] = desc
                    product['stock_status'] = stock
                    product['variants_json'] = json.dumps(variants, ensure_ascii=False)
                    all_products.append(product)
                    
                    time.sleep(1.5)

                page_num += 1
                pbar.update(1)
                time.sleep(2) 
            except Exception as e:
                print(f"Error in main loop: {e}")
                break

    # Save results
    df = pd.DataFrame(all_products)
    output_file = "data/vapewholesaleusa_products.csv"
    df.to_csv(output_file, index=False)
    print(f"\n Successfully scraped {len(df)} products. Saved to {output_file}")

if __name__ == "__main__":
    main()


