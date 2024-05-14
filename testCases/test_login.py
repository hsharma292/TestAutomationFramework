import time
from pageObjects.LocatorsLoginPage import LoginPage
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen


class Test_001_Login:
    # get data from utility file to avoid above hard coded values in test file
    baseURL = ReadConfig.getURL()
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    # Use self keyword to access Class
    def test_homePageTitle(self, setup):

        self.logger.info("****************** Test_001_Login ******************")
        self.logger.info("************ Verifying Home Page Title ************")

        # driver is initialized in setup method in conftest as fixture and called here
        self.driver = setup
        self.driver.get(self.baseURL)
        act_title = self.driver.title
        print(act_title)
        if act_title == "3DPassport | Login - Dassault Systèmes":
            assert True
            self.driver.close()
            self.logger.info("********** Home page title test is passed ********")
        else:
            self.driver.save_screenshot(".\\Screenshots\\" + "test_homePageTitle.png")
            self.driver.close()
            self.logger.error("********** Home page title test is Failed ********")
            assert False

    def test_login(self, setup):
        self.logger.info("********** Verifying login test ********")
        self.driver = setup
        self.driver.get(self.baseURL)
        # create object of login class to access methods in it
        self.lp = LoginPage(self.driver)
        time.sleep(5)

        # call action methods by above created object
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()
        time.sleep(5)
        act_title = self.driver.title
        print(act_title)
        time.sleep(5)
        if act_title.__contains__("GENERIC Dashboard"):
            assert True
            self.logger.info("********** Login test is passed ********")
            self.driver.close()
        else:
            self.driver.save_screenshot(".\\Screenshots\\" + "test_login.png")
            self.driver.close()
            self.logger.error("********** Login test is Failed ********")
            assert False
