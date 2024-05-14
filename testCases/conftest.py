import os.path
import configparser
import pytest
from _pytest.config import Config
import pytest_html
from pytest_metadata.plugin import metadata_key
from selenium import webdriver
from pytest_html import extras
import time
import allure
from datetime import datetime
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen
import requests


@pytest.fixture(scope="session")
def base_dir():
    return ReadConfig.get_base_dir()


@pytest.fixture(scope="session")
def config_path(base_dir):
    return os.path.join(base_dir, 'Configurations', 'config.ini')


# @pytest.fixture(scope="session")
# def setup_logger(base_dir):
#     # Configure your logger here, potentially using base_dir for log file paths
#     log_path = os.path.join(base_dir, 'Logs', 'automation.log')
#     logger = LogGen.loggen()
#     return logger

@pytest.fixture(scope="session")
def config(base_dir, config_path):
    cfg = configparser.ConfigParser()
    cfg.read(config_path)
    return cfg


# to avoid creating/writing the driver (statement) in each step , we can add that step within this confstep file
# now we can use the "setup" keyword everywhere in place of "driver"

@pytest.fixture()
def setup(browser, request):  # Run test on desired browser
    if browser == 'chrome':
        driver = webdriver.Chrome()
        print("Launching Chrome Browser............")
        driver.maximize_window();
    elif browser == 'firefox':
        driver = webdriver.Firefox()
        print("Launching Firefox Browser............")
        driver.maximize_window();
    elif browser == 'edge':
        driver = webdriver.Edge()
        print("Launching Edge Browser............")
        driver.maximize_window();
    else:
        driver = webdriver.Chrome()
        print("Launching default Chrome Browser............")
        driver.maximize_window();

    # Teardown method
    def teardown():
        print("    Closing browser............")
        driver.quit()

    # Register the teardown function with request.addfinalizer()
    request.addfinalizer(teardown)

    return driver


# Now, to run tests on the desired browser, go to the “conftest.py” file and add the below-mentioned 2 methods,
# which will get the browser from the command line. So update below:
def pytest_addoption(parser):  # This will get the value from CLI / hooks
    parser.addoption("--browser")


# the upper method will get the browser value from the command line and put it in “browser” variable.
# Once the browser value is there, this “browser” value will be passed via browser() method below to the SetUp() method, that decides which browser it needs to launch.
@pytest.fixture()
def browser(request):  # This will return the browser value to setup method
    return request.config.getoption("--browser")


# this method returns the ‘browser’ value to Setup() method. Now, to make it work,
# add this “browser” variable as argument In Setup() method, followed by a condition statement.


################# Pytest HTML Report Generation #################

# It is hook for adding Environment info to HTML Report
def pytest_configure(config):
    metadata = config.pluginmanager.getplugin("metadata")
    if metadata:
        config.stash[metadata_key]['Project Name'] = 'feature\\Code_merge1'
        config.stash[metadata_key]['Module Name'] = 'Impararia'
        config.stash[metadata_key]['Tester'] = 'Impararia_Tester'


# It is hook for delete/Modify Environment info to HTML Report
@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    metadata.pop("JAVA_HOME", None)
    metadata.pop("Plugins", None)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # This will get the pytest test result status
    outcome = yield
    rep = outcome.get_result()
    # We only look at actual failing test calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        mode = "a" if hasattr(rep, "wasxfail") else "w"
        if "setup" in item.fixturenames:  # only if fixture has "setup"
            web_driver = item.funcargs["setup"]
            # Take screenshot and save in a dedicated directory
            web_driver.save_screenshot(f"screenshots/{rep.nodeid.replace('::', '_')}.png")


# @pytest.fixture(scope="function", autouse=True)
# def driver(request):
#     # Initialize WebDriver
#     driver = webdriver.Chrome()
#     yield driver
#     # Teardown WebDriver after test
#     driver.quit()
#
#
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        # Assume the fixture for the driver is named 'setup'
        if 'setup' in item.fixturenames:  # Check if 'setup' fixture is used in the test
            web_driver = item.funcargs['setup']
            screenshot_path = f"D:\\Git\\test-automation\\feature\\Code_merge1\\Screenshots\\screenshot_{item.nodeid.replace('::', '__')}.png"
            web_driver.save_screenshot(screenshot_path)

        # Check if extra attribute exists, if not, create it
        # if not hasattr(report, 'extra'):
        #     report.extra = []

        # Append an HTML image tag to the extra field
        # html = f"<div><img src='{screenshot_path}' alt='Screenshot' style='width:600px;height:300px;'/></div>"
        # report.extra.append(pytest_html.extras.html(html))

        # Add the screenshot path to the report's extra section
        # report.extra.append(pytest_html.extras.image(screenshot_path, 'Screenshot'))

        # Open the HTML report file in append mode
        with open("report.html", "a") as html_report:
            # Write the image tag directly to the HTML report
            html_report.write(
                f"<div><img src='{screenshot_path}' alt='Screenshot' style='width:600px;height:300px;'/></div>")
