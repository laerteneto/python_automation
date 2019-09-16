from base.base_page import BasePage
from maps.es_workflow_map import EsWorkflowMap


class EsWorkflowPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.es_workflow_map = EsWorkflowMap()

    """
    Validate a element in a screen in order to check if the script is in the expected screen
    """

    def ValidateWorkflowCreated(self):
        message = self.WaitElement(locator_type="xpath", locator=self.es_workflow_map.workflow_message, timeout=50)
        return "The screen is correct!" in message.text

    """
    Create a workflow when is in the "Gestao de Workflow" Page
    """

    def CreateWorkflow(self, name, sla, tmo, text_description, project):
        self.ClickOn("xpath", self.es_workflow_map.ButtonElement("Crear Workflow"))
        self.SendKeys("xpath", self.es_workflow_map.InputFieldById("Name"), name)
        self.SendKeys("xpath", self.es_workflow_map.InputFieldById("SLA"), sla)
        self.SendKeys("xpath", self.es_workflow_map.InputFieldById("TMO"), tmo)
        self.SendKeys("xpath", self.es_workflow_map.InputFieldByName("Descripción", "textarea"), text_description)
        self.SelectElementByText("xpath", self.es_workflow_map.SelectField("Proyecto"), project)
        self.ClickOn(locator=self.es_workflow_map.ButtonElement("Guardar"))
