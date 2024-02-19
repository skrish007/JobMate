from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

class Logintest(LiveServerTestCase):

    def setUp(self):
        service = Service('C:\\Users\\s4shy\\Downloads\\geckodriver-v0.33.0-win64\\geckodriver.exe')
        self.driver = webdriver.Firefox(service=service)
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/login'  # Updated URL

    def tearDown(self):
        self.driver.quit()

    def fill_form(self, email='', password=''):
        driver = self.driver
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "email"))
        )
        driver.find_element(By.NAME, "email").send_keys(email)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        )
        driver.find_element(By.NAME, "password").send_keys(password)

    def test_correct_credentials_and_search(self):
        self.driver.get(self.live_server_url)
        self.fill_form(email="sobin@gmail.com", password="Sobin@123")
        self.driver.find_element(By.ID, "testid").click()
        # Add an assertion for successful login
        self.assertIn("userdash", self.driver.current_url)
        print("Test scenario 'Correct Credentials' passed.")

        # Wait for the element with ID 'seltest' to be clickable
        seltest_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "seltest"))
        )
        seltest_element.click()
        WebDriverWait(self.driver, 10).until(
            EC.title_contains("JLogin")
        )
        # Add an assertion for the redirected page with title 'Companies'
        print("Test scenario 'View Companies Page' passed.")
        time.sleep(5)

if __name__ == '__main__':
    LiveServerTestCase.main()
