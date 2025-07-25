"""
register_only.py

This script automates the process of registering a user on a Magento demo site using Selenium.
"""
#This code is part of a test suite for the WomenConfig module, which contains configuration details for the Magento demo site.
#This are the steps
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import WomenConfig
import os

# Load environment variables from .env file
load_dotenv()

# Read credentials from environment
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def open_site(driver):
    """Navigate to the homepage."""
    driver.get(WomenConfig.HOME_URL)

def register_account(driver):
    """Fill out the registration form and handle any registration result."""
    driver.find_element(By.XPATH, WomenConfig.CREATE_ACCOUNT_LINK).click()
    driver.find_element(By.ID, WomenConfig.FIRST_NAME_INPUT).send_keys("Dhruthi")
    driver.find_element(By.ID, WomenConfig.LAST_NAME_INPUT).send_keys("Sanil")
    driver.find_element(By.ID, WomenConfig.EMAIL_INPUT).send_keys(EMAIL)
    driver.find_element(By.ID, WomenConfig.PASSWORD_INPUT).send_keys(PASSWORD)
    driver.find_element(By.ID, WomenConfig.CONFIRM_PASSWORD_INPUT).send_keys(PASSWORD)
    driver.find_element(By.XPATH, WomenConfig.CREATE_ACCOUNT_BUTTON).click()

    try:
        driver.find_element(By.CLASS_NAME, "message-error")
        print("Registration failed: Email already exists.")
    except:
        print("Account created successfully.")

def main():
    """Run the registration test end-to-end."""
    if not EMAIL or not PASSWORD:
        print("EMAIL or PASSWORD not set in the .env file.")
        return

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.maximize_window()

    try:
        open_site(driver)
        register_account(driver)
    except Exception as e:
        print(f"Error during registration: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
