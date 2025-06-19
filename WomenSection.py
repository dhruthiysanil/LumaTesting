"""
Automated Selenium script for women's section checkout flow:
1. Log in to the website
2. Search for a shirt
3. Add it to the cart
4. Proceed to checkout
5. Fill in shipping details
6. Place the order and confirm success
"""

import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import config

def start_driver():
    """Initialize the Chrome WebDriver with necessary options."""
    options = Options()
    options.headless = False  # Set to True for headless mode
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver

def login(driver, wait):
    """Perform login using credentials from config."""
    print("Logging in...")
    driver.get(config.LOGIN_URL)
    wait.until(EC.presence_of_element_located((By.ID, config.SIGN_IN_EMAIL_INPUT))).send_keys(config.EMAIL)
    driver.find_element(By.ID, config.SIGN_IN_PASSWORD_INPUT).send_keys(config.PASSWORD)
    driver.find_element(By.ID, config.SIGN_IN_BUTTON).click()
    wait.until(EC.presence_of_element_located((By.ID, config.SEARCH_INPUT_ID)))
    print("Logged in successfully.")

def search_and_add_shirt(driver, wait):
    """Search for a shirt and add it to the cart."""
    print("Searching for shirt...")
    search_box = wait.until(EC.presence_of_element_located((By.ID, config.SEARCH_INPUT_ID)))
    search_box.clear()
    search_box.send_keys("shirt")
    search_box.submit()

    wait.until(EC.element_to_be_clickable((By.XPATH, config.RADIANT_TEE_XPATH))).click()
    driver.execute_script("window.scrollBy(0, 500);")

    wait.until(EC.element_to_be_clickable((By.ID, config.SIZE_M_ID))).click()
    wait.until(EC.element_to_be_clickable((By.ID, config.COLOR_BLUE_ID))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, config.ADD_TO_CART_XPATH))).click()
    print("Shirt added to cart.")

def proceed_to_checkout(driver, wait):
    """Open the minicart and proceed to checkout."""
    print("Opening cart and proceeding to checkout...")
    cart_button = wait.until(EC.element_to_be_clickable((By.XPATH, config.MY_CART_XPATH)))
    driver.execute_script("arguments[0].click();", cart_button)
    wait.until(EC.visibility_of_element_located((By.XPATH, config.VIEW_CART_XPATH))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, config.PROCEED_TO_CHECKOUT_CART_XPATH))).click()
    print("Reached checkout page.")

def fill_shipping_details(driver, wait):
    """Fill in all required shipping details in the checkout form."""
    print("Filling shipping details...")
    wait.until(EC.url_contains("checkout/#shipping"))

    wait.until(EC.presence_of_element_located(config.CHECKOUT_COMPANY_SELECTOR)).send_keys("NethraTech Pvt Ltd")
    wait.until(EC.presence_of_element_located(config.CHECKOUT_STREET_SELECTOR)).send_keys("123 AI Street")
    wait.until(EC.presence_of_element_located(config.CHECKOUT_CITY_SELECTOR)).send_keys("Bangalore")

    Select(wait.until(EC.element_to_be_clickable(config.CHECKOUT_STATE_DROPDOWN_SELECTOR))).select_by_index(1)
    wait.until(EC.presence_of_element_located(config.CHECKOUT_ZIP_SELECTOR)).send_keys("560001")
    Select(wait.until(EC.element_to_be_clickable(config.CHECKOUT_COUNTRY_SELECTOR))).select_by_index(1)
    wait.until(EC.presence_of_element_located(config.CHECKOUT_PHONE_SELECTOR)).send_keys("9844543210")

    wait.until(EC.element_to_be_clickable(config.SHIPPING_METHOD_RADIO_XPATH)).click()
    wait.until(EC.element_to_be_clickable(config.NEXT_BUTTON_XPATH)).click()
    print("Shipping details submitted.")

def place_order(driver, wait):
    """Place the final order and verify success page."""

    print("Placing order...")
    wait.until(EC.url_contains("checkout/#payment"))
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "img[alt='Loading...']")))

    place_order_button = wait.until(EC.element_to_be_clickable(config.PLACE_ORDER_BUTTON_XPATH))
    driver.execute_script("arguments[0].click();", place_order_button)

    wait.until(EC.url_to_be(config.SUCCESS_PAGE_URL))
    print("Order placed successfully. Redirected to Thank You page.")

def run_shirt_search_checkout():
    """Run the full shirt purchase test flow."""
    driver = start_driver()
    wait = WebDriverWait(driver, 20)
    try:
        login(driver, wait)
        search_and_add_shirt(driver, wait)
        proceed_to_checkout(driver, wait)
        fill_shipping_details(driver, wait)
        place_order(driver, wait)
    except Exception as e:
        print("Test failed:", e)
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == "__main__":
    run_shirt_search_checkout()
