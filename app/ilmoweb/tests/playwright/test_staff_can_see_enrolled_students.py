from playwright.sync_api import Page, expect
from helper_functions import login

def test_staff_does_not_see_student_who_cancelled_enrollment(page: Page):
    login(page, 'kemianopiskelija', 'salasana123')
    page.get_by_role('link', name='Laboratoriotyöt').click()
    page.get_by_test_id('group_7').click()
    page.get_by_test_id('enroll_group_7').click()
    expect(page.get_by_text('Ilmoittautuminen onnistui!')).to_be_visible()
    page.get_by_role('link', name='Kirjaudu ulos').click()
    login(page, 'kemianope', 'atomi123')
    page.goto('/open_labs/')
    page.get_by_test_id('7').click()
    student = page.get_by_test_id('kemianopiskelija').last
    expect(student).to_be_visible()
    page.get_by_test_id('close_7').click()
    page.get_by_role('link', name='Kirjaudu ulos').click()
    login(page, 'kemianopiskelija', 'salasana123')
    page.get_by_role('link', name='Laboratoriotyöt').click()
    page.get_by_test_id('group_7').click()
    expect(page.get_by_text('Ilmoittautuminen peruutettu')).to_be_visible()
    page.get_by_role('link', name='Kirjaudu ulos').click()
    login(page, 'kemianope', 'atomi123')
    page.goto('/open_labs/')
    expect(page.get_by_text('kemianopiskelija')).to_be_hidden()
