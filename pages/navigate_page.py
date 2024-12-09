import time
from utils.base_driver import chrome_driver

# Function to navigate to the homepage
def navigate_to_homepage(chrome_driver):
    chrome_driver.get("http://localhost/demo/index.php?route=common/home&language=en-gb")
    time.sleep(1)  # Wait for the page to load
    return chrome_driver.current_url

def navigate_to_shopping_cart(chrome_driver):
    chrome_driver.get("http://localhost/demo/index.php?route=checkout/cart&language=en-gb")
    time.sleep(1)  # Wait for the page to load
    return chrome_driver.current_url

def navigate_to_product_macbook(chrome_driver):
    chrome_driver.get("http://localhost/demo/index.php?route=product/product&language=en-gb&product_id=43")
    time.sleep(1)  # Wait for the page to load
    return chrome_driver.current_url

def navigate_to_product_iphone(chrome_driver):
    chrome_driver.get("http://localhost/demo/index.php?route=product/product&language=en-gb&product_id=40")
    time.sleep(1)  # Wait for the page to load
    return chrome_driver.current_url

def navigate_to_product_hp_lp3065(chrome_driver):
    chrome_driver.get("http://localhost/demo/index.php?route=product/product&language=en-gb&product_id=47")
    time.sleep(1)  # Wait for the page to load
    return chrome_driver.current_url

def navigate_to_login(chrome_driver):
    chrome_driver.get("http://localhost/demo/index.php?route=account/login&language=en-gb")
    time.sleep(1)  # Wait for the page to load
    return chrome_driver.current_url

def navigate_to_logout(chrome_driver):
    chrome_driver.get("http://localhost/demo/index.php?route=account/logout&language=en-gb")
    time.sleep(1)  # Wait for the page to load
    return chrome_driver.current_url

def navigate_to_forgotten(chrome_driver):
    chrome_driver.get("http://localhost/demo/index.php?route=account/forgotten&language=en-gb")
    time.sleep(1)  # Wait for the page to load
    return chrome_driver.current_url

def navigate_to_checkout_success(chrome_driver):
    chrome_driver.get("http://localhost/demo/index.php?route=checkout/success&language=en-gb")
    time.sleep(1)  # Wait for the page to load
    return chrome_driver.current_url

def navigate_to_dashboard(chrome_driver):
    chrome_driver.get("http://localhost/demo/admin/index.php?route=common/dashboard&user_token=edb79579958f6bc283b3a46e52a73283")
    time.sleep(1)  # Wait for the page to load
    return chrome_driver.current_url

def navigate_to_contact_us(chrome_driver):
    chrome_driver.get("http://localhost/demo/index.php?route=information/contact&language=en-gb")
    time.sleep(1)  # Wait for the page to load
    return chrome_driver.current_url

def navigate_to_contact_us_success(chrome_driver):
    chrome_driver.get("http://localhost/demo/index.php?route=information/contact.success&language=en-gb")
    time.sleep(1)  # Wait for the page to load
    return chrome_driver.current_url