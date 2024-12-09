import time
from selenium.webdriver.common.by import By
from utils.base_driver import chrome_driver
from pages.navigate_page import navigate_to_contact_us, navigate_to_homepage, navigate_to_contact_us_success


def test_contact_form_submission_success_chrome(chrome_driver):
    print("Starting test_contact_form_submission...")

    # Update the URL to the local server
    navigate_to_contact_us(chrome_driver)
    time.sleep(3)  # Wait for page to load

    # Fill out the contact form
    name_input = chrome_driver.find_element(By.ID, "input-name")
    name_input.send_keys("La Hieu Phong")
    time.sleep(1)

    email_input = chrome_driver.find_element(By.ID, "input-email")
    email_input.send_keys("hieuphong144@gmail.com")
    time.sleep(1)

    enquiry_input = chrome_driver.find_element(By.ID, "input-enquiry")
    enquiry_input.send_keys(
        "Hello,\n\nMy name is La Hieu Phong, and I am very interested in your store's products. "
        "I have a few questions regarding your shipping policies and warranty. I would greatly appreciate it if you could provide me with more detailed information.\n\nThank you very much!"
    )
    time.sleep(1)

    # Ensure the submit button is in view
    submit_button = chrome_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    chrome_driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    time.sleep(2)  # Ensure no overlays

    # Attempt to click the submit button
    submit_button.click()
    time.sleep(5)  # Wait for form submission to process

    # Check that the page redirects to the success page
    assert chrome_driver.current_url == navigate_to_contact_us_success(chrome_driver), \
        "Redirection to contact success page failed!"
    print("Redirected to contact success page successfully.")

    # Check the success page header
    success_header = chrome_driver.find_element(By.TAG_NAME, "h1")
    assert success_header.text == "Contact Us", "Contact success header not found!"
    print("Contact success header is present.")

    success_message = chrome_driver.find_element(By.XPATH, "//div[@id='content']/p")
    assert success_message.text == "Your enquiry has been successfully sent to the store owner!", \
        "Success message not found or incorrect!"
    print("Success message is present.")

    # Click 'Continue' to return to the home page
    continue_button = chrome_driver.find_element(By.CSS_SELECTOR, "a.btn.btn-primary")
    time.sleep(1)
    continue_button.click()
    time.sleep(3)  # Wait for home page to load
    print("Clicked 'Continue' button to return to the home page.")

    # Ensure return to home page
    assert chrome_driver.current_url == navigate_to_homepage(chrome_driver), \
        "Failed to return to the home page after submission!"
    print("Returned to the home page successfully after contact form submission.")


def test_contact_form_submission_failure_chrome(chrome_driver):
    # Navigate to the local contact page
    navigate_to_contact_us(chrome_driver)
    time.sleep(3)  # Wait for page to load
    print("Navigated to contact page.")

    # Leave the name field empty
    name_input = chrome_driver.find_element(By.ID, "input-name")
    name_input.send_keys("")  # Keep it empty to trigger error
    time.sleep(1)
    print("Entered name.")

    # Leave the email field empty
    email_input = chrome_driver.find_element(By.ID, "input-email")
    email_input.send_keys("")  # Keep it empty to trigger error
    time.sleep(1)
    print("Entered email.")

    # Leave the enquiry textarea empty
    enquiry_input = chrome_driver.find_element(By.ID, "input-enquiry")
    enquiry_input.send_keys("")  # Keep it empty to trigger error
    time.sleep(1)
    print("Entered enquiry message.")

    # Scroll to the submit button
    submit_button = chrome_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    chrome_driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    time.sleep(2)

    # Click the submit button
    submit_button.click()
    time.sleep(5)  # Wait for form submission to process
    print("Clicked submit button.")

    # Verify no redirection to success page
    assert chrome_driver.current_url != navigate_to_contact_us_success(chrome_driver), \
        "Redirection to contact success page occurred despite invalid input!"
    print("No redirection to contact success page, as expected.")

    # Verify error messages
    error_message_name = chrome_driver.find_element(By.ID, "error-name")
    assert error_message_name.is_displayed(), "Expected error message for empty name not found!"
    assert error_message_name.text == "Name must be between 3 and 32 characters!", "Incorrect error message for name!"
    print("Name error message displayed: " + error_message_name.text)

    error_message_email = chrome_driver.find_element(By.ID, "error-email")
    assert error_message_email.is_displayed(), "Expected error message for empty email not found!"
    assert error_message_email.text == "E-Mail Address does not appear to be valid!", "Incorrect error message for email!"
    print("Email error message displayed: " + error_message_email.text)

    error_message_enquiry = chrome_driver.find_element(By.ID, "error-enquiry")
    assert error_message_enquiry.is_displayed(), "Expected error message for empty enquiry not found!"
    assert error_message_enquiry.text == "Enquiry must be between 10 and 3000 characters!", "Incorrect error message for enquiry!"
    print("Enquiry error message displayed: " + error_message_enquiry.text)