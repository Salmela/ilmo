from playwright.sync_api import Page, expect
from helper_functions import login

def test_teacher_can_evaluate_a_report(page: Page):
    login(page, 'kemianopiskelija', 'salasana123')
    page.goto('/open_labs')
    page.locator('[data-testid="group_1"]').click()
    page.get_by_role('link', name='Kirjaudu ulos').click()

    login(page, 'kemianope', 'atomi123')
    page.goto('/open_labs')
    page.locator('[data-testid="group_1"]').click()
    page.get_by_role('link', name='Kirjaudu ulos').click()

    login(page, 'kemianopiskelija', 'salasana123')
    page.goto('/my_labs')
    expect(page.get_by_text('Palauta raportti')).to_be_visible()
    page.get_by_role('button', name='Palauta raportti').click()
    page.locator('[data-testid="file"]').set_input_files('config/file.pdf')
    page.get_by_role('button', name='Tallenna').click()
    page.get_by_role('link', name='Kirjaudu ulos').click()

    login(page, 'kemianope', 'atomi123')
    page.goto('/returned_reports')

    page.locator('[data-testid="open_1"]').click()
    page.get_by_test_id('select_grade').select_option('5')
    page.get_by_role('button', name='Arvostele').click()
    expect(page.get_by_text('Arvosteltu (5/5)')).to_be_visible()
