from werkzeug.security import safe_str_cmp

from base.base_page import BasePage


class LoginPage(BasePage):
    #locators
    _login_field = "//input[@id='username']"
    _password_field = "//input[@id='password']"
    _login_button = "//i[contains(text(),'Login')]"
    _logout_button = "//i[@class='icon-2x icon-signout']"
    _login_message = "//div[@id='flash']"
    _select_login = "//a[@href='/login']"


    def __init__(self, driver):
        super().__init__(driver)
    
    def Login(self, username, password):
        self.SendKeys("xpath", self._login_field, username)
        self.SendKeys("xpath", self._password_field, password)
        self.ClickOn("xpath", self._login_button)
    
    def SelectFromLogin(self, menu_option):
        if safe_str_cmp(menu_option, "loginForm"):
            self.ClickOn("xpath", self._select_login)
        
    def IsLogged(self):
        message = self.WaitElement(locatorType="xpath",locator=self._login_message,timeout=50)
        return "You logged into a secure area!" in message.text
    
    def goToPage(self, url):
        self.driver.get(url)
    