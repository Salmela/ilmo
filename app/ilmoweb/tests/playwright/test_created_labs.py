import re
from playwright.sync_api import Page, expect
from helper_functions import login

def test_login_and_navigate_to_created_labs(page: Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    expect(page).to_have_title(re.compile('Created labs'))

def test_create_lab_and_check_that_it_is_created(page: Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.locator('[data-testid="1"]').click()
    page.get_by_test_id('lab_name').fill('Testilabra')
    page.get_by_test_id('description').fill('Kuvaus testilabrasta.')
    page.get_by_test_id('max_students').fill('3')
    page.get_by_role('button', name='Luo labra').click()
    page.goto('/created_labs')
    expect(page.get_by_role('cell', name='Testilabra'))

def test_toggling_labgroup_status(page: Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    assert page.get_by_test_id('status_2').inner_text() == 'Ei julkaistu'
    page.get_by_test_id('publish_2').click()
    assert page.get_by_test_id('status_2').inner_text() == 'Ilmoittautuminen käynnissä'
    page.get_by_test_id('cancel_2').click()
    assert page.get_by_test_id('status_2').inner_text() == 'Peruttu'
    #page.get_by_test_id('publish_2').click()
    #assert page.get_by_test_id('status_2').inner_text() == 'Ilmoittautuminen käynnissä'
