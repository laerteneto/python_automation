import unittest
import pytest

from ddt import data, ddt, unpack
from pages.es_workflow_page import EsWorkflowPage
from pages.es_login_page import EsLoginPage
from pages.es_menu_page import EsMenuPage
from utilities.read_data import DataHandler


@pytest.mark.usefixtures("BrowserSetUp", "GenerateEvidence")
@ddt
class CreateWorkflowTest(unittest.TestCase):
    @pytest.yield_fixture(autouse=True)
    def ClassSetup(self, BrowserSetUp):
        self.es_login_page = EsLoginPage(self.driver)
        self.es_workflow_page = EsWorkflowPage(self.driver)
        self.es_menu_page = EsMenuPage(self.driver)
        yield
        self.driver.quit()

    @data(*DataHandler.GetGoogleData('Automated Tests', 'es'))
    def test_export_import_workflow(self, info):
        # Login
        self.es_workflow_page.GoToPage(info['url'])
        self.es_login_page.Login(info['username'], info['password'])

        # Setup
        self.es_workflow_page.CreateWorkflow(info['workflow1'], info['sla'], info['tmo'], info['description'], info['project'])

        # Test
        self.es_workflow_page.ExportWorkflow(name_workflow_to_export=info['workflow1'])
        self.es_workflow_page.ImportWorkflowMainPage(project=info['project'], workflow_name=info['workflow2'])
        self.es_workflow_page.MarkFinal("test_export_import_workflow", True, "Workflow Imported")
