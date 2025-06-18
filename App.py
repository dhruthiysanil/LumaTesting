# register_only.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

EMAIL = "code200@gmail.com"
PASSWORD = "DhruthiSanil@15"

def start_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver

def open_site(driver):
    driver.get(config.HOME_URL)

def register_account(driver):
    driver.find_element(By.XPATH, config.CREATE_ACCOUNT_LINK).click()
    driver.find_element(By.ID, config.FIRST_NAME_INPUT).send_keys("Dhruthi")
    driver.find_element(By.ID, config.LAST_NAME_INPUT).send_keys("Sanil")
    driver.find_element(By.ID, config.EMAIL_INPUT).send_keys(EMAIL)
    driver.find_element(By.ID, config.PASSWORD_INPUT).send_keys(PASSWORD)
    driver.find_element(By.ID, config.CONFIRM_PASSWORD_INPUT).send_keys(PASSWORD)
    driver.find_element(By.XPATH, config.CREATE_ACCOUNT_BUTTON).click()

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
