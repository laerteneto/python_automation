class LoginMap():
    #locators
    _login_field = "//input[@id='username']"
    _password_field = "//input[@id='password']"
    _login_button = "//i[contains(text(),'Login')]"
    _logout_button = "//i[@class='icon-2x icon-signout']"
    _login_message = "//div[@id='flash']"
    _select_login = "//a[@href='/login']"