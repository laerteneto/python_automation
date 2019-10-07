from base.base_page import BasePage
from maps.es_workflow_map import EsWorkflowMap
from pages.es_menu_page import EsMenuPage
from utilities.FilesManipulator import FilesManipulator
import time


class EsWorkflowPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.es_workflow_map = EsWorkflowMap()
        self.es_menu_page = EsMenuPage(self.driver)

    """
    Filter for searching something
    """

    def FilterSearch(self, id_workflow="", name=""):
        self.ClickOn(locator=self.es_workflow_map.ButtonElement("Filtro"))
        self.SendKeys(locator=self.es_workflow_map.InputFieldByName("Tarea", "input"), text=id_workflow)
        self.SendKeys(locator=self.es_workflow_map.InputFieldByName("Nombre", "input"), text=name)
        self.ClickOn(locator=self.es_workflow_map.ButtonElement("Búsqueda"))

    def GearClick(self, button_name):
        self.ClickOn(locator=self.es_workflow_map.GearClosed())
        self.ClickOn(locator=self.es_workflow_map.GearItem(button_name))

    """
    Create a workflow when is in the "Gestao de Workflow" Page
    """

    def CreateWorkflow(self, workflow_name, sla, tmo, text_description, project):
        self.es_menu_page.click_es_menu('Administración', "Workflow")
        self.ClickOn("xpath", self.es_workflow_map.ButtonElement("Crear Workflow"))
        self.SendKeys("xpath", self.es_workflow_map.InputFieldById("Name"), workflow_name)
        self.SendKeys("xpath", self.es_workflow_map.InputFieldById("SLA"), sla)
        self.SendKeys("xpath", self.es_workflow_map.InputFieldById("TMO"), tmo)
        self.SendKeys("xpath", self.es_workflow_map.InputFieldByName("Descripción", "textarea"), text_description)
        self.SelectElementByText("xpath", self.es_workflow_map.SelectField("Proyecto"), project)
        self.ClickOn(locator=self.es_workflow_map.ButtonElement("Guardar"))
        self.IsElementPresent(locator=self.es_workflow_map.ValidateMessage("Detalle del workflow"))
        self.TakeScreenshot("Workflow created")

    def ExportWorkflow(self, name_workflow_to_export=""):
        self.es_menu_page.click_es_menu('Administración', "Workflow")
        self.FilterSearch(name=name_workflow_to_export)
        self.GearClick("Exportación")
        time.sleep(0.2)  # To assure the download
        self.ClickOn(locator=self.es_workflow_map.ModalButton("Exportación"))
        time.sleep(2)  # To assure the download
        self.TakeScreenshot("Workflow exported")

    def ImportWorkflowMainPage(self, project, workflow_name):
        self.es_menu_page.click_es_menu('Administración', "Workflow")
        self.ClickOn("xpath", self.es_workflow_map.ButtonElement("Importación"))
        self.SelectElementByText("xpath", self.es_workflow_map.ModalSelectById("projects"), project)
        self.SendKeys("xpath", self.es_workflow_map.InputFieldById("nameWorkflow"), workflow_name)
        self.SendKeys("xpath", self.es_workflow_map.InputFieldById("upload"),
                      FilesManipulator.SelectLastModifiedFileInPath())
        self.ClickOn(locator=self.es_workflow_map.ModalButtonById("btn-importation"))
        self.IsElementPresent(locator=self.es_workflow_map.ValidateMessage("El nuevo flujo de trabajo creado."))
        self.TakeScreenshot("Workflow imported")
