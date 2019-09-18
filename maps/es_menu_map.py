class EsMenuMap:
    # locators
    login_button = "//button[@class='btn btn-default']"
    logout_button = "//i[@class='icon-2x icon-signout']"
    login_message = "//label[@title='Admin']"
    menu_message = ""

    """Estes métodos retornam elementos(str) dinamicamente"""

    @classmethod
    def MenuElement(cls, text_menu):
        return "//span[contains(text(), '" + text_menu + "')]"

    @classmethod
    def SubMenuElement(cls, text_submenu):
        return "//a[text()='" + text_submenu + "']"
