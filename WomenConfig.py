#Config file of WomenSection.py
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
load_dotenv() 
# URLs
HOME_URL = "https://magento.softwaretestingboard.com/"
LOGIN_URL = "https://magento.softwaretestingboard.com/customer/account/login/"
SUCCESS_PAGE_URL = "https://magento.softwaretestingboard.com/checkout/onepage/success/"

# Credentials from environment variables
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# Login
SIGN_IN_EMAIL_INPUT = "email"
SIGN_IN_PASSWORD_INPUT = "pass"
SIGN_IN_BUTTON = "send2"

# Registration
CREATE_ACCOUNT_LINK = "//a[contains(@href, 'customer/account/create')]"
FIRST_NAME_INPUT = "firstname"
LAST_NAME_INPUT = "lastname"
EMAIL_INPUT = "email_address"
PASSWORD_INPUT = "password"
CONFIRM_PASSWORD_INPUT = "password-confirmation"
CREATE_ACCOUNT_BUTTON = "//button[@title='Create an Account']"

# Product selectors
WOMEN_TAB_XPATH = "//span[text()='Women']"
PRODUCT_LINK_XPATH = "//a[@class='product-item-link' and normalize-space(text())='Breathe-Easy Tank']"
SIZE_S_XPATH = "//div[@class='swatch-option text' and text()='S']"
COLOR_YELLOW_XPATH = "//div[@class='swatch-option color' and @option-label='Yellow']"
ADD_TO_CART_XPATH = "//span[text()='Add to Cart']"


# Radiant Tee
SEARCH_INPUT_ID = "search"
RADIANT_TEE_XPATH = "//a[@class='product-item-link' and contains(text(), 'Radiant Tee')]"
SIZE_M_ID = "option-label-size-143-item-168"
COLOR_BLUE_ID = "option-label-color-93-item-50"

# Cart
MY_CART_XPATH = "//span[text()='My Cart']"
VIEW_CART_XPATH = "//span[contains(text(),'View and Edit Cart')]"
PROCEED_TO_CHECKOUT_CART_XPATH = "//span[text()='Proceed to Checkout']"

# Shipping Info Data
COMPANY_NAME = "NethraTech Pvt Ltd"
STREET_ADDRESS = "123 AI Street"
CITY = "Bangalore"
STATE_INDEX = 1  # Adjust as per dropdown index
ZIP_CODE = "560001"
COUNTRY_INDEX = 1  # Adjust as per dropdown index
PHONE_NUMBER = "9844543210"

# Checkout Fields
CHECKOUT_COMPANY_SELECTOR = (By.NAME, "company")
CHECKOUT_STREET_SELECTOR = (By.NAME, "street[0]")
CHECKOUT_CITY_SELECTOR = (By.NAME, "city")
CHECKOUT_STATE_DROPDOWN_SELECTOR = (By.NAME, "region_id")
CHECKOUT_ZIP_SELECTOR = (By.NAME, "postcode")
CHECKOUT_COUNTRY_SELECTOR = (By.NAME, "country_id")
CHECKOUT_PHONE_SELECTOR = (By.NAME, "telephone")

# Shipping & Payment
SHIPPING_METHOD_RADIO_XPATH = (By.XPATH, "//input[@type='radio' and contains(@value,'flatrate')]")
NEXT_BUTTON_XPATH = (By.XPATH, "//span[@data-bind=\"i18n: 'Next'\"]")
PLACE_ORDER_BUTTON_XPATH = (By.XPATH, "//span[@data-bind=\"i18n: 'Place Order'\"]")
