import os
from datetime import datetime
from traceback import print_stack

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from werkzeug.security import safe_str_cmp
from exceptions.exceptions import ElementNotFoundException, ElementNotClickableException

import utilities.custom_logger as cl


class BasePage:
    """Cria a BasePage com diversas funções built in
    
        @param driver: instância do webdriver passada por parametro
    """
    log = cl.CustomLogger()

    def __init__(self, driver):
        self.driver = driver
        self.resultList = []

    def GetByType(self, locator_type):
        """Cria um objeto do tipo da busca a que o elemento vai ser submetido
    
        @param locator_type(str): tipo de localizador do elemento
        """
        locator_type = locator_type.lower()
        if safe_str_cmp(locator_type, "id"):
            return By.ID
        if safe_str_cmp(locator_type, "name"):
            return By.NAME
        if safe_str_cmp(locator_type, "xpath"):
            return By.XPATH
        else:
            self.log.info("Locator type " + locator_type + "not correct/support...")

    def TakeScreenshot(self, resultMessage):
        """Tira screenshot da tela e salva no diretório do teste
    
        @param resultMessage(str): parte do nome do arquivo
        """
        folder_name = os.path.join(str(pytest.time_start_format),
                                   os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0].split('___')[
                                       0] + '/')
        pytest.screenshotDirectory = os.path.join('screenshots/', folder_name)
        file_name = str(datetime.now().strftime("%H_%M_%S")) + '_' + resultMessage.replace(' ', '_') + '.png'
        final_file = pytest.screenshotDirectory + file_name
        try:
            if not os.path.exists(pytest.screenshotDirectory):
                os.makedirs(pytest.screenshotDirectory)
            self.driver.save_screenshot(final_file)
            self.log.info("Screenshot saved to: " + final_file)
        except:
            self.log.error("### Exception Ocurred")
            print_stack()

    def GetElement(self, locator_type="xpath", locator=""):
        """Espera e retorna o elemento

        @param locator_type(str): tipo de locator usado na busca
        @param locator(str): identificador do elemento
        """
        element = None
        try:
            by_type = self.GetByType(locator_type)
            element = self.WaitElement(locator=locator, locator_type=by_type, timeout=50)
            self.log.info("Element found...")
        except:
            self.log.info("Element not found...")
        return element

    def ClickOn(self, locator_type="xpath", locator=""):
        """Clica no elemento

        @param locator_type(str): tipo de locator usado na busca
        @param locator(str): identificador do elemento
        """
        try:
            element = self.GetElement(locator_type, locator)
            element.click()
            self.log.info("Clicked on : " + locator + " with locatorType: " + locator_type)
        except (ElementNotClickableException, ElementNotFoundException):
            print_stack()
            raise

    def SendKeys(self, locator_type="xpath", locator="", text=""):
        """Envia texto ao elemento

        @param locator_type(str): tipo de locator usado na busca
        @param locator(str): identificador do elemento
        @param text(str)
        """
        try:
            element = self.GetElement(locator_type, locator)
            element.send_keys(text)
            self.log.info("Keys sent to: " + locator + " with locatorType: " + locator_type)
        except ElementNotFoundException:
            self.log.info("Could not send keys to element: " + locator + " with locatorType: " + locator_type)
            print_stack()
            raise

    def SelectElementByText(self, locator_type="xpath", locator="", text=""):
        """Seleciona o elemento em um menu do tipo select pelo atributo texto    
        
        @param locator_type(str): tipo de locator usado na busca
        @param locator(str): identificador do elemento
        @param text(str)
        """
        try:
            element = self.GetElement(locator_type, locator)
            select = Select(element)
            select.select_by_visible_text(text)
            self.log.info("Selected element from menu: " + locator + " with locatorType: " + locator_type)
        except:
            self.log.info("Could not select element: " + locator + " with locatorType: " + locator_type)
            print_stack()

    def IsElementPresent(self, locator_type="xpath", locator=""):
        """Verifica se o elemento está presente. Retorna true caso esteja
        e false caso não.    
        
        @param locator_type(str): tipo de locator usado na busca
        @param locator(str): identificador do elemento
        """
        try:
            element = self.GetElement(locator_type, locator)
            if element:
                self.log.info("Element found...")
                return True
            else:
                self.log.info("Element not found...")
                return False
        except:
            self.log.info("Element not found...")
            return False

    def WaitElement(self, locator_type="xpath", locator="", timeout=10):
        """Espera o elemento ser exibido na tela pelo tempo definido pelo usuário    
        
        @param locator_type(str): tipo de locator usado na busca
        @param locator(str): identificador do elemento
        @param timeout(int): tempo máximo de espera
        """
        element = None
        try:
            by_type = self.GetByType(locator_type)
            self.log.info("Waiting for :: " + str(timeout) + " :: seconds for element")
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by_type, locator)))
        except:
            raise ElementNotFoundException(locator)

        return element

    def SetResult(self, result, result_message):
        """Seta o resultado de determinado teste e tira screenshot
        
        @param result(bool): resultado do teste
        @param result_message(str): mensagem de verificação
        """
        self.TakeScreenshot(result_message)
        try:
            if result:
                self.resultList.append("PASS")
                self.log.info("### VERIFICATION SUCCESSFULL:: " + result_message)

            else:
                self.resultList.append("FAIL")
                self.log.info("### VERIFICATION FAILED:: " + result_message)
        except:
            self.resultList.append("FAIL")
            self.log.info("### EXCEPTION OCCURRED:: " + result_message)

    def Mark(self, result, result_message):
        """Invoca set result. Novas ações serão implementadas
        
            @param result(bool): resultado do teste
            @param result_message(str): mensagem de verificação
        """
        self.SetResult(result, result_message)

    def MarkFinal(self, test_name, result, result_message):
        """Seta o resultado de determinado teste, tira screenshot e finaliza o teste
        
            @param result(bool): resultado do teste
            @param result_message(str): mensagem de verificação
        """
        self.SetResult(result, result_message)
        if "FAIL" in self.resultList:
            self.log.error(test_name + " ###TEST FAILED...")
            # self.resultList.clear()
            assert False
        else:
            self.log.info(test_name + " ###TEST SUCCESSFUL...")
            # self.resultList.clear()
            assert True

    """
    Go to a web page
    
    @:param url: url page to be accessed 
    """

    def GoToPage(self, url):
        self.driver.get(url)
