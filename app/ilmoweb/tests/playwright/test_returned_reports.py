from playwright.sync_api import Page, expect
from helper_functions import login

def test_teacher_can_add_notes_to_a_report(page:Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.goto('/returned_reports')
    page.get_by_test_id('open_1').click()
    page.get_by_test_id('notes').fill('tämä on muistiinpano')
    page.get_by_role('button', name='Tallenna muistiinpanot').click()
    expect(page.get_by_text('Muistiinpanot tallennettu')).to_be_visible()

def test_report_notes_stay_visible(page:Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.goto('/returned_reports')
    page.get_by_test_id('open_1').click()
    expect(page.get_by_text('tämä on muistiinpano')).to_be_visible()
    