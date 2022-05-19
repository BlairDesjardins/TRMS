from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


class SubmitRequestsPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def description(self):
        return self.driver.find_element(By.ID, 'descInput')

    def cost(self):
        return self.driver.find_element(By.ID, 'costInput')

    def location(self):
        return self.driver.find_element(By.ID, 'locationInput')

    def date(self):
        return self.driver.find_element(By.ID, 'dateInput')

    def time(self):
        return self.driver.find_element(By.ID, 'timeInput')

    def event_type(self):
        return self.driver.find_element(By.ID, 'eventInput')

    def submit(self):
        return self.driver.find_element(By.XPATH, '//*[@id="requests"]/table/tbody/tr[7]/td[2]/button')
