from playwright.sync_api import Page, expect
import pytest

def test_welcome_message(page: Page):
    page.goto('/')
    assert page.inner_text('h1') == 'Welcome to IlmoWeb!'