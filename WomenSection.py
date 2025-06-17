from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config


def start_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver


def login(driver, wait):
    driver.get(config.LOGIN_URL)
    print("Navigated to Login page.")

    email = wait.until(EC.presence_of_element_located((By.ID, config.SIGN_IN_EMAIL_INPUT)))
    email.send_keys(config.EMAIL)

    password = driver.find_element(By.ID, config.SIGN_IN_PASSWORD_INPUT)
    password.send_keys(config.PASSWORD)

    driver.find_element(By.ID, config.SIGN_IN_BUTTON).click()
    wait.until(EC.presence_of_element_located((By.XPATH, config.WOMEN_TAB_XPATH)))
    print("Login successful.")


def add_breathe_easy_tank(driver, wait):
    driver.find_element(By.XPATH, config.WOMEN_TAB_XPATH).click()
    print("Navigated to Women section.")

    wait.until(EC.element_to_be_clickable((By.XPATH, config.PRODUCT_LINK_XPATH))).click()
    print("Opened Breathe-Easy Tank page.")

    driver.execute_script("window.scrollBy(0, 500);")
    wait.until(EC.element_to_be_clickable((By.XPATH, config.SIZE_S_XPATH))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, config.COLOR_YELLOW_XPATH))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, config.ADD_TO_CART_XPATH))).click()
    print("Added Breathe-Easy Tank to cart.")


def search_and_add_radiant_tee(driver, wait):
    search_box = wait.until(EC.presence_of_element_located((By.ID, config.SEARCH_INPUT_ID)))
    search_box.clear()
    search_box.send_keys("shirt")
    search_box.submit()
    print("Searched for 'shirt'.")

    wait.until(EC.element_to_be_clickable((By.XPATH, config.RADIANT_TEE_XPATH))).click()
    driver.execute_script("window.scrollBy(0, 500);")
    wait.until(EC.element_to_be_clickable((By.ID, config.SIZE_M_ID))).click()
    wait.until(EC.element_to_be_clickable((By.ID, config.COLOR_BLUE_ID))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, config.ADD_TO_CART_XPATH))).click()
    print("Added Radiant Tee to cart.")


def open_cart_and_checkout(driver, wait):
    cart_button = wait.until(EC.element_to_be_clickable((By.XPATH, config.MY_CART_XPATH)))
    driver.execute_script("arguments[0].click();", cart_button)
    print("Opened My Cart.")

    view_cart = wait.until(EC.element_to_be_clickable((By.XPATH, config.VIEW_CART_XPATH)))
    view_cart.click()
    print("Clicked View and Edit Cart.")

    proceed_checkout = wait.until(EC.element_to_be_clickable((By.XPATH, config.PROCEED_TO_CHECKOUT_CART_XPATH)))
    proceed_checkout.click()
    print("Clicked Proceed to Checkout.")


def fill_checkout_address(driver, wait):
    company_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, config.COMPANY_INPUT_SELECTOR)))
    company_input.send_keys("OpenAI Solutions")

    street_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, config.STREET_ADDRESS_SELECTOR)))
    street_input.send_keys("123 AI Lane")

    city_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, config.CITY_INPUT_SELECTOR)))
    city_input.send_keys("Bangalore")

    print("Filled Company, Street Address, and City.")



def test_add_products_checkout():
    driver = start_driver()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver, wait)
        add_breathe_easy_tank(driver, wait)
        search_and_add_radiant_tee(driver, wait)
        open_cart_and_checkout(driver, wait)
        fill_checkout_address(driver, wait)
        print(" Test completed successfully.")
    except Exception as e:
        print(" Test Failed:", e)
    finally:
        driver.quit()


# Run the test
test_add_products_checkout()
