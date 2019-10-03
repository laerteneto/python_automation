from base.base_page import BasePage
from maps.es_login_map import EsLoginMap


class EsLoginPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.es_login_map = EsLoginMap()

    """ Esse metodo realiza login no sistema ES
        
        @param username
        @param password
    """

    def Login(self, username, password):
        self.SendKeys("xpath", self.es_login_map.login_field, username)
        self.SendKeys("xpath", self.es_login_map.password_field, password)
        self.TakeScreenshot("Login step")
        self.ClickOn("xpath", self.es_login_map.login_button)

    """ Esse metodo verifica se o login foi realizado corretamente
        
        @param username
        @param password
    """

    def IsInScreen(self):
        message = self.WaitElement(locator_type="xpath", locator=self.es_login_map.login_message, timeout=50)
        return "Login was done!" in message.text
