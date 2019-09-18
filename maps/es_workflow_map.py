class EsWorkflowMap:
    # locators
    workflow_message = "//*[contains(text(),'Detalle del workflow')]"

    """Estes métodos retornam elementos(str) dinamicamente"""
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
