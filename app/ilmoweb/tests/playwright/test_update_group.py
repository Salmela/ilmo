import re
from playwright.sync_api import Page, expect
from helper_functions import login

def test_navigate_to_update_group(page: Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.locator('[data-testid="group_1"]').click()
    expect(page).to_have_title(re.compile('Update group'))

def test_teacher_can_update_group(page: Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.locator('[data-testid="group_1"]').click()
    page.get_by_test_id('date').fill('2024-11-11')
    page.keyboard.press('Shift')
    page.get_by_test_id('time').select_option('8-12')
    page.get_by_test_id('place').select_option('B152')
    page.get_by_test_id('assistant').select_option('kemianassari')
    page.get_by_role('button', name='Päivitä labra').click()
    expect(page).to_have_title(re.compile('Created labs'))
    expect(page.locator('[data-testid="date_1"]')).to_have_text('11.11.2024 klo 8 - 12')
    expect(page.locator('[data-testid="place_1"]')).to_have_text('B152')
