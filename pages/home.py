from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


class HomePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def email(self):
        return self.driver.find_element(By.ID, 'email')

    def password(self):
        return self.driver.find_element(By.ID, 'password')

    def login(self):
        return self.driver.find_element(By.XPATH, '/html/body/div/div/button')
