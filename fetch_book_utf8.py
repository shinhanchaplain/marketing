import urllib.request
from bs4 import BeautifulSoup

url = 'https://m.search.naver.com/search.naver?query=AI+%ED%96%89%EC%A0%95%ED%95%99+%EB%A7%88%EC%8A%A4%ED%84%B0+%EA%B9%80%EC%A7%84%ED%98%B8'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15'})

html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
soup = BeautifulSoup(html, 'html.parser')
text = soup.get_text('\n', strip=True)

with open("ai_admin_book_scraped.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("Saved raw book text, total chars:", len(text))
