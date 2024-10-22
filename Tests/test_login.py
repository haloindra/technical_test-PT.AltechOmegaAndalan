import Data.user_data as user_data
import pytest
import os
import logging

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.login_linux
class TestLogin:

    @pytest.mark.positive_linux
    def test_positive_login(self):
        logger.info("Starting positive login test.")

        # Initialize ChromeOptions and set desired options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="130.0.6723.58").install()), options=chrome_options)

        # Log navigation to URL
        print(f"Navigating to URL: {user_data.URL}")
        driver.get(user_data.URL)
        driver.implicitly_wait(user_data.implicit_wait_time)

        # Log username input
        print(f"Entering Username: {user_data.STANDARD_USER}")
        username_locator = driver.find_element(By.ID, "user-name")
        username_locator.send_keys(user_data.STANDARD_USER)

        # Log password input
        print("Entering Password.")
        password_locator = driver.find_element(By.NAME, "password")
        password_locator.send_keys(user_data.STANDARD_PASSWORD)

        # Submit login
        print("Clicking Submit button.")
        submit_button_locator = driver.find_element(By.XPATH, "//input[@class='submit-button btn_action']")
        submit_button_locator.click()
        driver.implicitly_wait(user_data.implicit_wait_time)

        # Verify URL change
        actual_url = driver.current_url
        print(f"Expected URL: {user_data.home_url}, Actual URL: {actual_url}")
        assert actual_url == user_data.home_url, "Login failed!"

        # Verify successful login by checking for an element on the inventory page
        inventory_displayed = driver.find_element(By.ID, "inventory_container").is_displayed()
        print(f"Validation Pass: Inventory page is displayed: {inventory_displayed}")
        
        # Close browser
        driver.quit()

    @pytest.mark.negative_linux
    def test_negative_login(self):
        logger.info("Starting negative login test.")

        # Initialize ChromeOptions and set desired options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="130.0.6723.58").install()), options=chrome_options)

        # Log navigation to URL
        print(f"Navigating to URL: {user_data.URL}")
        driver.get(user_data.URL)
        driver.implicitly_wait(user_data.implicit_wait_time)

        # Log username input
        print(f"Entering Username: {user_data.LOCKED_OUT_USER}")
        username_locator = driver.find_element(By.ID, "user-name")
        username_locator.send_keys(user_data.LOCKED_OUT_USER)

        # Log password input
        print("Entering Password.")
        password_locator = driver.find_element(By.NAME, "password")
        password_locator.send_keys(user_data.STANDARD_PASSWORD)

        # Submit login
        print("Clicking Submit button.")
        submit_button_locator = driver.find_element(By.XPATH, "//input[@class='submit-button btn_action']")
        submit_button_locator.click()
        driver.implicitly_wait(user_data.implicit_wait_time)

        # Verify error message
        error_message_locator = driver.find_element(By.XPATH, "//div[@class='error-message-container error']")
        error_message_displayed = error_message_locator.is_displayed()
        print(f"Validation Pass: Error message is displayed: {error_message_displayed}")

        # Verify error message text
        error_message = error_message_locator.text
        expected_error_message = "Epic sadface: Sorry, this user has been locked out."
        print(f"Expected Error Message: '{expected_error_message}', Actual Error Message: '{error_message}'")
        assert error_message == expected_error_message, "Unexpected error message!"

        # Close browser
        driver.quit()
