"""
Automated Selenium script to:
1. Log in to an e-commerce site
2. Search for a shirt
3. Add it to the cart
4. Proceed to checkout
5. Fill in shipping details
6. Place the order and confirm success
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import config
import traceback  # For full exception trace

# Start Chrome driver with options
def start_driver():
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.headless = False  # Show browser for debugging
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver

# Log in to the website using credentials
def login(driver, wait):
    print(" Logging in...")
    driver.get(config.LOGIN_URL)
    wait.until(EC.presence_of_element_located((By.ID, config.SIGN_IN_EMAIL_INPUT))).send_keys(config.EMAIL)
    driver.find_element(By.ID, config.SIGN_IN_PASSWORD_INPUT).send_keys(config.PASSWORD)
    driver.find_element(By.ID, config.SIGN_IN_BUTTON).click()
    wait.until(EC.presence_of_element_located((By.ID, config.SEARCH_INPUT_ID)))
    print(" Logged in successfully.")

# Search for a shirt and add it to cart
def search_and_add_shirt(driver, wait):
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
    print(" Shirt added to cart.")

# Go to cart and start checkout process
def proceed_to_checkout(driver, wait):
    print(" Opening cart and proceeding to checkout...")
    cart_button = wait.until(EC.element_to_be_clickable((By.XPATH, config.MY_CART_XPATH)))
    driver.execute_script("arguments[0].click();", cart_button)
    wait.until(EC.visibility_of_element_located((By.XPATH, config.VIEW_CART_XPATH))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, config.PROCEED_TO_CHECKOUT_CART_XPATH))).click()
    print(" Reached checkout page.")

# Fill in shipping information
def fill_shipping_details(driver, wait):
    print(" Filling shipping details...")
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
    print(" Shipping details submitted.")

# Place the order and verify the confirmation page
def place_order(driver, wait):
    print("Placing order...")
    wait.until(EC.url_contains("checkout/#payment"))
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "img[alt='Loading...']")))

    place_order_button = wait.until(EC.element_to_be_clickable(config.PLACE_ORDER_BUTTON_XPATH))
    driver.execute_script("arguments[0].click();", place_order_button)

    wait.until(EC.url_to_be(config.SUCCESS_PAGE_URL))
    print(" Order placed successfully. Redirected to Thank You page.")

# Run the complete test: login → search → checkout → place order
def run_shirt_search_checkout():
    driver = start_driver()
    wait = WebDriverWait(driver, 20)

    try:
        login(driver, wait)
        search_and_add_shirt(driver, wait)
        proceed_to_checkout(driver, wait)
        fill_shipping_details(driver, wait)
        place_order(driver, wait)
    except Exception as e:
        print(" Test failed:", e)
        traceback.print_exc()
    finally:
        driver.quit()

# Entry point
run_shirt_search_checkout()
