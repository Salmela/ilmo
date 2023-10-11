"""Sync module for later use"""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('http://127.0.0.1:8000/')
    page.get_by_role('button', name='Kirjaudu sisään').click()
    page.get_by_role('textbox', name='Username').fill('kemianopiskelija')
    page.get_by_role('textbox', name='Password').fill('salasana123')
    page.get_by_role('button', name='Log In').click()
    browser.close()