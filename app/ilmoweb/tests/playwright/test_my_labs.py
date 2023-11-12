from playwright.sync_api import Page, expect
from helper_functions import login

def test_teacher_can_evaluate_a_report(page: Page):
    login(page, 'kemianopiskelija', 'salasana123')
    page.goto('/open_labs')
    page.locator('[data-testid="group_1"]').click()
    page.locator('[data-testid="enroll_group_1"]').click()
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

def test_login_and_navigate_to_my_labs(page: Page):
    page.goto('/')
    login(page, 'kemianopiskelija', 'salasana123')
    page.get_by_role('link', name='Omat labrat').click()
    expect(page.get_by_role('heading', name='Omat ilmoittautumiset')).to_be_visible()

def test_enrolled_group_is_visible_in_my_labs(page: Page):
    login(page, 'kemianopiskelija', 'salasana123')
    #page.get_by_role('link', name='Laboratoriotyöt').click()
    #page.locator('[data-testid="group_1"]').click()
    page.get_by_role('link', name='Omat labrat').click()
    expect(page.get_by_text('labra 1')).to_be_visible()

def test_student_can_check_report_info(page: Page):
    login(page, 'kemianopiskelija', 'salasana123')
    page.get_by_role('link', name='Omat labrat').click()
    page.get_by_role('button', name='Avaa').click()
    expect(page.get_by_role('link', name='file.pdf')).to_be_visible()
    expect(page.get_by_text('Kalle Kemisti')).to_be_visible()
    expect(page.locator('td:text("5")')).to_be_visible()

def test_student_can_cancel_enrollment(page: Page):
    login(page, 'kemianopiskelija', 'salasana123')
    page.get_by_role('link', name='Laboratoriotyöt').click()
    page.locator('[data-testid="group_7"]').click()
    page.locator('[data-testid="enroll_group_7"]').click()
    page.get_by_role('link', name='Omat labrat').click()
    expect(page.get_by_text('Heisenberg')).to_be_visible()
    page.get_by_role('link', name='Laboratoriotyöt').click()
    page.locator('[data-testid="group_7"]').click()
    page.get_by_role('link', name='Omat labrat').click()
    expect(page.get_by_text('Heisenberg')).to_be_hidden()

