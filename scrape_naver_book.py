import urllib.request
import re
from bs4 import BeautifulSoup
import json

url = "https://search.shopping.naver.com/book/catalog/60278125307?fromwhere=people"

req = urllib.request.Request(
    url,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
)

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
    
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("title").get_text() if soup.find("title") else "AI 행정학 마스터"
    print("Page Title:", title)

    # 텍스트 추출
    for s in soup(["script", "style", "nav", "footer"]):
        s.decompose()
    
    text = soup.get_text(separator="\n", strip=True)
    with open("scraped_book_raw.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Scraped length:", len(text))
    # 주요 내용 스니펫 출력
    lines = [line for line in text.splitlines() if len(line) > 10]
    print("\n--- Snippet Top 20 lines ---")
    for l in lines[:20]:
        print(l)

except Exception as e:
    print("Scraping error:", e)
