from playwright.sync_api import Page, expect
from helper_functions import login

def test_navigate_to_user_info(page: Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.get_by_test_id('user_info').click()
    expect(page).to_have_title('Omat tiedot')

def test_user_info_is_correct(page:Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.get_by_test_id('user_info').click()
    expect(page.get_by_test_id('name')).to_have_text('Kalle Kemisti')
    expect(page.get_by_test_id('student_id')).to_have_text('100012000')
    expect(page.get_by_test_id('email')).to_have_text('kemianope@ilmoweb.fi')

def test_user_can_change_their_email(page:Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.get_by_test_id('user_info').click()
    page.get_by_test_id('new_email').fill('testi.meili@ilmoweb.fi')
    page.get_by_test_id('change_email').click()
    expect(page.get_by_test_id('email')).to_have_text('testi.meili@ilmoweb.fi')

def test_teacher_cannot_see_achievements(page:Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.get_by_test_id('user_info').click()
    expect(page.get_by_text('Suoritukset')).to_be_hidden()

def test_student_can_see_graded_report(page:Page):
    page.goto('/')
    login(page, 'kemianopiskelija', 'salasana123')
    page.get_by_test_id('user_info').click()
    expect(page.get_by_text('Suoritukset')).to_be_visible()
    expect(page.get_by_test_id('lab_1')).to_have_text('labra 1')
    expect(page.get_by_test_id('grade_1')).to_have_text('5')

def test_student_can_see_ungraded_report(page:Page):
    page.goto('/')
    login(page, 'kemianopiskelija', 'salasana123')
    page.goto('/open_labs')
    page.get_by_test_id('group_7').click()
    page.get_by_test_id('enroll_group_7').click()
    page.get_by_role('link', name='Kirjaudu ulos').click()

    login(page, 'kemianope', 'atomi123')
    page.goto('/created_labs')
    page.get_by_test_id('confirm_7').click()
    page.get_by_role('link', name='Kirjaudu ulos').click()

    login(page, 'kemianopiskelija', 'salasana123')
    page.goto('/my_labs')
    page.get_by_test_id('return_7').click()
    page.get_by_test_id('file_7').set_input_files('config/file.pdf')
    page.get_by_role('button', name='Tallenna').click()

    page.get_by_test_id('user_info').click()
    expect(page.get_by_test_id('lab_3')).to_have_text('labra 1')
    expect(page.get_by_test_id('grade_3')).to_have_text('Odottaa arvostelua')
