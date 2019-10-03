from werkzeug.security import safe_str_cmp

from base.base_page import BasePage
from maps.login_map import LoginMap


class LoginPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.login_map = LoginMap()

    def Login(self, username, password):
        self.SendKeys("xpath", self.login_map.login_field, username)
        self.SendKeys("xpath", self.login_map.password_field, password)
        self.ClickOn("xpath", self.login_map.login_button)

    def SelectFromLogin(self, menu_option):
        if safe_str_cmp(menu_option, "loginForm"):
            self.ClickOn("xpath", self.login_map.select_login)

    def IsLogged(self):
        message = self.WaitElement(locator_type="xpath", locator=self.login_map.login_message, timeout=50)
        return "You logged into a secure area!" in message.text

    def GoToPage(self, url):
        self.driver.get(url)
