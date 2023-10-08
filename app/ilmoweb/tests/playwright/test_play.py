from playwright.sync_api import Page, expect

def test_welcome_message(page: Page):
    page.goto('/')
    assert page.inner_text('h1') == 'Fysikaalisen kemian laboratorio - Labra'

def test_login_link(page: Page):
    page.goto('/')
    page.get_by_role('link', name='Kirjaudu sisään').click()
    expect(page.get_by_role('heading', name='Log In')).to_be_visible()
"""
def test_admin_view(page: Page):
    page.goto('/')
    assert page.inner_text('h6') == 'Olet admin roolissa'

def test_student_view(page: Page):
    page.goto('/')
    assert page.inner_text('h6') == 'Olet käyttäjäroolissa'
"""