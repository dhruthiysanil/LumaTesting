"""
Automated Selenium script to:
- Log in to the Magento website
- Search and add a shirt to the cart (select size and color)
- Proceed to checkout
- Fill in shipping details
- Place the order and confirm success on the Thank You page
"""

import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import WomenConfig


def login(driver, wait):
    """Log in to the Magento site using provided credentials."""
    driver.get(WomenConfig.LOGIN_URL)
    wait.until(EC.presence_of_element_located((By.ID, WomenConfig.SIGN_IN_EMAIL_INPUT))).send_keys(
        WomenConfig.EMAIL
    )
    driver.find_element(By.ID, WomenConfig.SIGN_IN_PASSWORD_INPUT).send_keys(WomenConfig.PASSWORD)
    driver.find_element(By.ID, WomenConfig.SIGN_IN_BUTTON).click()
    wait.until(EC.presence_of_element_located((By.ID, WomenConfig.SEARCH_INPUT_ID)))
    print("Logged in successfully")


def search_and_add_shirt(driver, wait):
    """Search for a shirt and add it to the cart."""
    search_box = wait.until(
        EC.presence_of_element_located((By.ID, WomenConfig.SEARCH_INPUT_ID))
    )
    search_box.clear()
    search_box.send_keys("shirt")
    search_box.submit()

    wait.until(EC.element_to_be_clickable((By.XPATH, WomenConfig.RADIANT_TEE_XPATH))).click()
    driver.execute_script("window.scrollBy(0, 500);")

    wait.until(EC.element_to_be_clickable((By.ID, WomenConfig.SIZE_M_ID))).click()
    wait.until(EC.element_to_be_clickable((By.ID, WomenConfig.COLOR_BLUE_ID))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, WomenConfig.ADD_TO_CART_XPATH))).click()
    print("Shirt added to cart")


def proceed_to_checkout(driver, wait):
    """Proceed to checkout from the minicart."""
    cart_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, WomenConfig.MY_CART_XPATH))
    )
    driver.execute_script("arguments[0].click();", cart_button)

    wait.until(EC.visibility_of_element_located((By.XPATH, WomenConfig.VIEW_CART_XPATH))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, WomenConfig.PROCEED_TO_CHECKOUT_CART_XPATH))).click()
    print("Reached checkout page")


def fill_shipping_details(driver, wait):
    """Fill in the shipping address form on the checkout page."""
    wait.until(EC.url_contains("checkout/#shipping"))

    wait.until(EC.presence_of_element_located(WomenConfig.CHECKOUT_COMPANY_SELECTOR)).send_keys(
        "NethraTech Pvt Ltd"
    )
    wait.until(EC.presence_of_element_located(WomenConfig.CHECKOUT_STREET_SELECTOR)).send_keys(
        "123 AI Street"
    )
    wait.until(EC.presence_of_element_located(WomenConfig.CHECKOUT_CITY_SELECTOR)).send_keys(
        "Bangalore"
    )

    Select(wait.until(
        EC.element_to_be_clickable(WomenConfig.CHECKOUT_STATE_DROPDOWN_SELECTOR))
    ).select_by_index(1)
    wait.until(EC.presence_of_element_located(WomenConfig.CHECKOUT_ZIP_SELECTOR)).send_keys("560001")
    Select(wait.until(
        EC.element_to_be_clickable(WomenConfig.CHECKOUT_COUNTRY_SELECTOR))
    ).select_by_index(1)
    wait.until(EC.presence_of_element_located(WomenConfig.CHECKOUT_PHONE_SELECTOR)).send_keys(
        "9844543210"
    )

    wait.until(EC.element_to_be_clickable(WomenConfig.SHIPPING_METHOD_RADIO_XPATH)).click()
    wait.until(EC.element_to_be_clickable(WomenConfig.NEXT_BUTTON_XPATH)).click()
    print("Shipping details submitted")


def place_order(driver, wait):
    """Place the order and verify redirection to the success page."""
    wait.until(EC.url_contains("checkout/#payment"))
    wait.until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "img[alt='Loading...']"))
    )

    place_order_button = wait.until(
        EC.element_to_be_clickable(WomenConfig.PLACE_ORDER_BUTTON_XPATH)
    )
    driver.execute_script("arguments[0].click();", place_order_button)

    wait.until(EC.url_to_be(WomenConfig.SUCCESS_PAGE_URL))
    print("Order placed successfully. Redirected to Thank You page")


def main():
    """Run the full automation flow from login to order placement."""
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.maximize_window()
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
