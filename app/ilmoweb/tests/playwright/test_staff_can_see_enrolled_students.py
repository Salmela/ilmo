from playwright.sync_api import Page, expect
from helper_functions import login

def test_staff_does_not_see_student_who_cancelled_enrollment(page: Page):
    login(page, 'kemianopiskelija', 'salasana123')
    page.get_by_role('link', name='Laboratoriotyöt').click()
    page.locator('[data-testid="group_7"]').click()
    page.locator('[data-testid="enroll_group_7"]').click()
    page.get_by_role('link', name='Kirjaudu ulos').click()
    login(page, 'kemianope', 'atomi123')
    page.goto('/open_labs/')
    page.locator('[data-testid="7"]').click()
    student = page.locator('[data-testid="kemianopiskelija"]')
    expect(student).to_be_visible()
    page.locator('[data-testid="close_7"]').click()
    page.get_by_role('link', name='Kirjaudu ulos').click()
    login(page, 'kemianopiskelija', 'salasana123')
    page.get_by_role('link', name='Laboratoriotyöt').click()
    page.locator('[data-testid="group_7"]').click()
    page.get_by_role('link', name='Kirjaudu ulos').click()
    login(page, 'kemianope', 'atomi123')
    page.goto('/open_labs/')
    expect(page.get_by_text('kemianopiskelija')).to_be_hidden()
