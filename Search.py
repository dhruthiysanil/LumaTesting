"""
Automated Selenium script to login, search for a shirt, add it to the cart,
fill shipping details, and place an order.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import config1
import traceback  # To print full exception stack trace


# Start and configure Chrome WebDriver
def start_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver


# Perform login using credentials from config1
def login(driver, wait):
    driver.get(config1.LOGIN_URL)
    wait.until(EC.presence_of_element_located((By.ID, config1.SIGN_IN_EMAIL_INPUT))).send_keys(config1.EMAIL)
    driver.find_element(By.ID, config1.SIGN_IN_PASSWORD_INPUT).send_keys(config1.PASSWORD)
    driver.find_element(By.ID, config1.SIGN_IN_BUTTON).click()
    wait.until(EC.presence_of_element_located((By.ID, config1.SEARCH_INPUT_ID)))


# Search for a shirt and add to cart
def search_and_add_shirt(driver, wait):
    # Search for shirt
    search_box = wait.until(EC.presence_of_element_located((By.ID, config1.SEARCH_INPUT_ID)))
    search_box.clear()
    search_box.send_keys("shirt")
    search_box.submit()

    # Click product link
    wait.until(EC.element_to_be_clickable((By.XPATH, config1.RADIANT_TEE_XPATH))).click()
    driver.execute_script("window.scrollBy(0, 500);")

    # Select size, color
    wait.until(EC.element_to_be_clickable((By.ID, config1.SIZE_M_ID))).click()
    wait.until(EC.element_to_be_clickable((By.ID, config1.COLOR_BLUE_ID))).click()

    # Wait for "Add to Cart" span to be clickable
    add_to_cart_btn = wait.until(EC.element_to_be_clickable((By.XPATH, config1.ADD_TO_CART_XPATH)))
    driver.execute_script("arguments[0].click();", add_to_cart_btn)
    print(" Product added to cart.")


#Proceed to checkout
def proceed_to_checkout(driver, wait):
    print("Clicking cart icon to view minicart...")

    # Click on <a class='action showcart'> to open the minicart
    cart_icon = wait.until(EC.element_to_be_clickable((By.XPATH, config1.CART_ICON_XPATH)))
    driver.execute_script("arguments[0].click();", cart_icon)

    print("➡️ Clicking 'Proceed to Checkout' button...")
    try:
        checkout_btn = wait.until(EC.element_to_be_clickable((By.ID, config1.MINICART_CHECKOUT_BUTTON_ID)))
        driver.execute_script("arguments[0].click();", checkout_btn)
    except Exception as e:
        driver.save_screenshot("checkout_btn_error.png")
        raise Exception(" Could not click 'Proceed to Checkout' button.") from e




# Fill all shipping address details
def fill_shipping_details(driver, wait):
    wait.until(EC.url_contains("checkout/#shipping"))

    wait.until(EC.presence_of_element_located(config1.CHECKOUT_COMPANY_SELECTOR)).send_keys("NethraTech Pvt Ltd")
    wait.until(EC.presence_of_element_located(config1.CHECKOUT_STREET_SELECTOR)).send_keys("123 AI Street")
    wait.until(EC.presence_of_element_located(config1.CHECKOUT_CITY_SELECTOR)).send_keys("Bangalore")

    Select(wait.until(EC.element_to_be_clickable(config1.CHECKOUT_STATE_DROPDOWN_SELECTOR))).select_by_index(1)
    wait.until(EC.presence_of_element_located(config1.CHECKOUT_ZIP_SELECTOR)).send_keys("560001")
    Select(wait.until(EC.element_to_be_clickable(config1.CHECKOUT_COUNTRY_SELECTOR))).select_by_index(1)
    wait.until(EC.presence_of_element_located(config1.CHECKOUT_PHONE_SELECTOR)).send_keys("9844543210")

    wait.until(EC.element_to_be_clickable(config1.SHIPPING_METHOD_RADIO_XPATH)).click()
    wait.until(EC.element_to_be_clickable(config1.NEXT_BUTTON_XPATH)).click()


# Place the final order and wait for confirmation page
def place_order(driver, wait):
    wait.until(EC.url_contains("checkout/#payment"))
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "img[alt='Loading...']")))

    place_order_button = wait.until(EC.element_to_be_clickable(config1.PLACE_ORDER_BUTTON_XPATH))
    driver.execute_script("arguments[0].click();", place_order_button)

    wait.until(EC.url_to_be(config1.SUCCESS_PAGE_URL))


# Run the complete automation flow
def run_shirt_search_checkout():
    driver = start_driver()
    wait = WebDriverWait(driver, 20)

    try:
        login(driver, wait)
        search_and_add_shirt(driver, wait)
        proceed_to_checkout(driver, wait)
        fill_shipping_details(driver, wait)
        place_order(driver, wait)
        print(" Order placed successfully. Redirected to Thank You page.")
    except Exception as e:
        print(" Test failed:", e)
        traceback.print_exc()  # Print full error stack trace
    finally:
        driver.quit()


# Entry point
run_shirt_search_checkout()
