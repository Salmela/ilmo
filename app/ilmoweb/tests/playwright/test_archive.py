from playwright.sync_api import Page, expect
from helper_functions import login

def test_login_and_navigate_to_archive_page_from_navbar(page: Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.get_by_test_id('archive-button').click()
    expect(page).to_have_title('Arkisto')

def test_login_and_access_archive_url(page: Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.goto('/archive')
    expect(page).to_have_title('Arkisto')

def test_student_cant_access_archive(page: Page):
    page.goto('/')
    login(page, 'kemianopiskelija', 'salasana123')
    page.goto('/archive')
    expect(page.get_by_role('heading', name='Avoimet labrat')).to_be_visible()

def test_archive_page_shows_only_student_users(page: Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.goto('/archive')
    expect(page.get_by_text('Onni Opiskelija')).to_be_visible()
    expect(page.get_by_text('Steve Student')).to_be_visible()
    expect(page.get_by_text('Larry Rat')).to_be_visible()

def test_personal_archive(page: Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.goto('/archive')
    page.get_by_test_id('4').click()
    expect(page.get_by_text('Onni Opiskelija')).to_be_visible()
