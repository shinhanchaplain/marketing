import asyncio
from playwright.async_api import async_playwright

async def automate_figma():
    async with async_playwright() as p:
        try:
            print("Connecting to 127.0.0.1:9222...")
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            print(f"Total pages open: {len(context.pages)}")
            
            figma_page = None
            for page in context.pages:
                print(f"Page title: {await page.title()}, url: {page.url}")
                if "figma.com" in page.url:
                    figma_page = page
                    break
            
            if figma_page:
                print(f"Found active Figma page: {figma_page.url}")
                await figma_page.bring_to_front()
                # 단축키 전송
                await figma_page.keyboard.press("Control+p")
                await asyncio.sleep(1)
                await figma_page.keyboard.type("manifest")
                await asyncio.sleep(1)
                await figma_page.keyboard.press("Enter")
                print("Automated manifest trigger sent!")
            else:
                print("Figma page not found in active tabs.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(automate_figma())
