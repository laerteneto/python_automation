import unittest
import pytest

from ddt import data, ddt, unpack
from pages.login_page import LoginPage
from utilities.read_data import GetCsvData, GetExcelData, GetGoogleData
import os


@pytest.mark.usefixtures("BrowserSetUp", "GenerateEvidence")
@ddt
class LoginTest(unittest.TestCase):

    @pytest.yield_fixture(autouse=True)
    def ClassSetup(self, BrowserSetUp):
        self.loginPage = LoginPage(self.driver)
        yield
        self.driver.quit()

    @data(*GetGoogleData('Automated Tests','Teste'))
    @unpack
    def test_valid_login(self, url, username, password):
        self.loginPage.GoToPage(url)
        self.loginPage.SelectFromLogin("loginForm")
        self.loginPage.Login(username, password)
        self.loginPage.MarkFinal("test_valid_login", self.loginPage.IsLogged(), "Login was successful")
