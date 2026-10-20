import asyncio
from playwright.async_api import async_playwright
import json

async def scrape_book():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        url = "https://search.shopping.naver.com/book/catalog/60278125307?fromwhere=people"
        print(f"Navigating to {url}...")
        
        await page.goto(url, wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_timeout(3000)
        
        title = await page.title()
        print("Page Title:", title)
        
        # 텍스트 수집
        text = await page.evaluate("() => document.body.innerText")
        
        with open("book_scraped_content.txt", "w", encoding="utf-8") as f:
            f.write(text)
            
        print(f"Successfully scraped {len(text)} characters.")
        lines = [line.strip() for line in text.split("\n") if len(line.strip()) > 5]
        print("\n--- Key Snippets ---")
        for line in lines[:30]:
            print(line)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_book())
