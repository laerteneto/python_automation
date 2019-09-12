from base.base_page import BasePage
from werkzeug.security import safe_str_cmp

from maps.select_map import SelectMap


class SelectPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.select_map = SelectMap()
    
    def SelectFromLogin(self, menu_option):
        if safe_str_cmp(menu_option, "dropdown"):
            self.ClickOn("xpath", self.select_map._select_login)
    
    def Select(self, text):
        self.SelectElementByText('xpath',self.select_map._select_menu,text)
    
    def IsSelected(self,text):
        return safe_str_cmp(text,self.GetElement('xpath', self.select_map._select_menu).text)