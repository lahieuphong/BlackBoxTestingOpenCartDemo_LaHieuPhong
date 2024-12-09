import time
import pytest
from selenium.webdriver.common.by import By

from utils.base_driver import chrome_driver
from pages.navigate_page import navigate_to_homepage


@pytest.mark.parametrize("search_term", ["MacBook", "macbook"])
def test_search_macbook(chrome_driver, search_term):
    # Step 1: Navigate to the homepage
    navigate_to_homepage(chrome_driver)

    # Step 2: Find the search input box and enter the search term
    search_box = chrome_driver.find_element(By.NAME, "search")
    search_box.send_keys(search_term)
    time.sleep(1)  # Wait after entering the keyword
    print(f"\nEntered '{search_term}' into the search box.")

    # Step 3: Click the search button
    search_button = chrome_driver.find_element(By.CSS_SELECTOR, "button.btn.btn-light.btn-lg")
    search_button.click()
    time.sleep(2)  # Wait for the search results page to load

    chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Step 5: Verify the presence of the search result heading with the text "Search - MacBook"
    search_heading = chrome_driver.find_element(By.TAG_NAME, "h1").text
    expected_heading = f"Search - {search_term.capitalize()}"

    # Convert both to lowercase to make the comparison case-insensitive
    assert search_heading.lower() == expected_heading.lower(), f"Expected heading '{expected_heading}', but got '{search_heading}'"
    print(f"Verified heading: '{search_heading}'")
    print(f"-"*40)

    # Step 6: Verify the presence of product listings for "MacBook"
    product_list = chrome_driver.find_element(By.ID, "product-list")
    products = product_list.find_elements(By.CLASS_NAME, "product-thumb")

    # Ensure there are multiple products listed
    assert len(products) > 0, "Expected at least one product, but found none."
    print(f"Found {len(products)} product(s) in the search results for '{search_term}'.")

    # Step 7: Verify each product item contains "MacBook" in the title
    expected_data = ['MacBook', 'MacBook Air', 'MacBook Pro']
    product_result = []

    for product in products:
        product_title = product.find_element(By.CSS_SELECTOR, ".content h4 a").text
        assert "MacBook" in product_title, f"Product title '{product_title}' does not contain 'MacBook'."
        print(f"Verified product: '{product_title}'")

        # Optionally, print the price information for each product
        product_price = product.find_element(By.CLASS_NAME, "price-new").text
        print(f"Product '{product_title}' has a price of {product_price}")

        # Add product name to the result list
        product_result.append({'name': product_title})

    # Check if any of the product names match the expected data
    print([product['name'] for product in product_result])  # Print all the product names
    assert any(data in [product['name'] for product in product_result] for data in expected_data), \
        f"Expected products '{expected_data}' not found in search results."

    time.sleep(2)


@pytest.mark.parametrize("search_term", ["MacBok", "macbok", "######"])
def test_search_macbook_fail(chrome_driver, search_term):
    # Step 1: Navigate to the homepage
    navigate_to_homepage(chrome_driver)

    # Step 2: Find the search input box and enter an intentionally incorrect term
    search_box = chrome_driver.find_element(By.NAME, "search")
    search_box.send_keys(search_term)
    time.sleep(1)  # Wait after entering the keyword
    print(f"\nEntered '{search_term}' into the search box.")

    # Step 3: Click the search button
    search_button = chrome_driver.find_element(By.CSS_SELECTOR, "button.btn.btn-light.btn-lg")
    search_button.click()
    time.sleep(5)  # Wait for the search results page to load

    chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Step 5: Verify the presence of the search result heading with the text "Search - MacBok" or "Search - macbok"
    search_heading = chrome_driver.find_element(By.TAG_NAME, "h1").text
    expected_heading = f"Search - {search_term}"
    assert search_heading == expected_heading, f"Expected heading '{expected_heading}', but got '{search_heading}'"
    print(f"Verified heading: '{search_heading}'")

    # Step 6: Check if no products are found and print the appropriate message
    try:
        # Check if the "no product matches" message appears
        no_results_message = chrome_driver.find_element(By.XPATH,
                                                        "//p[contains(text(), 'There is no product that matches the search criteria.')]").text
        expected_message = "There is no product that matches the search criteria."
        assert no_results_message == expected_message, f"Expected message '{expected_message}', but got '{no_results_message}'"

        print(f"-" * 40)
        # If no products are found, we don't need to look for the product list
        print(f"Found 0 product(s) in the search results for '{search_term}'.")
        print(f"Verified 'no product matches' message: '{no_results_message}'")
    except Exception as e:
        # If no results message is not found, handle the error and check for the product list
        print(f"Error occurred: {e}")
        try:
            # If the "no product matches" message is not found, look for the product list
            product_list = chrome_driver.find_element(By.ID, "product-list")
            products = product_list.find_elements(By.CLASS_NAME, "product-thumb")
            print(f"Found {len(products)} product(s) in the search results for '{search_term}'.")
        except:
            print("Could not find the product list element.")

    time.sleep(2)


def test_search_empty_keyword(chrome_driver):
    # Step 1: Navigate to the homepage
    navigate_to_homepage(chrome_driver)

    # Step 2: Find the search input box and clear any existing text (simulate empty search)
    search_box = chrome_driver.find_element(By.NAME, "search")
    search_box.clear()  # Clear the search box to simulate an empty search
    time.sleep(1)  # Wait after clearing the keyword
    print("\nCleared the search box (empty keyword).")

    # Step 3: Click the search button
    search_button = chrome_driver.find_element(By.CSS_SELECTOR, "button.btn.btn-light.btn-lg")
    search_button.click()
    time.sleep(5)  # Wait for the search results page to load

    chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Step 4: Verify if an empty search query shows an appropriate message or no results
    try:
        # Check if the "no product matches" message appears when no search term is provided
        no_results_message = chrome_driver.find_element(By.XPATH,
                                                        "//p[contains(text(), 'There is no product that matches the search criteria.')]").text
        expected_message = "There is no product that matches the search criteria."
        assert no_results_message == expected_message, f"Expected message '{expected_message}', but got '{no_results_message}'"

        print(f"-" * 40)
        # If no products are found, print the appropriate message
        print("Found 0 product(s) in the search results for an empty search.")
        print(f"Verified 'no product matches' message: '{no_results_message}'")
    except Exception as e:
        # If no results message is not found, handle the error and check for the product list
        print(f"Error occurred: {e}")
        try:
            # If the "no product matches" message is not found, look for the product list
            product_list = chrome_driver.find_element(By.ID, "product-list")
            products = product_list.find_elements(By.CLASS_NAME, "product-thumb")
            print(f"Found {len(products)} product(s) in the search results for an empty search.")
        except:
            print("Could not find the product list element.")

    time.sleep(2)  # Wait before ending the test


def test_search_with_percent(chrome_driver):
    # Step 1: Navigate to the homepage
    navigate_to_homepage(chrome_driver)

    # Step 2: Find the search input box and enter an intentionally incorrect or special term like "%"
    search_term = "%"

    search_box = chrome_driver.find_element(By.NAME, "search")
    search_box.send_keys(search_term)
    time.sleep(1)  # Wait after entering the keyword
    print(f"\nEntered '{search_term}' into the search box.")

    # Step 3: Click the search button
    search_button = chrome_driver.find_element(By.CSS_SELECTOR, "button.btn.btn-light.btn-lg")
    search_button.click()
    time.sleep(5)  # Wait for the search results page to load

    chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Step 4: Verify the presence of the search result heading with the text "Search - %"
    search_heading = chrome_driver.find_element(By.TAG_NAME, "h1").text
    expected_heading = f"Search - {search_term}"
    assert search_heading == expected_heading, f"Expected heading '{expected_heading}', but got '{search_heading}'"
    print(f"Verified heading: '{search_heading}'")

    # Step 5: Try to locate the "no product matches" message first
    try:
        no_results_message = chrome_driver.find_element(By.XPATH, "//p[contains(text(), 'There is no product that matches the search criteria.')]").text
        expected_message = "There is no product that matches the search criteria."
        assert no_results_message == expected_message, f"Expected message '{expected_message}', but got '{no_results_message}'"

        print(f"Verified 'no product matches' message: '{no_results_message}'")

    except Exception as e:
        # Check for products in the product list if no results message is not found
        product_list = chrome_driver.find_element(By.ID, "product-list")
        products = product_list.find_elements(By.CLASS_NAME, "product-thumb")

        # Fail the test if any products are found
        assert len(products) == 0, f"Expected 0 products but found {len(products)} for search term '{search_term}'."

        assert False, f"Expected 0 products but the 'no results' message was also not found."

    # Step 6: Wait a little bit before finishing the test
    time.sleep(2)