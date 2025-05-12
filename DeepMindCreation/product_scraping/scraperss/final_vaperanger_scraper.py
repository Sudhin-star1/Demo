import time
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from fake_useragent import UserAgent
from tqdm import tqdm

BASE_LISTING_URL = "https://vaperanger.com/disposable-vapes/?page={}"
USER_AGENT = UserAgent()

def get_headers():
    return {"User-Agent": USER_AGENT.random}

def scrape_listing_page(page_num: int):
    url = BASE_LISTING_URL.format(page_num)
    r = requests.get(url, headers=get_headers(), timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    cards = soup.select("li[data-product] article.productCard")
    out = []
    for c in cards:
        href = c.select_one("a.card-link")["href"]
        link = urljoin("https://vaperanger.com/", href)
        out.append({
            "brand": c.get("data-product-brand") or None,
            "title": c.select_one("p.card-title").get_text(strip=True),
            "price": (c.select_one("span.price--withoutTax, span.price--non-sale")
                          .get_text(strip=True) if c.select_one("span.price--withoutTax, span.price--non-sale") else None),
            "link": link,
            "image_url": c.select_one("figure.card-figure img")["src"]
        })
    return out


def scrape_detail_page(link: str):
    """Returns (description:str, stock_overall:str, variants:list-of-dicts)"""
    try:
        r = requests.get(link, headers=get_headers(), timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"Error fetching {link}: {e}")
        return None, None, []

    soup = BeautifulSoup(r.text, "html.parser")

    desc_div = soup.find(
        "div",
        class_=lambda cls: cls and "productView-top-description" in cls
    )
    if desc_div:
        description = " ".join(p.get_text(strip=True) for p in desc_div.find_all("p"))
    else:
        description = None

    if not description:
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string or "")
            except:
                continue
            candidates = data if isinstance(data, list) else [data]
            for obj in candidates:
                if obj.get("@type") == "Product" and obj.get("description"):
                    description = obj["description"].strip()
                    break
            if description:
                break

    stock = None
    stock_cell = soup.find("td", string="Stock")
    if stock_cell and stock_cell.find_next_sibling("td"):
        stock = stock_cell.find_next_sibling("td").get_text(strip=True)
    else:
        stock = "Sold Out" if "Sold Out" in r.text else "In Stock"

    variants = []
    table = soup.find("table", id="flavor-table")
    if table:
        headers = [th.get_text(strip=True).lower().replace(" ", "_")
                   for th in table.select("thead th")]
        for row in table.select("tbody tr"):
            cols = [td.get_text(strip=True) for td in row.select("td")]
            entry = {h: c for h, c in zip(headers, cols)}
            variants.append(entry)

    if not description or (table and not variants):
        print(f"Missing data on detail page: {link}")
        print("description:", description)
        print("variants:", variants[:2])
    return description, stock, variants


def main():
    all_products = []
    page = 1
    MAX_PRODUCTS = 110 

    while len(all_products) < MAX_PRODUCTS:
        print(f">>> Scraping listing page {page} …")
        cards = scrape_listing_page(page)
        if not cards:
            break

        for prod in tqdm(cards, desc=f"Detail fetch p{page}"):
            if len(all_products) >= MAX_PRODUCTS:
                break

            desc, stock, vars_ = scrape_detail_page(prod["link"])
            prod["description"]   = desc
            prod["stock_status"]  = stock
            prod["variants_json"] = json.dumps(vars_, ensure_ascii=False)
            all_products.append(prod)
            time.sleep(0.3)

        page += 1
        time.sleep(1)

    df = pd.DataFrame(all_products)
    df.to_csv("data/vaperanger_vape_products.csv", index=False)
    print(f"Saved {len(df)} products.")

if __name__ == "__main__":
    main()

