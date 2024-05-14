import time
import os

from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from pageObjects.LocatorsDashboard import DashboardAndTabs
from pageObjects.LocatorsLoginPage import LoginPage
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig


class Test_003_Dashboard_selection:
    baseURL = ReadConfig.getURL()
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()
    widget_name = 'Document Register'

    logger = LogGen.loggen()

    def test_dashboard_selection(self, setup,base_dir):
        self.path = os.path.join(base_dir, "TestData", "DataManager.xlsx")

        self.driver = setup
        self.driver.get(self.baseURL)
        self.lp = LoginPage(self.driver)
        time.sleep(5)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()
        time.sleep(10)
        dashboard = "GENERIC Dashboard"

        time.sleep(5)
        try:
            WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, "//span[@class='topbar-app-name']")))
            self.driver.find_element(By.XPATH,
                                     "//span[contains(@class,'topbar-app-name') and text()='" + dashboard + "']")
            # "//span[@title='" + self.dashboard_name + "']")
            time.sleep(5)
            try:
                WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                    (By.XPATH,
                     "//span[@class='fonticon fonticon-close new-dashboard-menu-close-btn']"))).click()
            except:
                pass
        except:
            try:
                # click on Dashboards and cockpit list menu
                WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//span[@class='wp-panel-button fonticon fonticon-menu new-dashboard-menu-open-btn inactive']"))).click()
                # self.logger.info("** clicked on Dashboard and cockpit list menu **")
                try:
                    WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                        (By.XPATH,
                         "//div[@class='dashboard-menu-list-item']//p[@class='dashboard-menu-list-item-text-title' and text()='" + dashboard + "']"))).click()
                    self.logger.info("** clicked on Dashboard **")
                except Exception as e:
                    self.logger.error("*** Fail to click on Dashboard: {}".format(str(e)))
            except:
                try:
                    WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                        (By.XPATH,
                         "//div[@class='dashboard-menu-list-item-text-with-description']/p[contains(@class, 'dashboard-menu-list-item-text-title') and text()='" + dashboard + "']"))).click()
                    # self.logger.info("** ** clicked on Dashboard ** **")
                    WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located(
                        (By.XPATH,
                         "//span[@class='fonticon fonticon-close new-dashboard-menu-close-btn']")))
                except Exception as e:
                    self.logger.error("exception {}".format(str(e)))

            WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH,
                 "//span[@class='fonticon fonticon-close new-dashboard-menu-close-btn']"))).click()
            WebDriverWait(self.driver, 5).until(expected_conditions.invisibility_of_element_located(
                (By.XPATH, "//span[@class='fonticon fonticon-close new-dashboard-menu-close-btn']")))

        self.dt = DashboardAndTabs(self.driver)
        time.sleep(5)
        self.dt.clickdocumentmgtab()
        self.logger.info("*** Navigated to document management tab ***")
        time.sleep(5)
        self.dt.clickworkflowmgtab()
        self.logger.info("*** Navigated to Workflow management tab ***")
        time.sleep(5)
        self.dt.clickmailmgtab()
        self.logger.info("*** Navigated to Mail management tab ***")
        time.sleep(5)
        self.dt.clickalltasksviewtab()
        self.logger.info("*** Navigated to All Task View tab ***")
        time.sleep(5)
        self.dt.clickprojectinsightstab()
        self.logger.info("*** Navigated to Project Insight tab ***")

        time.sleep(5)
        self.logger.info("*** Ended Navigate Dashboard Selection test ***")
