"""
Magento Shirt Purchase Automation Script

This script automates:
1. Logging into the Magento demo site
2. Searching for a shirt
3. Adding the shirt to the cart
4. Proceeding to checkout
5. Filling shipping details
6. Placing an order and verifying success

All credentials and selectors are stored in `SearchConfig.py`.
"""

import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import SearchConfig


def login(driver, wait):
    """Log into Magento site using credentials from config."""
    driver.get(SearchConfig.LOGIN_URL)
    wait.until(
        EC.presence_of_element_located((By.ID, SearchConfig.SIGN_IN_EMAIL_INPUT))
    ).send_keys(SearchConfig.EMAIL)
    driver.find_element(By.ID, SearchConfig.SIGN_IN_PASSWORD_INPUT).send_keys(
        SearchConfig.PASSWORD
    )
    driver.find_element(By.ID, SearchConfig.SIGN_IN_BUTTON).click()
    wait.until(EC.presence_of_element_located((By.ID, SearchConfig.SEARCH_INPUT_ID)))
    print("Logged in successfully")


def search_and_add_shirt(driver, wait):
    """Search for a shirt, select attributes, and add to cart."""
    search_box = wait.until(
        EC.presence_of_element_located((By.ID, SearchConfig.SEARCH_INPUT_ID))
    )
    search_box.clear()
    search_box.send_keys("shirt")
    search_box.submit()

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, SearchConfig.RADIANT_TEE_XPATH))).click()
    driver.execute_script("window.scrollBy(0, 500);")

    wait.until(EC.element_to_be_clickable((By.ID, SearchConfig.SIZE_M_ID))).click()
    wait.until(EC.element_to_be_clickable((By.ID, SearchConfig.COLOR_BLUE_ID))).click()

    add_to_cart_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, SearchConfig.ADD_TO_CART_XPATH))
    )
    driver.execute_script("arguments[0].click();", add_to_cart_btn)

    print("Product added to cart.")


def proceed_to_checkout(driver, wait):
    """Open minicart and click 'Proceed to Checkout'."""
    cart_icon = wait.until(
        EC.element_to_be_clickable((By.XPATH, SearchConfig.CART_ICON_XPATH))
    )
    driver.execute_script("arguments[0].click();", cart_icon)

    try:
        checkout_btn = wait.until(
            EC.element_to_be_clickable((By.ID, SearchConfig.MINICART_CHECKOUT_BUTTON_ID))
        )
        driver.execute_script("arguments[0].click();", checkout_btn)
        print("Proceeded to checkout")
    except TimeoutError as err:
        driver.save_screenshot("checkout_btn_error.png")
        raise RuntimeError("Could not click 'Proceed to Checkout'") from err


def fill_shipping_details(driver, wait):
    """Fill all required shipping details and continue."""
    wait.until(EC.url_contains("checkout/#shipping"))

    wait.until(
        EC.presence_of_element_located(SearchConfig.CHECKOUT_COMPANY_SELECTOR)
    ).send_keys("NethraTech Pvt Ltd")
    wait.until(
        EC.presence_of_element_located(SearchConfig.CHECKOUT_STREET_SELECTOR)
    ).send_keys("123 AI Street")
    wait.until(
        EC.presence_of_element_located(SearchConfig.CHECKOUT_CITY_SELECTOR)
    ).send_keys("Bangalore")

    Select(wait.until(
        EC.element_to_be_clickable(SearchConfig.CHECKOUT_STATE_DROPDOWN_SELECTOR))
    ).select_by_index(1)
    wait.until(
        EC.presence_of_element_located(SearchConfig.CHECKOUT_ZIP_SELECTOR)
    ).send_keys("560001")
    Select(wait.until(
        EC.element_to_be_clickable(SearchConfig.CHECKOUT_COUNTRY_SELECTOR))
    ).select_by_index(1)
    wait.until(
        EC.presence_of_element_located(SearchConfig.CHECKOUT_PHONE_SELECTOR)
    ).send_keys("9844543210")

    wait.until(
        EC.element_to_be_clickable(SearchConfig.SHIPPING_METHOD_RADIO_XPATH)
    ).click()
    wait.until(
        EC.element_to_be_clickable(SearchConfig.NEXT_BUTTON_XPATH)
    ).click()

    print("Shipping details filled")


def place_order(driver, wait):
    """Click 'Place Order' and verify redirection to success page."""
    wait.until(EC.url_contains("checkout/#payment"))
    wait.until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "img[alt='Loading...']"))
    )

    place_order_btn = wait.until(
        EC.element_to_be_clickable(SearchConfig.PLACE_ORDER_BUTTON_XPATH)
    )
    driver.execute_script("arguments[0].click();", place_order_btn)

    wait.until(EC.url_to_be(SearchConfig.SUCCESS_PAGE_URL))
    print("🎉 Order placed successfully!")


def main():
    """Run the complete purchase flow."""
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    wait = WebDriverWait(driver, 20)

    try:
        login(driver, wait)
        search_and_add_shirt(driver, wait)
        proceed_to_checkout(driver, wait)
        fill_shipping_details(driver, wait)
        place_order(driver, wait)
    except Exception as err:
        print("Test failed:", err)
        traceback.print_exc()
    finally:
        input("Press Enter to exit and close browser...")
        driver.quit()


if __name__ == "__main__":
    main()
