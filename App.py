"""
register_only.py

This script automates the process of registering a user on a Magento demo site using Selenium.]
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import WomenConfig
import os

# Get credentials from environment variables
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def open_site(driver):
    """Navigates to the home URL defined in the config file."""
    driver.get(WomenConfig.HOME_URL)

def register_account(driver):
    """
    Automates account registration by filling out the form fields and clicking the register button.
    Prints whether the account was created or already exists.
    """
    driver.find_element(By.XPATH, WomenConfig.CREATE_ACCOUNT_LINK).click()
    driver.find_element(By.ID, WomenConfig.FIRST_NAME_INPUT).send_keys("Dhruthi")
    driver.find_element(By.ID, WomenConfig.LAST_NAME_INPUT).send_keys("Sanil")
    driver.find_element(By.ID, WomenConfig.EMAIL_INPUT).send_keys(EMAIL)
    driver.find_element(By.ID, WomenConfig.PASSWORD_INPUT).send_keys(PASSWORD)
    driver.find_element(By.ID, WomenConfig.CONFIRM_PASSWORD_INPUT).send_keys(PASSWORD)
    driver.find_element(By.XPATH, WomenConfig.CREATE_ACCOUNT_BUTTON).click()

    try:
        driver.find_element(By.CLASS_NAME, "message-error")
        print(" Registration failed: Email already exists.")
    except:
        print("✅ Account created successfully.")

def main():
    """Main entry point to execute the registration process."""
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()

    try:
        open_site(driver)
        register_account(driver)
    except Exception as e:
        print(f" Error during registration: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
