import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.base_driver import chrome_driver
from pages.add_to_cart_page import add_product_to_cart, add_three_products_to_cart, compare_total_price
from pages.navigate_page import navigate_to_shopping_cart, navigate_to_product_macbook


def test_add_single_product_to_cart(chrome_driver):
    # Call the function that adds the product to the cart and prints the total
    print(f"\nPRODUCT PAGE: ")
    total_added_price = add_product_to_cart(chrome_driver)  # Capture the total price from add_product_to_cart

    # Đợi sau khi sản phẩm được thêm vào giỏ hàng
    time.sleep(5)

    # Tìm nút "Shopping Cart" và nhấn vào nó
    shopping_cart_button = chrome_driver.find_element(By.XPATH, "//a[@title='Shopping Cart']")
    shopping_cart_button.click()

    # Chờ thêm một chút để trang giỏ hàng tải xong
    time.sleep(3)

    # Kiểm tra URL giỏ hàng
    current_url = chrome_driver.current_url
    assert current_url == navigate_to_shopping_cart(chrome_driver), f"Expected URL to be '{navigate_to_shopping_cart(chrome_driver)}', but got {current_url}"

    print(f"SHOPPING CART PAGE: ")
    # Lấy thông tin tổng cộng từ bảng giỏ hàng
    totals = chrome_driver.find_elements(By.XPATH, "//tfoot[@id='checkout-total']//tr")

    # Initialize a variable to store the total value
    cart_total = 0

    # Extract total price from the table
    for total_row in totals:
        label = total_row.find_element(By.XPATH, ".//td[@class='text-end']/strong").text
        amount = total_row.find_element(By.XPATH, ".//td[@class='text-end'][2]").text
        amount_value = float(amount.replace('$', '').replace(',', '').strip())
        if label == "Total":
            cart_total = amount_value
        print(f"{label}: {amount}")

    print('-' * 50)

    # Print the total value for comparison
    print(f"Total Price from Product (id 43): ${total_added_price:,.2f}")
    print(f"Total Price from Shopping Cart: ${cart_total:,.2f}")

    # Assert that the total calculated from the cart matches the total from the add_product_to_cart
    assert round(cart_total, 2) == round(total_added_price, 2), \
        f"Expected total to be {total_added_price:,.2f}, but got {cart_total:,.2f}"

    print("\n ==> Total price comparison passed!")


def test_add_multi_product_to_cart(chrome_driver):
    print(f"\nPRODUCTS PAGE:")
    # Add three products to the cart
    add_three_products_to_cart(chrome_driver)

    # Navigate to the checkout page
    navigate_to_shopping_cart(chrome_driver)
    time.sleep(2)
    chrome_driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(5)

    # Compare the total price of products with the total price in checkout
    compare_total_price(chrome_driver)


def test_add_product_to_cart_with_invalid_qty(chrome_driver):
    # Product details for testing
    product = {
        "url": navigate_to_product_macbook(chrome_driver),
        "name": "MacBook",
    }

    # Access the product page
    chrome_driver.get(product["url"])
    WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, "input-quantity"))
    )

    # Trying to send invalid quantity (non-numeric input like "abc")
    quantity_field = chrome_driver.find_element(By.ID, "input-quantity")
    quantity_field.clear()  # Clear the field before entering new quantity
    quantity_field.send_keys("abc")  # Sending non-numeric value "abc"
    time.sleep(2)
    print(f"Entered invalid quantity: 'abc' for {product['name']}")

    # Simulate the "Add to Cart" button click after entering invalid quantity
    add_to_cart_button = chrome_driver.find_element(By.ID, "button-cart")
    add_to_cart_button.click()  # Clicking the "Add to Cart" button

    time.sleep(5)

    # Wait for the message to appear and get it
    message_element = WebDriverWait(chrome_driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert"))
    )

    # Get the actual message text
    actual_message = message_element.text

    # Define the expected error message
    expected_message = "Error: You must enter a valid quantity"

    # Assert that the message is the expected error message
    assert actual_message == expected_message, \
        f"Test failed! Expected message: '{expected_message}', but got: '{actual_message}'"


def test_add_to_cart_with_empty_qty(chrome_driver):
    # Product details for testing
    product = {
        "url": navigate_to_product_macbook(chrome_driver),
        "name": "MacBook",
    }

    # Access the product page
    chrome_driver.get(product["url"])
    WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, "input-quantity"))
    )

    # Clear the quantity field (empty it)
    quantity_field = chrome_driver.find_element(By.ID, "input-quantity")
    quantity_field.clear()  # Clear the quantity field (making it empty)
    print(f"Cleared the quantity field for {product['name']}")

    # Simulate the "Add to Cart" button click after leaving the quantity empty
    add_to_cart_button = chrome_driver.find_element(By.ID, "button-cart")
    add_to_cart_button.click()  # Clicking the "Add to Cart" button

    time.sleep(5)

    # Wait for the message to appear and get it
    message_element = WebDriverWait(chrome_driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert"))
    )

    # Get the actual message text
    actual_message = message_element.text

    # Define the expected error message
    expected_message = "Error: You must enter a quantity"

    # Assert that the message is the expected error message
    assert actual_message == expected_message, \
        f"Test failed! Expected message: '{expected_message}', but got: '{actual_message}'"


def test_add_to_cart_with_zero_qty(chrome_driver):
    # Product details for testing
    product = {
        "url": navigate_to_product_macbook(chrome_driver),
        "name": "MacBook",
    }

    # Access the product page
    chrome_driver.get(product["url"])
    WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, "input-quantity"))
    )

    # Trying to send invalid quantity (non-numeric input like "abc")
    quantity_field = chrome_driver.find_element(By.ID, "input-quantity")
    quantity_field.clear()  # Clear the field before entering new quantity
    quantity_field.send_keys(0)  # Sending non-numeric value "abc"
    print(f"Entered invalid quantity: '0' for {product['name']}")

    # Simulate the "Add to Cart" button click after entering invalid quantity
    add_to_cart_button = chrome_driver.find_element(By.ID, "button-cart")
    add_to_cart_button.click()  # Clicking the "Add to Cart" button

    time.sleep(5)

    # Wait for the message to appear and get it
    message_element = WebDriverWait(chrome_driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert"))
    )

    # Get the actual message text
    actual_message = message_element.text

    # Define the expected error message
    expected_message = "Error: You must enter a valid quantity"

    # Assert that the message is the expected error message
    assert actual_message == expected_message, \
        f"Test failed! Expected message: '{expected_message}', but got: '{actual_message}'"