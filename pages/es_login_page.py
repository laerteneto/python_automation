from werkzeug.security import safe_str_cmp

from base.base_page import BasePage
from maps.es_login_map import EsLoginMap


class EsLoginPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.es_login_map = EsLoginMap()

    def Login(self, username, password):
        self.SendKeys("xpath", self.es_login_map.login_field, username)
        self.SendKeys("xpath", self.es_login_map.password_field, password)
        self.ClickOn("xpath", self.es_login_map.login_button)

    def IsInScreen(self):
        message = self.WaitElement(locator_type="xpath", locator=self.es_login_map.login_message, timeout=50)
        return "Login was done!" in message.text
