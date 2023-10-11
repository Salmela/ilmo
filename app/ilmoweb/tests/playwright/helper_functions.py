def login(page, username, password):
    page.goto('/')
    page.get_by_role('button', name='Kirjaudu sisään').click()
    page.get_by_role('textbox', name='Username').fill(username)
    page.get_by_role('textbox', name='Password').fill(password)
    page.get_by_role('button', name='Log In').click()
