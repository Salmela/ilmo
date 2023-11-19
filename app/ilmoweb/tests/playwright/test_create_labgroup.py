from playwright.sync_api import Page, expect
from helper_functions import login

def test_login_and_navigate_to_create_labgroup(page: Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.get_by_test_id('course_1').click()
    expect(page).to_have_title('Create group')


def test_create_labgroup_and_check_that_it_is_created(page: Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.get_by_test_id('course_1').click()
    page.get_by_test_id('date').fill('2025-10-31')
    page.keyboard.press('Shift')
    page.get_by_test_id('start_time').fill('12:00')
    page.get_by_test_id('end_time').fill('16:00')
    page.get_by_test_id('place').select_option('D210 (Phy)')
    page.get_by_test_id('1').click()
    page.get_by_role('button', name='Luo labra').click()
    expect(page).to_have_title('Created labs')
    expect(page.get_by_role('cell', name='31.10.2025 klo 12 - 16'))
    expect(page.get_by_text('D210 (Phy)')).to_be_visible()

def test_delete_lab_group_and_check_it_is_deleted(page:Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.get_by_test_id('lab_group_12').click()
    page.get_by_test_id('delete_lab_group_12').click()
    expect(page.get_by_role('cell', name='31.10.2025 klo 12 - 16')).to_be_hidden()
    expect(page.get_by_text('D210 (Phy)')).to_be_hidden()
