from playwright.sync_api import Page, expect
from helper_functions import login

def test_student_can_enroll_and_staff_sees_enrolled_student(page: Page):
    page.goto('/')
    # login(page, 'kemianopiskelija', 'salasana123')
    # page.get_by_role('link', name='Laboratoriotyöt').click()
    # page.locator('[data-testid="group_1"]').click()
    # page.get_by_role('link', name='Kirjaudu ulos').click()
    login(page, 'kemianope', 'atomi123')
    # page.goto('/open_labs/')
    page.locator('[data-testid="11"]').click()
    expect(page.get_by_text('Kurssin Kuningasvesi laboratoriotyöhön labra 1 ilmoittautuneet opiskelijat')).to_be_visible()
