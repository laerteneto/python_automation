import utilities.custom_logger as cl


class ElementNotFoundException(Exception):
    log = cl.CustomLogger()

    def __init__(self, element):
        self.log.info("[Exceptions] - Element not found: " + str(element))


class ElementFoundException(Exception):
    log = cl.CustomLogger()

    def __init__(self, element):
        self.log.info("[Exceptions] - Element found: " + str(element))


class ElementNotClickableException(Exception):
    log = cl.CustomLogger()

    def __init__(self, locator, locator_type):
        self.log.info("[Exceptions] - Could not click on element: " + locator + " with locatorType: " + locator_type)


class SQLException(Exception):
    log = cl.CustomLogger()

    def __init__(self, query):
        self.log.info("[Exceptions] - Error while execution the sql query: " + str(query))
