from utils.base_driver import chrome_driver
import time
import urllib
import urllib.parse
from selenium.webdriver.common.by import By


def navigate_to_login_page(chrome_driver):
    """Navigates to the login page."""
    chrome_driver.get("http://localhost/demo/index.php?route=account/login&language=en-gb")
    time.sleep(2)  # Wait for the page to load
    print("\nNavigated to login page.")

def count_account_menu_items(chrome_driver):
    """Counts the number of items in the 'My Account' dropdown menu."""
    account_menu_items = chrome_driver.find_elements(By.CSS_SELECTOR, "ul.dropdown-menu.dropdown-menu-right li")
    item_count = len(account_menu_items)
    print(f"Found {item_count} items in the dropdown menu.")
    return item_count


def login_success_chrome(chrome_driver):
    # Go to the login page
    navigate_to_login_page(chrome_driver)

    # Input email
    email_input = chrome_driver.find_element(By.ID, "input-email")
    email_input.send_keys("hieuphong144@gmail.com")
    time.sleep(1)
    print("Entered email.")

    # Input password
    password_input = chrome_driver.find_element(By.ID, "input-password")
    password_input.send_keys("21112003")
    time.sleep(1)
    print("Entered password.")

    # Click login button
    login_button = chrome_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    time.sleep(3)  # Wait for login to process
    print("Clicked login button.")

    # Assert no error alert is displayed
    error_alert = chrome_driver.find_elements(By.CSS_SELECTOR, ".alert.alert-danger")
    assert not error_alert, "Login failed with valid credentials!"
    print("No error alert found; login should be successful.")

    # Capture the current URL after login
    current_url = chrome_driver.current_url
    print(f"Current URL after login: {current_url}")

    # Assert that the current URL contains the account route
    assert "route=account/account" in current_url, \
        f"Expected to be redirected to account page, but was redirected to {current_url}!"

    # Extract the customer_token from the URL
    parsed_url = urllib.parse.urlparse(current_url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    customer_token = query_params.get('customer_token', [None])[0]

    assert customer_token is not None, "Customer token not found in the URL!"
    print("Successfully redirected to account page with a valid customer token.")

    # Navigate back to the main page and verify
    logo = chrome_driver.find_element(By.CSS_SELECTOR, "img[title='Your Store']")
    logo.click()
    time.sleep(3)  # Wait for the main page to load
    print("Clicked on the logo to go back to the home page.")

    # Check that we're on the home page with logged-in status
    assert chrome_driver.current_url == "http://localhost/demo/index.php?route=common/home&language=en-gb", \
        "Failed to return to the home page with logged-in status!"
    print("Returned to the home page successfully.")