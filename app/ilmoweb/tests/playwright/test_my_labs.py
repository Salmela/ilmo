from playwright.sync_api import Page, expect
from helper_functions import login

def test_teacher_can_grade_a_report(page: Page):
    login(page, 'kemianopiskelija', 'salasana123')
    page.goto('/open_labs')
    page.get_by_test_id('group_1').click()
    page.get_by_test_id('enroll_group_1').click()
    page.get_by_role('link', name='Kirjaudu ulos').click()

    login(page, 'chemstudent', 'password123')
    page.goto('/open_labs')
    page.get_by_test_id('group_1').click()
    page.get_by_test_id('enroll_group_1').click()
    page.get_by_role('link', name='Kirjaudu ulos').click()

    login(page, 'kemianope', 'atomi123')
    page.goto('/created_labs')
    page.get_by_test_id('confirm_1').click()
    expect(page.get_by_text('Ryhmä vahvistettu')).to_be_visible()
    page.get_by_role('link', name='Kirjaudu ulos').click()

    login(page, 'kemianopiskelija', 'salasana123')
    page.goto('/my_labs')
    expect(page.get_by_text('Palauta raportti')).to_be_visible()
    page.get_by_role('button', name='Palauta raportti').click()
    page.get_by_test_id('file_1').set_input_files('config/file.pdf')
    page.get_by_role('button', name='Tallenna').click()
    page.get_by_role('link', name='Kirjaudu ulos').click()

    login(page, 'kemianope', 'atomi123')
    page.goto('/returned_reports')

    page.get_by_test_id('open_1').click()
    page.get_by_test_id('select_grade').select_option('5')
    page.get_by_test_id('comment').fill('tämä on kommentti')
    page.get_by_test_id('file').set_input_files('config/comment.pdf')
    page.get_by_role('button', name='Arvostele').click()
    expect(page.get_by_test_id('status_1')).to_have_text('Arvosteltu (5/5)')

def test_teacher_can_send_a_report_back_to_be_fixed(page: Page):
    login(page, 'chemstudent', 'password123')
    page.goto('/my_labs')
    expect(page.get_by_text('Palauta raportti')).to_be_visible()
    page.get_by_role('button', name='Palauta raportti').click()
    page.get_by_test_id('file_1').set_input_files('config/file.pdf')
    page.get_by_role('button', name='Tallenna').click()
    page.get_by_role('link', name='Kirjaudu ulos').click()

    login(page, 'kemianope', 'atomi123')
    page.goto('/returned_reports')

    page.get_by_test_id('open_2').click()
    page.get_by_test_id('select_grade').select_option('Vaatii korjausta')
    page.get_by_test_id('comment').fill('tämä on kommentti')
    page.get_by_test_id('file').set_input_files('config/comment.pdf')
    page.get_by_role('button', name='Arvostele').click()
    expect(page.get_by_test_id('status_2')).to_have_text('Korjauksessa')

def test_login_and_navigate_to_my_labs(page: Page):
    page.goto('/')
    login(page, 'kemianopiskelija', 'salasana123')
    page.get_by_role('link', name='Omat labrat').click()
    expect(page.get_by_role('heading', name='Omat ilmoittautumiset')).to_be_visible()

def test_enrolled_group_is_visible_in_my_labs(page: Page):
    login(page, 'kemianopiskelija', 'salasana123')
    page.get_by_role('link', name='Omat labrat').click()
    expect(page.get_by_text('labra 1')).to_be_visible()

def test_student_can_check_graded_report_info(page: Page):
    login(page, 'kemianopiskelija', 'salasana123')
    page.get_by_role('link', name='Omat labrat').click()
    page.get_by_role('button', name='Avaa').click()
    expect(page.get_by_text('Raportti')).to_be_hidden()
    expect(page.get_by_text('tämä on kommentti')).to_be_visible()
    expect(page.get_by_role('link', name='comment.pdf')).to_be_visible()

def test_student_can_check_sent_to_fix_report_info(page: Page):
    login(page, 'chemstudent', 'password123')
    page.get_by_role('link', name='Omat labrat').click()
    page.get_by_role('button', name='Avaa').click()
    expect(page.get_by_role('link', name='file.pdf')).to_be_visible()
    expect(page.get_by_text('Kalle Kemisti')).to_be_visible()
    expect(page.get_by_text('Raportti vaatii korjausta')).to_be_visible()
    expect(page.get_by_text('tämä on kommentti')).to_be_visible()
    expect(page.get_by_role('link', name='comment.pdf')).to_be_visible()

def test_student_can_cancel_enrollment(page: Page):
    login(page, 'kemianopiskelija', 'salasana123')
    page.get_by_role('link', name='Laboratoriotyöt').click()
    page.get_by_test_id('group_7').click()
    page.get_by_test_id('enroll_group_7').click()
    page.get_by_role('link', name='Omat labrat').click()
    expect(page.get_by_text('Heisenberg')).to_be_visible()
    page.get_by_role('link', name='Laboratoriotyöt').click()
    page.get_by_test_id('group_7').click()
    page.get_by_role('link', name='Omat labrat').click()
    expect(page.get_by_text('Heisenberg')).to_be_hidden()

def test_labgroup_canceled_state_appearance(page: Page):
    login(page, 'chemstudent', 'password123')
    page.goto('/open_labs')
    page.get_by_test_id('group_9').click()
    page.get_by_test_id('enroll_group_9').click()
    page.get_by_role('link', name='Kirjaudu ulos').click()

    login(page, 'kemianope', 'atomi123')
    page.goto('/created_labs')
    page.get_by_test_id('confirm_9').click()
    page.goto('/created_labs')
    page.get_by_test_id('cancel_9').click()
    page.get_by_role('link', name='Kirjaudu ulos').click()

    login(page, 'chemstudent', 'password123')
    page.goto('/my_labs')
    expect(page.get_by_text('Labra peruttu')).to_be_visible()
