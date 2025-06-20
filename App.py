"""
register_only.py

This script automates the process of registering a user on a website using Selenium.
It opens the browser, navigates to the site, fills out the registration form,
and checks for success or failure messages.
"""
# register_only.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import WomenConfig
import os

# Credentials from environment variables
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# Start and configure the Chrome driver
def start_driver():
    """Initializes and returns a Chrome WebDriver with implicit wait and maximized window."""
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver

# Open the homepage of the website
def open_site(driver):
    """Navigates to the home URL defined in the config file."""
    driver.get(WomenConfig.HOME_URL)

# Fill and submit the registration form
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
        error = driver.find_element(By.CLASS_NAME, "message-error")
        print("Registration failed: Email already exists.")
    except:
        print("Account created successfully.")

# Main function to execute the registration test
def run_registration():
    """
    Controls the full registration flow:
    Starts the driver, opens the site, attempts registration,
    handles any exceptions, and ensures browser cleanup.
    """
    driver = start_driver()
    try:
        open_site(driver)
        register_account(driver)
    except Exception as e:
        print(f"Error during registration: {e}")
    finally:
        driver.quit()

# Run the registration test
run_registration()


def start_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver

def open_site(driver):
    driver.get(WomenConfig.HOME_URL)

def register_account(driver):
    driver.find_element(By.XPATH, WomenConfig.CREATE_ACCOUNT_LINK).click()
    driver.find_element(By.ID, WomenConfig.FIRST_NAME_INPUT).send_keys("Dhruthi")
    driver.find_element(By.ID, WomenConfig.LAST_NAME_INPUT).send_keys("Sanil")
    driver.find_element(By.ID, WomenConfig.EMAIL_INPUT).send_keys(EMAIL)
    driver.find_element(By.ID, WomenConfig.PASSWORD_INPUT).send_keys(PASSWORD)
    driver.find_element(By.ID, WomenConfig.CONFIRM_PASSWORD_INPUT).send_keys(PASSWORD)
    driver.find_element(By.XPATH, WomenConfig.CREATE_ACCOUNT_BUTTON).click()

    try:
        error = driver.find_element(By.CLASS_NAME, "message-error")
        print("Registration failed: Email already exists.")
    except:
        print("Account created successfully.")

def run_registration():
    driver = start_driver()
    try:
        open_site(driver)
        register_account(driver)
    except Exception as e:
        print(f"Error during registration: {e}")
    finally:
        driver.quit()

# Run the registration test
run_registration()
