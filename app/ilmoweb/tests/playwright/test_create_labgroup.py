from playwright.sync_api import Page, expect
from helper_functions import login

def test_login_and_navigate_to_create_labgroup(page: Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.goto('/created_labs')
    page.locator('[data-testid="group_1"]').click()
    expect(page).to_have_title('Create group')


def test_create_labgroup_and_check_that_it_is_created(page: Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.goto('/created_labs')
    page.locator('[data-testid="group_1"]').click()
    page.get_by_test_id('date').fill('2025-10-31')
    page.keyboard.press('Shift')
    page.get_by_test_id('time').select_option('12-16')
    page.get_by_test_id('place').select_option('D210 (Phy)')
    page.locator('[data-testid="1"]').click()
    page.get_by_role('button', name='Luo labra').click()
    expect(page).to_have_title('Created labs')
    expect(page.get_by_role("cell", name="31.10.2025 klo 12 - 16"))
    expect(page.get_by_text('D210 (Phy)')).to_be_visible()
