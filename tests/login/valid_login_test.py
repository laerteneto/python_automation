import unittest
import pytest

from ddt import data, ddt
from pages.login_page import LoginPage
from utilities.read_data import DataHandler


@pytest.mark.usefixtures("BrowserSetUp", "GenerateEvidence")
@ddt
class LoginTest(unittest.TestCase):

    @pytest.yield_fixture(autouse=True)
    def ClassSetup(self, BrowserSetUp):
        self.loginPage = LoginPage(self.driver)
        yield
        self.driver.quit()

    @data(*DataHandler.GetGoogleData('Automated Tests', 'Login'))
    def test_valid_login(self, info):
        self.loginPage.GoToPage(info['url'])
        self.loginPage.SelectFromLogin("loginForm")
        self.loginPage.Login(info['username'], info['password'])
        self.loginPage.MarkFinal("test_valid_login", self.loginPage.IsLogged(), "Login was successful")
