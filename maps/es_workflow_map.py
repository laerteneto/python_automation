class EsWorkflowMap:
    """Estes métodos retornam elementos(str) dinamicamente"""

    @classmethod
    def ValidateMessage(cls, text_to_validate):
        return "//*[contains(text(),'" + text_to_validate + "')]"

    @classmethod
    def ButtonElement(cls, name_button):
        return "//*[contains(text(), '" + name_button + "')]"

    @classmethod
    def InputFieldByName(cls, field_name, field_type):
        return "//label[contains(text(), '" + field_name + "')]/following-sibling::" + field_type + ""

    @classmethod
    def InputFieldById(cls, field_id):
        return "//input[@id='" + field_id + "']"

    @classmethod
    def SelectField(cls, text_select):
        return "//label[contains(text(), '" + text_select + "')]/following-sibling::select"

    ### MODAL ####
    @classmethod
    def ModalButton(cls, button_name):
        return "//div[@class='modal-content']//button[contains(text(), '" + button_name + "')]"

    @classmethod
    def ModalButtonById(cls, button_id):
        return "//div[@class='modal-content']//*[@id='" + button_id + "']"

    @classmethod
    def ModalSelectById(cls, project_id):
        return "//div[@class='modal-content']//select[@id='" + project_id + "']"

    ###### Gear Map ######
    @classmethod
    def GearClosed(cls):
        return "//div[@class='btn-group']"

    @classmethod
    def GearItem(cls, name_item):
        return "//div[@class='btn-group open']//a[contains(text(), '" + name_item + "')]"

    ###### Alert Messages #####
    @classmethod
    def SuccessMessage(cls, message_text):
        return "//div[@class='alert alert-success text-center' and contains(text(), '" + message_text + "')]"
