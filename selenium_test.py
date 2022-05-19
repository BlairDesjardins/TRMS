import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

from pages.home import HomePage
from pages.submit_requests import SubmitRequestsPage
from pages.view_requests import ViewRequestsPage

ser = Service('C:/Users/blair/PycharmProjects/TRMS/chromedriver.exe')
driver: WebDriver = webdriver.Chrome(service=ser)

home_page = HomePage(driver)
view_requests = ViewRequestsPage(driver)
submit_requests = SubmitRequestsPage(driver)


def _test():
    try:
        driver.get("file:///C:/Users/blair/Documents/Revature/TRMS-Client/index.html")
        time.sleep(3)
        home_page.email().send_keys("pete@email.com")
        home_page.password().send_keys("pw")
        home_page.login().click()
        time.sleep(3)
        view_requests.submit_nav_button().click()
        time.sleep(3)
        submit_requests.description().send_keys("Uni course blah blah")
        submit_requests.cost().send_keys("100")
        submit_requests.location().send_keys("123 place")
        submit_requests.date().send_keys("06152022")
        submit_requests.time().send_keys("1330")
        submit_requests.submit().click()
        time.sleep(3)

        assert "Request Successfully Added!" == driver.switch_to.alert.text
    except AssertionError:
        print(f"Test: Submit Request - Failed\n Actual text: {driver.switch_to.alert.text}")
    else:
        print("Test: Submit Request - Passed")
    finally:
        driver.quit()


if __name__ == '__main__':
    _test()
