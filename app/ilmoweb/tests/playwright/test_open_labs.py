import re
from playwright.sync_api import Page, expect
from helper_functions import login

def test_has_title_and_heading(page: Page):
    login(page, 'kemianopiskelija', 'salasana123')
    expect(page).to_have_title(re.compile('Open Labs'))
    assert page.inner_html('h1 b') == 'Fysikaalisen kemian<br>ilmoittautumisjärjestelmä'

def test_laboratoriotyot_button(page: Page):
    login(page, 'kemianopiskelija', 'salasana123')
    page.get_by_role('link', name='Laboratoriotyöt').click()
    expect(page.get_by_role('heading', name='Avoimet labrat')).to_be_visible()
