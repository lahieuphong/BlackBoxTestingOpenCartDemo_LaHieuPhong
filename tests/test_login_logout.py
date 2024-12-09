import time
from selenium.webdriver.common.by import By
from utils.base_driver import chrome_driver
from pages.login_page import navigate_to_login_page, login_success_chrome, count_account_menu_items
from pages.navigate_page import navigate_to_logout, navigate_to_homepage


def test_login_success_chrome(chrome_driver):
    login_success_chrome(chrome_driver)

    # Check the "My Account" dropdown
    my_account_dropdown = chrome_driver.find_element(By.CSS_SELECTOR, "a.dropdown-toggle i.fa-user")
    my_account_dropdown.click()
    time.sleep(2)  # Wait for dropdown to open
    print("Opened 'My Account' dropdown.")

    # Count the number of items in the dropdown menu
    item_count = count_account_menu_items(chrome_driver)

    # Assert that there are five items in the dropdown when logged in
    assert item_count == 5, f"Expected 5 menu items in My Account dropdown, but found {item_count}. Login likely failed."
    print("Login success confirmed. Dropdown contains expected 5 items.")


def test_login_failure_invalid_username_chrome(chrome_driver):
    # Go to the login page
    navigate_to_login_page(chrome_driver)

    # Input incorrect email
    email_input = chrome_driver.find_element(By.ID, "input-email")
    email_input.send_keys("incorrect@example.com")
    time.sleep(1)
    print("Entered incorrect email.")

    # Input incorrect password
    password_input = chrome_driver.find_element(By.ID, "input-password")
    password_input.send_keys("21112003")
    time.sleep(1)
    print("Entered incorrect password.")

    # Click login button
    login_button = chrome_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    time.sleep(3)  # Wait for login attempt to process
    print("Clicked login button.")

    # Verify that login failed by checking for a specific error alert message
    error_alerts = chrome_driver.find_elements(By.CSS_SELECTOR, ".alert.alert-danger")
    assert error_alerts, "Expected an error alert, but none was found."

    # Check that the first error alert is displayed and contains the correct message
    error_alert = error_alerts[0]
    assert error_alert.is_displayed(), "Expected the error alert to be displayed, but it was not found."
    assert "Warning: No match for E-Mail Address and/or Password." in error_alert.text, \
        "The specific warning message for incorrect login was not displayed as expected."
    print(f"Correct warning message found; login failed as expected. Alert message: {error_alert.text}")

    # Click on the logo to go back to the home page
    logo = chrome_driver.find_element(By.CSS_SELECTOR, "img[title='Your Store']")
    logo.click()
    time.sleep(3)  # Wait for the home page to load
    print("Clicked on the logo to go back to the home page.")

    # Click on the "My Account" dropdown
    my_account_dropdown = chrome_driver.find_element(By.CSS_SELECTOR, "a.dropdown-toggle i.fa-user")
    my_account_dropdown.click()
    time.sleep(2)  # Wait for dropdown to open
    print("Opened 'My Account' dropdown.")

    # Count the number of items in the dropdown menu
    item_count = count_account_menu_items(chrome_driver)

    # Assert that there are only two items (Register and Login) in the dropdown when login fails
    assert item_count == 2, f"Expected 2 menu items in My Account dropdown, but found {item_count}. Login failure not detected correctly."
    print("Login failure confirmed. Dropdown contains expected 2 items.")


def test_login_failure_invalid_password_chrome(chrome_driver):
    # Go to the login page
    navigate_to_login_page(chrome_driver)

    # Input incorrect email
    email_input = chrome_driver.find_element(By.ID, "input-email")
    email_input.send_keys("hieuphong144@gmail.com")
    time.sleep(1)
    print("Entered incorrect email.")

    # Input incorrect password
    password_input = chrome_driver.find_element(By.ID, "input-password")
    password_input.send_keys("211120033")
    time.sleep(1)
    print("Entered incorrect password.")

    # Click login button
    login_button = chrome_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    time.sleep(3)  # Wait for login attempt to process
    print("Clicked login button.")

    # Verify that login failed by checking for a specific error alert message
    error_alerts = chrome_driver.find_elements(By.CSS_SELECTOR, ".alert.alert-danger")
    assert error_alerts, "Expected an error alert, but none was found."

    # Check that the first error alert is displayed and contains the correct message
    error_alert = error_alerts[0]
    assert error_alert.is_displayed(), "Expected the error alert to be displayed, but it was not found."
    assert "Warning: No match for E-Mail Address and/or Password." in error_alert.text, \
        "The specific warning message for incorrect login was not displayed as expected."
    print(f"Correct warning message found; login failed as expected. Alert message: {error_alert.text}")

    # Click on the logo to go back to the home page
    logo = chrome_driver.find_element(By.CSS_SELECTOR, "img[title='Your Store']")
    logo.click()
    time.sleep(3)  # Wait for the home page to load
    print("Clicked on the logo to go back to the home page.")

    # Click on the "My Account" dropdown
    my_account_dropdown = chrome_driver.find_element(By.CSS_SELECTOR, "a.dropdown-toggle i.fa-user")
    my_account_dropdown.click()
    time.sleep(2)  # Wait for dropdown to open
    print("Opened 'My Account' dropdown.")

    # Count the number of items in the dropdown menu
    item_count = count_account_menu_items(chrome_driver)

    # Assert that there are only two items (Register and Login) in the dropdown when login fails
    assert item_count == 2, f"Expected 2 menu items in My Account dropdown, but found {item_count}. Login failure not detected correctly."
    print("Login failure confirmed. Dropdown contains expected 2 items.")


def test_login_failure_empty_credentials_chrome(chrome_driver):
    # Go to the login page
    navigate_to_login_page(chrome_driver)

    # Leave the email field empty
    email_input = chrome_driver.find_element(By.ID, "input-email")
    email_input.clear()  # Ensure it's empty
    time.sleep(1)
    print("Email field is empty.")

    # Leave the password field empty
    password_input = chrome_driver.find_element(By.ID, "input-password")
    password_input.clear()  # Ensure it's empty
    time.sleep(1)
    print("Password field is empty.")

    # Click login button
    login_button = chrome_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    time.sleep(3)  # Wait for login attempt to process
    print("Clicked login button.")

    # Verify that login failed by checking for a specific error alert message
    error_alerts = chrome_driver.find_elements(By.CSS_SELECTOR, ".alert.alert-danger")
    assert error_alerts, "Expected an error alert, but none was found."

    # Check that the first error alert is displayed and contains the correct message
    error_alert = error_alerts[0]
    assert error_alert.is_displayed(), "Expected the error alert to be displayed, but it was not found."
    assert "Warning: No match for E-Mail Address and/or Password." in error_alert.text, \
        "The specific warning message for missing credentials was not displayed as expected."
    print(f"Correct warning message found; login failed as expected. Alert message: {error_alert.text}")

    # Click on the logo to go back to the home page
    logo = chrome_driver.find_element(By.CSS_SELECTOR, "img[title='Your Store']")
    logo.click()
    time.sleep(3)  # Wait for the home page to load
    print("Clicked on the logo to go back to the home page.")

    # Click on the "My Account" dropdown
    my_account_dropdown = chrome_driver.find_element(By.CSS_SELECTOR, "a.dropdown-toggle i.fa-user")
    my_account_dropdown.click()
    time.sleep(2)  # Wait for dropdown to open
    print("Opened 'My Account' dropdown.")

    # Count the number of items in the dropdown menu
    item_count = count_account_menu_items(chrome_driver)

    # Assert that there are only two items (Register and Login) in the dropdown when login fails
    assert item_count == 2, f"Expected 2 menu items in My Account dropdown, but found {item_count}. Login failure not detected correctly."
    print("Login failure confirmed. Dropdown contains expected 2 items.")


def test_logout_success_chrome(chrome_driver):
    # First, call the test_login_success to ensure the user is logged in
    test_login_success_chrome(chrome_driver)

    # Click on the logout link
    logout_link = chrome_driver.find_element(By.LINK_TEXT, "Logout")
    logout_link.click()
    time.sleep(3)  # Wait for logout to process
    print("Clicked logout link.")

    # Verify redirection to logout confirmation page
    expected_logout_url = navigate_to_logout(chrome_driver)
    assert chrome_driver.current_url == expected_logout_url, "Logout redirection failed!"
    print("Redirected to logout page successfully.")

    # Verify that the logout confirmation page contains the expected content
    logout_header = chrome_driver.find_element(By.TAG_NAME, "h1")
    assert logout_header.is_displayed() and logout_header.text == "Account Logout", "Logout header not found!"
    print("Logout confirmation header is present.")

    logout_message = chrome_driver.find_element(By.XPATH, "//div[@id='content']/p[1]")
    assert "You have been logged off your account." in logout_message.text, "Logout message not found!"
    print("Logout confirmation message is present.")

    # Click on the 'Continue' button to return to the home page
    continue_button = chrome_driver.find_element(By.CSS_SELECTOR, "a.btn.btn-primary")
    continue_button.click()
    time.sleep(3)  # Wait for home page to load
    print("Clicked 'Continue' button.")

    # Verify redirection back to the home page
    expected_home_url = navigate_to_homepage(chrome_driver)
    assert chrome_driver.current_url == expected_home_url, "Failed to return to the home page after logout!"
    print("Returned to the home page successfully after logout.")

    # Click on the 'My Account' dropdown again
    my_account_dropdown = chrome_driver.find_element(By.CSS_SELECTOR, "a.dropdown-toggle i.fa-user")
    my_account_dropdown.click()
    time.sleep(2)  # Wait for dropdown to open
    print("Opened 'My Account' dropdown again.")

    # Count the number of items in the dropdown menu
    item_count = count_account_menu_items(chrome_driver)

    # Assert that there are only two items (Register and Login) in the dropdown after logout
    assert item_count == 2, f"Expected 2 menu items in My Account dropdown after logout, but found {item_count}."
    print("Logout success confirmed. Dropdown contains expected 2 items after logout.")