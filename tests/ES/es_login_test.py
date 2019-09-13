import unittest
import pytest

from ddt import data, ddt, unpack
from pages.es_login_page import EsLoginPage
from utilities.read_data import GetCsvData


@pytest.mark.usefixtures("BrowserSetUp", "GenerateEvidence")
@ddt
class LoginTest(unittest.TestCase):
    @pytest.yield_fixture(autouse=True)
    def ClassSetup(self, BrowserSetUp):
        self.es_login_page = EsLoginPage(self.driver)
        yield
        self.driver.quit()

    @data(*GetCsvData('data\\es\\es_valid_login_test.csv'))
    @unpack
    def test_valid_login(self, url, username, password):
        self.es_login_page.GoToPage(url)
        self.es_login_page.Login(username, password)
        self.es_login_page.MarkFinal("es_test_valid_login", not self.es_login_page.IsInScreen(), "Login was successful")
