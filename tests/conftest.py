from datetime import datetime

import pytest
import pytest_html
from selenium import webdriver
from werkzeug.security import safe_str_cmp

from config.evidence_gen import EvidenceGenerator

SCREENSHOT = 'screenshots/'

driver = None


def pytest_sessionstart(session):
    session.results = dict()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == 'call':
        item.session.results[item] = result


def pytest_sessionfinish(session, exitstatus):
    return sum(1 for result in session.results.values() if result.failed)


@pytest.yield_fixture(scope='function')
def BrowserSetUp(request, browser):
    global driver
    print("Running browser setUp")
    if safe_str_cmp(browser, 'firefox'):
        print("Tests will be executed on Firefox")
        driver = webdriver.Firefox()
    elif safe_str_cmp(browser, 'chrome'):
        print("Tests will be executed on Chrome")
        driver = webdriver.Chrome("config\\chromedriver.exe")
    driver.maximize_window()
    driver.implicitly_wait(20)

    if request.cls:
        request.cls.driver = driver
    yield driver


def pytest_addoption(parser):
    parser.addoption("--browser")
    parser.addoption("--osType", help="Operating system...")


@pytest.fixture(scope='session')
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope='session')
def osType(request):
    return request.config.getoption("--osType")


@pytest.fixture(scope='session')
def GenerateEvidence(request, scope='session'):
    import os
    pytest.time_start = datetime.now()
    pytest.time_start_format = "Test_Suit_Executed_At_" + pytest.time_start.strftime("%d_%m_%Y_%H_%M_%S")
    session = request.node
    yield
    result = "Failed" if sum(1 for result in session.results.values() if result.failed) > 0 else "Passed"
    pytest.time_end = datetime.now()
    pytest.time_end_format = pytest.time_end.strftime("%d_%m_%Y_%H_%M_%S")
    doc = EvidenceGenerator("Test Automation Framework",
                            str((pytest.time_end - pytest.time_start).seconds) + 's', result)
    TEST_DIR = SCREENSHOT + str(pytest.time_start_format)
    if not os.path.exists(TEST_DIR):
        os.makedirs(TEST_DIR, exist_ok=True)
    dirs = os.listdir(TEST_DIR)
    for subdir in dirs:
        evidences = os.listdir(TEST_DIR + '/' + subdir + '/')
        for e in evidences:
            doc.AddEvidence(subdir, e, TEST_DIR + '/' + subdir + '/' + e)
    doc.CreateDocument(TEST_DIR + '/' + "doc.docx")


def pytest_runtest_makereport(__multicall__, item):
    report = __multicall__.execute()
    extra = getattr(report, 'extra', [])
    if report.when == 'call':
        url = driver.current_url
        extra.append(pytest_html.extras.url(url))
        screenshot = driver.get_screenshot_as_base64()
        extra.append(pytest_html.extras.image(screenshot, 'Screenshot'))
        html = driver.page_source.encode('utf-8')
        extra.append(pytest_html.extras.text(html, 'HTML'))
        report.extra = extra
    return report
