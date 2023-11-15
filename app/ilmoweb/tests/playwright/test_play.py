from playwright.sync_api import Page, expect
from helper_functions import login

def test_welcome_message(page: Page):
    page.goto('/')
    assert page.inner_html('h1 b') == 'Fysikaalisen kemian<br>ilmoittautumisjärjestelmä'
