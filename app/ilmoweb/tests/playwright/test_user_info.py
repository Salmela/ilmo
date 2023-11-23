from playwright.sync_api import Page, expect
from helper_functions import login

def test_navigate_to_user_info(page: Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.get_by_test_id('user_info').click()
    expect(page).to_have_title('User info')

def test_user_info_is_correct(page:Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.get_by_test_id('user_info').click()
    expect(page.get_by_test_id('name')).to_have_text('Kalle Kemisti')
    expect(page.get_by_test_id('student_id')).to_have_text('100012000')
    expect(page.get_by_test_id('email')).to_have_text('kemianope@ilmoweb.fi')

def test_user_can_change_their_email(page:Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.get_by_test_id('user_info').click()
    page.get_by_test_id('new_email').fill('testi.meili@ilmoweb.fi')
    page.get_by_test_id('change_email').click()
    expect(page.get_by_test_id('email')).to_have_text('testi.meili@ilmoweb.fi')
