"""Async module for later use."""
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('http://127.0.0.1:8000/')
        await browser.close()

asyncio.run(main())