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
    @unpack
    def test_export_import_workflow(self, url, username, password, workflow1, workflow2, sla, tmo, description,
                                    project):
        # Login
        self.es_workflow_page.GoToPage(url)
        self.es_login_page.Login(username, password)

        # Setup
        self.es_workflow_page.CreateWorkflow(workflow1, sla, tmo, description, project)

        # Test
        self.es_workflow_page.ExportWorkflow(name_workflow_to_export=workflow1)
        self.es_workflow_page.ImportWorkflowMainPage(project=project, workflow_name=workflow2)
        self.es_workflow_page.MarkFinal("test_export_import_workflow", True, "Workflow Imported")
