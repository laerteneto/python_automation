import unittest
import pytest

from ddt import data, ddt, unpack
from pages.es_workflow_page import EsWorkflowPage
from pages.es_login_page import EsLoginPage
from utilities.read_data import GetCsvData
import os


@pytest.mark.usefixtures("BrowserSetUp", "GenerateEvidence")
@ddt
class CreateWorkflowTest(unittest.TestCase):
    @pytest.yield_fixture(autouse=True)
    def ClassSetup(self, BrowserSetUp):
        self.es_login_page = EsLoginPage(self.driver)
        self.es_workflow_page = EsWorkflowPage(self.driver)
        yield
        self.driver.quit()

    @data(*GetCsvData(os.path.join('data', 'es', 'es_create_workflow_test.csv')))
    @unpack
    def test_creat_workflow(self, url, username, password):
        self.es_workflow_page.GoToPage(url)
        self.es_login_page.Login(username, password)
        self.es_workflow_page.click_es_menu('Administración', "Workflow")
        self.es_workflow_page.CreateWorkflow("Workflow Ceara 9", "0000002", "0000007", "Melhor que tem",
                                             "Proyecto")

        self.es_workflow_page.MarkFinal("es_create_workflow_login", not self.es_workflow_page.ValidateWorkflowCreated(),
                                        "Workflow created")
