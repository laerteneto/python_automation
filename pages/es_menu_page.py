from base.base_page import BasePage
from maps.es_login_map import EsLoginMap
from maps.es_menu_map import EsMenuMap


class EsMenuPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.es_login_map = EsLoginMap()
        self.menu_es = EsMenuMap()

        """
        ES - Click in the menu and in a submenu

        @:param menu_text: Name of the menu title
        @:param submenu_text: Name of the submenu title
        """

    def click_es_menu(self, menu_text, submenu_text):
        self.ClickOn("xpath", self.menu_es.MenuElement(menu_text))
        self.ClickOn("xpath", self.menu_es.SubMenuElement(submenu_text))

    """
    Check if the menu is in screen .
    NOTE: THIS METHOD IS NOT DONE. NEEDS TO CHECK THE "menu_message" MAP VARIABLE
    """
    def IsInScreen(self):
        message = self.WaitElement(locator_type="xpath", locator=self.menu_es.menu_message, timeout=50)
        return "Login was done!" in message.text
