"""
Test script to navigate directly to the Women section,
open the 'Breathe-Easy Tank' product, select size 'S',
select color 'Yellow', and add the product to the cart.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

# Start Chrome driver
def start_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver

# Navigate to 'Women' and perform product actions
def test_women_product():
    driver = start_driver()
    wait = WebDriverWait(driver, 10)
    try:
        driver.get(config.HOME_URL)

        # Click Women tab
        women_tab = wait.until(EC.element_to_be_clickable((By.XPATH, config.WOMEN_TAB_XPATH)))
        women_tab.click()
        print(" Navigated to Women section.")

        # Click product
        product = wait.until(EC.element_to_be_clickable((By.XPATH, config.PRODUCT_LINK_XPATH)))
        product.click()
        print(" Opened Breathe-Easy Tank page.")

        # Scroll to swatch options
        driver.execute_script("window.scrollBy(0, 500);")

        # Select size S
        size_s = wait.until(EC.element_to_be_clickable((By.XPATH, config.SIZE_S_XPATH)))
        size_s.click()
        print(" Selected size S.")

        # Select color Yellow
        color_yellow = wait.until(EC.element_to_be_clickable((By.XPATH, config.COLOR_YELLOW_XPATH)))
        color_yellow.click()
        print(" Selected color Yellow.")

        # Click Add to Cart button
        add_to_cart = wait.until(EC.element_to_be_clickable((By.XPATH, config.ADD_TO_CART_XPATH)))
        add_to_cart.click()
        print(" Added to cart.")

    except Exception as e:
        print(f" Test Failed: {e}")
    finally:
        driver.quit()

# Run the test
test_women_product()
