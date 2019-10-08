from datetime import datetime
import os
from config import Models
import pytest
from selenium import webdriver
from werkzeug.security import safe_str_cmp

from utilities.read_data import DataHandler

from config.evidence_gen import EvidenceGenerator

import glob


SCREENSHOT = 'screenshots/'

driver = None


def pytest_sessionstart(session):
    session.results = dict()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Metodo utilizado para geração automática de report
    """
    outcome = yield
    result = outcome.get_result()

    if result.when == 'call':
        item.session.results[item] = result
    print("Result:", result)


@pytest.yield_fixture(scope='function')
def BrowserSetUp(request, browser, webDriverWait):
    """
        Esse método cria o browser através do parâmetro informado pela linha de comando
        parâmetro: --browser chrome (ou firefox)
    """
    global driver
    print("Running browser setUp")
    if safe_str_cmp(browser, 'firefox'):
        print("Tests will be executed on Firefox")
        driver = webdriver.Firefox()
    elif safe_str_cmp(browser, 'chrome'):
        print("Tests will be executed on Chrome")
        driver = webdriver.Chrome(os.path.join("config", "chromedriver.exe"))
    driver.maximize_window()
    driver.implicitly_wait(webDriverWait)

    if request.cls:
        request.cls.driver = driver
    yield driver


"""
    Esses métodos auxiliam aos testes capturando a plataforma e browser informados
"""


def pytest_addoption(parser):
    parser.addoption("--browser")
    parser.addoption("--dataSource", help="GetCsvData, GetExcelData or GetGoogleData")
    parser.addoption("--webDriverWait", help="param: int -> for implicity wait")
    parser.addoption("--osType", help="Operating system...")


@pytest.fixture(scope='session')
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope='function')
def fileHandler(request):
    files = os.listdir(os.path.join(request.config.rootdir, 'temp/'))
    files = [os.path.join(request.config.rootdir, 'temp/', f) for f in files]
    for f in files:
        os.remove(f)


@pytest.fixture(scope='session')
def dataSource(request):
    op = request.config.getoption("--dataSource")
    if op == 'GetCsvData':
        pytest.dataFunction = DataHandler.GetCsvData
    elif op == 'GetExcelData':
        pytest.dataFunction = DataHandler.GetExcelData
    elif op == 'GetGoogleData':
        pytest.dataFunction = DataHandler.GetGoogleData


@pytest.fixture(scope='session')
def webDriverWait(request):
    return int(request.config.getoption("--webDriverWait"))


@pytest.fixture(scope='session')
def osType(request):
    return request.config.getoption("--osType")


@pytest.fixture(scope='session')
def GenerateEvidence(request, scope='session'):
    """
        Esse método gera o documento de report geral após a execução dos casos de teste
    """
    pytest.time_start = datetime.now()
    pytest.time_start_format = "Test_Suit_Executed_At_" + pytest.time_start.strftime("%d_%m_%Y_%H_%M_%S")
    session = request.node
    yield
    result = "Failed" if sum(1 for result in session.results.values() if result.failed) > 0 else "Passed"
    pytest.time_end = datetime.now()
    pytest.time_end_format = pytest.time_end.strftime("%d_%m_%Y_%H_%M_%S")
    doc = EvidenceGenerator("Test Automation Framework",
                            str((pytest.time_end - pytest.time_start).seconds) + 's', result)
    TEST_DIR = os.path.join(SCREENSHOT, str(pytest.time_start_format))
    if not os.path.exists(TEST_DIR):
        os.makedirs(TEST_DIR, exist_ok=True)
    dirs = os.listdir(TEST_DIR)
    for subdir in dirs:
        evidences = os.listdir(os.path.join(TEST_DIR, subdir))
        for e in evidences:
            doc.AddEvidence(subdir, e, os.path.join(TEST_DIR, subdir, e))
    doc.CreateDocument(os.path.join(TEST_DIR, "doc.docx"))


def pytest_sessionfinish(session, exitstatus):
    """
    Método que retorna a quantidade de falhas em uma execução de suíte de teste e guarda em um banco de dados
    """
    print()
    print('run status code:', exitstatus)
    passed_amount = sum(1 for result in session.results.values() if result.passed)
    failed_amount = sum(1 for result in session.results.values() if result.failed)
    print(f'there are {passed_amount} passed and {failed_amount} failed tests')
    db = Models.Database()
    suite_execution = Models.TestSuite(_suite_name=pytest.time_start_format, _passed_tests=passed_amount,
                                       _failed_tests=failed_amount, _suite_executed_at=pytest.time_start)
    db.session.add(suite_execution)
    db.session.commit()


"""
def pytest_runtest_makereport(__multicall__, item):
    '''
        Metodo 'built in' utilizado para geração automática de report
        criada pela comunidade.
        Adicionar parâmetro '--html=report.html' ao final da execução
        para que o pytest gere seu próprio, incluindo imagens.
    '''
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
"""
