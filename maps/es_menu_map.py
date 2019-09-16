class EsMenuMap:
    # locators
    login_button = "//button[@class='btn btn-default']"
    logout_button = "//i[@class='icon-2x icon-signout']"
    login_message = "//label[@title='Admin']"

    @classmethod
    def MenuElement(cls, text_menu):
        return "//span[contains(text(), '" + text_menu + "')]"

    @classmethod
    def SubMenuElement(cls, text_submenu):
        return "//a[text()='" + text_submenu + "']"
