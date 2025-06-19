"""
Automated Selenium script to login, search for a shirt, add it to the cart,
fill shipping details, and place an order.
"""

import traceback  # Standard imports first
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import config1


def start_driver():
    """Start and configure Chrome WebDriver."""
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver


def login(driver, wait):
    """Perform login using credentials from config1."""
    driver.get(config1.LOGIN_URL)
    wait.until(EC.presence_of_element_located((By.ID, config1.SIGN_IN_EMAIL_INPUT)))\
        .send_keys(config1.EMAIL)
    driver.find_element(By.ID, config1.SIGN_IN_PASSWORD_INPUT).send_keys(config1.PASSWORD)
    driver.find_element(By.ID, config1.SIGN_IN_BUTTON).click()
    wait.until(EC.presence_of_element_located((By.ID, config1.SEARCH_INPUT_ID)))


def search_and_add_shirt(driver, wait):
    """Search for a shirt and add it to the cart."""
    search_box = wait.until(EC.presence_of_element_located((By.ID, config1.SEARCH_INPUT_ID)))
    search_box.clear()
    search_box.send_keys("shirt")
    search_box.submit()

    wait.until(EC.element_to_be_clickable((By.XPATH, config1.RADIANT_TEE_XPATH))).click()
    driver.execute_script("window.scrollBy(0, 500);")

    wait.until(EC.element_to_be_clickable((By.ID, config1.SIZE_M_ID))).click()
    wait.until(EC.element_to_be_clickable((By.ID, config1.COLOR_BLUE_ID))).click()

    add_to_cart_btn = wait.until(EC.element_to_be_clickable((By.XPATH, config1.ADD_TO_CART_XPATH)))
    driver.execute_script("arguments[0].click();", add_to_cart_btn)

    print(" Product added to cart.")


    print("Product added to cart.")


#Proceed to checkout
def proceed_to_checkout(driver, wait):

    print("Clicking cart icon to view minicart...")

    # Click on <a class='action showcart'> to open the minicart
    """Open the minicart and click 'Proceed to Checkout'."""
    print("Clicking cart icon to view minicart...")
    cart_icon = wait.until(EC.element_to_be_clickable((By.XPATH, config1.CART_ICON_XPATH)))
    driver.execute_script("arguments[0].click();", cart_icon)

    print("➡️ Clicking 'Proceed to Checkout' button...")
    try:
        checkout_btn = wait.until(
            EC.element_to_be_clickable((By.ID, config1.MINICART_CHECKOUT_BUTTON_ID))
        )
        driver.execute_script("arguments[0].click();", checkout_btn)
    except Exception as e:  # You could narrow this to TimeoutException
        driver.save_screenshot("checkout_btn_error.png")
        raise RuntimeError("Could not click 'Proceed to Checkout' button.") from e


def fill_shipping_details(driver, wait):
    """Fill in all shipping address fields."""
    wait.until(EC.url_contains("checkout/#shipping"))

    wait.until(EC.presence_of_element_located(config1.CHECKOUT_COMPANY_SELECTOR))\
        .send_keys("NethraTech Pvt Ltd")
    wait.until(EC.presence_of_element_located(config1.CHECKOUT_STREET_SELECTOR))\
        .send_keys("123 AI Street")
    wait.until(EC.presence_of_element_located(config1.CHECKOUT_CITY_SELECTOR))\
        .send_keys("Bangalore")

    Select(wait.until(EC.element_to_be_clickable(config1.CHECKOUT_STATE_DROPDOWN_SELECTOR)))\
        .select_by_index(1)
    wait.until(EC.presence_of_element_located(config1.CHECKOUT_ZIP_SELECTOR))\
        .send_keys("560001")
    Select(wait.until(EC.element_to_be_clickable(config1.CHECKOUT_COUNTRY_SELECTOR)))\
        .select_by_index(1)
    wait.until(EC.presence_of_element_located(config1.CHECKOUT_PHONE_SELECTOR))\
        .send_keys("9844543210")

    wait.until(EC.element_to_be_clickable(config1.SHIPPING_METHOD_RADIO_XPATH)).click()
    wait.until(EC.element_to_be_clickable(config1.NEXT_BUTTON_XPATH)).click()


def place_order(driver, wait):
    """Place the final order and confirm success."""
    wait.until(EC.url_contains("checkout/#payment"))
    wait.until(EC.invisibility_of_element_located(
        (By.CSS_SELECTOR, "img[alt='Loading...']")
    ))

    place_order_button = wait.until(
        EC.element_to_be_clickable(config1.PLACE_ORDER_BUTTON_XPATH)
    )
    driver.execute_script("arguments[0].click();", place_order_button)

    wait.until(EC.url_to_be(config1.SUCCESS_PAGE_URL))


def run_shirt_search_checkout():
    """Execute the entire shirt purchase flow."""
    driver = start_driver()
    wait = WebDriverWait(driver, 20)

    try:
        login(driver, wait)
        search_and_add_shirt(driver, wait)
        proceed_to_checkout(driver, wait)
        fill_shipping_details(driver, wait)
        place_order(driver, wait)
        print("Order placed successfully. Redirected to Thank You page.")
    except Exception as e:
        print("Test failed:", e)
        traceback.print_exc()
    finally:
        driver.quit()


if __name__ == "__main__":
    run_shirt_search_checkout()
