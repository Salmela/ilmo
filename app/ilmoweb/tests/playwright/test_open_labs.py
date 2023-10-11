import re
from playwright.sync_api import Page, expect

def test_has_title_and_heading(page: Page):
    page.goto('/')
    page.get_by_role('button', name='Kirjaudu sisään').click()
    page.get_by_role('textbox', name='Username').fill('kemianopiskelija')
    page.get_by_role('textbox', name='Password').fill('salasana123')
    page.get_by_role('button', name='Log In').click()
    page.goto('/open_labs/')
    expect(page).to_have_title(re.compile('Open Labs'))
    assert page.inner_text('h1') == 'Fysikaalisen kemian laboratorio - Labra'

def test_laboratoriotyot_button(page: Page):
    page.goto('/')
    page.get_by_role('button', name='Kirjaudu sisään').click()
    page.get_by_role('textbox', name='Username').fill('kemianopiskelija')
    page.get_by_role('textbox', name='Password').fill('salasana123')
    page.get_by_role('button', name='Log In').click()
    page.get_by_role('link', name='Laboratoriotyöt').click()
    expect(page.get_by_role('heading', name='Tulevat labrat')).to_be_visible()
