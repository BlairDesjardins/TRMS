from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


class ViewRequestsPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def submit_nav_button(self):
        return self.driver.find_element(By.XPATH, '/html/body/ul/li[3]/a')
