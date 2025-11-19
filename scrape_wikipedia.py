# scrape_wikipedia.py
# Simple scraper that saves full visible content of two pages to wikipedia_full_output/

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time, re
from pathlib import Path

PAGES = ["Artificial_intelligence", "Programming_language"]
WIKI_BASE = "https://en.wikipedia.org/wiki/"
OUTPUT_DIR = Path("wikipedia_full_output")
OUTPUT_DIR.mkdir(exist_ok=True)

options = Options()
# comment out headless line to see browser while debugging
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(6)

def clean_text(s):
    if not s:
        return ""
    s = re.sub(r"\[([^\]]+)\]", "", s)  # remove citations like [1]
    s = re.sub(r"\s+", " ", s).strip()
    return s

def extract_full_text(soup):
    content = soup.find("div", {"id": "mw-content-text"})
    if not content:
        return clean_text(soup.get_text(" ", strip=True))
    for sup in content.find_all("sup"):
        sup.decompose()
    toc = content.find("div", {"id": "toc"})
    if toc:
        toc.decompose()
    pieces = []
    for tag in content.find_all(["p","h2","h3","h4","h5","h6"], recursive=True):
        if tag.name == "p":
            txt = clean_text(tag.get_text(" ", strip=True))
            if len(txt) > 20:
                pieces.append(txt + "\n\n")
        else:
            span = tag.find("span", {"class":"mw-headline"})
            if span:
                pieces.append("\n\n" + span.get_text(strip=True) + "\n")
    if not pieces:
        return clean_text(content.get_text(" ", strip=True))
    return "".join(pieces).strip()

for slug in PAGES:
    url = WIKI_BASE + slug
    print("Opening:", url)
    driver.get(url)
    time.sleep(1.2)
    soup = BeautifulSoup(driver.page_source, "lxml")
    title_tag = soup.find("h1", {"id": "firstHeading"})
    title = title_tag.get_text(strip=True) if title_tag else slug
    text = extract_full_text(soup)
    path = OUTPUT_DIR / f"{slug}_full.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(title + "\n" + url + "\n\n" + text)
    print("Saved:", path)

driver.quit()
print("Done.")
