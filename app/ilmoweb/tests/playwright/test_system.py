from playwright.sync_api import Page, expect
from helper_functions import login

def navigate_to_system_page_as_superuser(page: Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.get_by_test_id('system-button').click()
    expect(page).to_have_title('System')

def navigate_to_system_page_as_not_superuser(page: Page):
    page.goto('/')
    login(page, 'kemianopiskelija', 'salasana123')
    page.get_by_test_id('system-button').click()
    expect(page).to_have_title('Created Labs')