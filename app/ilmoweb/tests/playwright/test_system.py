from playwright.sync_api import Page, expect
from helper_functions import login

def test_navigate_to_system_page_as_superuser(page: Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.get_by_test_id('system-button').click()
    expect(page).to_have_title('System')

def test_navigate_to_system_page_as_not_superuser(page: Page):
    page.goto('/')
    login(page, 'kemianopiskelija', 'salasana123')
    expect(page.get_by_test_id('system-button')).to_be_hidden()

def test_update_message_to_students(page: Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.get_by_test_id('system-button').click()
    expect(page.get_by_test_id('current_message')).to_have_text('Ei viestiä')
    page.get_by_test_id('message').fill('Uusi viesti')
    page.get_by_test_id('send_message').click()
    expect(page.get_by_test_id('current_message')).to_have_text('Uusi viesti')


