"""
Automated Selenium test script to:
- Register a new user (if not already registered)
- Log in with that user
- Navigate to the Magento homepage
- Access the 'Women' section
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

# User credentials
EMAIL = "dhruthi12@gmail.com"
PASSWORD = "DhruthiSanil@15"

# Start the Chrome driver
def start_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver

# Open the home page
def open_site(driver):
    driver.get(config.HOME_URL)

# Register a new account or handle existing email
def register_account(driver):
    driver.find_element(By.XPATH, config.CREATE_ACCOUNT_LINK).click()
    driver.find_element(By.ID, config.FIRST_NAME_INPUT).send_keys("Dhruthi")
    driver.find_element(By.ID, config.LAST_NAME_INPUT).send_keys("Sanil")
    driver.find_element(By.ID, config.EMAIL_INPUT).send_keys(EMAIL)
    driver.find_element(By.ID, config.PASSWORD_INPUT).send_keys(PASSWORD)
    driver.find_element(By.ID, config.CONFIRM_PASSWORD_INPUT).send_keys(PASSWORD)
    driver.find_element(By.XPATH, config.CREATE_ACCOUNT_BUTTON).click()

    # Check if account already exists
    try:
        error = driver.find_element(By.CLASS_NAME, "message-error")
        print(" Registration failed: Email already exists.")
    except:
        print(" Account created.")

# Log in to existing account
def login_account(driver):
    wait = WebDriverWait(driver, 15)
    driver.get(config.LOGIN_URL)
    print(" Navigated to Sign In page.")
    wait.until(EC.presence_of_element_located((By.ID, config.SIGN_IN_EMAIL_INPUT))).send_keys(EMAIL)
    driver.find_element(By.ID, config.SIGN_IN_PASSWORD_INPUT).send_keys(PASSWORD)
    wait.until(EC.element_to_be_clickable((By.ID, config.SIGN_IN_BUTTON))).click()

    welcome_msg = wait.until(EC.visibility_of_element_located((By.XPATH, config.WELCOME_MESSAGE_XPATH)))
    print(f"Login successful: {welcome_msg.text}")

# Verify if homepage is loaded
def verify_homepage(driver):
    driver.get(config.HOME_URL)
    assert "Home Page" in driver.title or "Magento" in driver.title, " Not on the Magento homepage"
    print(" Successfully navigated to the Magento Home Page.")



# Master test runner
def run_test():
    driver = start_driver()
    try:
        open_site(driver)
        register_account(driver)
        login_account(driver)
        verify_homepage(driver)
     
    except Exception as e:
        print(f" Test Failed: {e}")
    finally:
        driver.quit()

# Run the test
run_test()
