import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.base_driver import chrome_driver


def add_product_to_cart(chrome_driver):
    # Product details for testing
    product = {
        "url": "http://localhost/demo/index.php?route=product/product&language=en-gb&product_id=43",
        "name": "MacBook",
    }

    # Access the product page
    chrome_driver.get(product["url"])
    WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, "input-quantity"))
    )

    # Random quantity from 1 to 10
    random_quantity = random.randint(1, 10)
    quantity_field = chrome_driver.find_element(By.ID, "input-quantity")
    quantity_field.clear()  # Clear the field before entering new quantity
    quantity_field.send_keys(str(random_quantity))

    # Extract product details (Name, Price, Brand, Product Code, Availability)
    product_name = chrome_driver.find_element(By.CSS_SELECTOR, "div.col-sm h1").text
    price_new = chrome_driver.find_element(By.CSS_SELECTOR, ".price-new").text

    # Clean price to remove non-numeric characters (like $ and commas)
    price_new = price_new.replace('$', '').replace(',', '')

    # Convert price_new to float for calculation
    try:
        price_new = float(price_new)
    except ValueError:
        print(f"Error converting price to float: {price_new}")
        price_new = 0.0

    # Calculate total price based on quantity
    total_price = price_new * random_quantity

    # Print total price with comma separator for thousands
    print(f"Total Price for {random_quantity} {product_name}(s): ${total_price:,.2f} - (MANUAL)")

    # Click "Add to Cart" button
    add_to_cart_button = chrome_driver.find_element(By.ID, "button-cart")
    add_to_cart_button.click()

    # Wait for and verify the success message
    try:
        success_message_element = WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-success"))
        )
        success_message = success_message_element.text
        expected_message = f"Success: You have added {product['name']} to your shopping cart!"
        assert expected_message in success_message, \
            f"Unexpected success message for {product['name']}: {success_message}"
        # print(f"Success message verified for {product['name']}: {success_message}")
    except Exception as e:
        print(f"Error while verifying success message for {product['name']}: {e}")

    print("-" * 40)

    return total_price


def add_three_products_to_cart(chrome_driver):
    products = [
        {"url": "http://localhost/demo/index.php?route=product/product&language=en-gb&product_id=43", "name": "MacBook",
         "price": 602.00},
        {"url": "http://localhost/demo/index.php?route=product/product&language=en-gb&product_id=40", "name": "iPhone",
         "price": 123.20},
        {"url": "http://localhost/demo/index.php?route=product/product&language=en-gb&product_id=28",
         "name": "HTC Touch HD", "price": 122.00},
    ]

    for product in products:
        # Access the product page
        chrome_driver.get(product["url"])
        WebDriverWait(chrome_driver, 10).until(
            EC.presence_of_element_located((By.ID, "input-quantity"))
        )

        # Random quantity from 1 to 10 (for simplicity, use a fixed quantity here)
        random_quantity = 5  # or any value from 1 to 10
        quantity_field = chrome_driver.find_element(By.ID, "input-quantity")
        quantity_field.clear()  # Clear the field before entering new quantity
        quantity_field.send_keys(str(random_quantity))
        new_price_text = chrome_driver.find_element(By.CSS_SELECTOR, ".price-new").text

        print(f"Product: {product['name']}")
        print(f"Price/{product['name']}: {new_price_text}")
        print(f"Qty: {random_quantity}")
        print("-"*40)

        # Click "Add to Cart" button
        add_to_cart_button = chrome_driver.find_element(By.ID, "button-cart")
        add_to_cart_button.click()

        # Wait for and verify the success message
        try:
            success_message_element = WebDriverWait(chrome_driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-success"))
            )
            success_message = success_message_element.text
            expected_message = f"Success: You have added {product['name']} to your shopping cart!"
            assert expected_message in success_message, \
                f"Unexpected success message for {product['name']}: {success_message}"
            # print(f"Success message verified for {product['name']}: {success_message}")
        except Exception as e:
            print(f"Error while verifying success message for {product['name']}: {e}")

def compare_total_price(chrome_driver):
    # Get the total price of all products added to the cart (from the previous step)
    product_prices = {
        "MacBook": {"price": 602.00, "quantity": 5},
        "iPhone": {"price": 123.20, "quantity": 5},
        "HTC Touch HD": {"price": 122.00, "quantity": 5}
    }

    # Calculate total price of all products
    total_price_all_products = sum([product['price'] * product['quantity'] for product in product_prices.values()])

    # Print the calculated total price for all products
    print(f"Total Price for all products (MANUAL): ${total_price_all_products:,.2f}")

    # Wait for the checkout total to load and get the total from the checkout page
    WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, "checkout-total"))
    )

    # Extract the total price from the checkout footer
    total_in_checkout = chrome_driver.find_element(By.XPATH, "//tfoot[@id='checkout-total']//tr[4]/td[2]").text
    total_in_checkout = float(total_in_checkout.replace('$', '').replace(',', ''))

    # Print the extracted total price from the checkout footer
    print(f"Total from Checkout (WEB CHECKOUT): ${total_in_checkout:,.2f}")

    # Compare the two totals and assert that they are the same
    assert total_price_all_products == total_in_checkout, \
        f"Total price mismatch! Calculated Total: ${total_price_all_products:,.2f}, Checkout Total: ${total_in_checkout:,.2f}"

    print("\n ==> The total price matches between the cart and the checkout!")


def add_two_products_to_cart(chrome_driver):

    # Product details for testing
    products = [
        {
            "url": "http://localhost/demo/index.php?route=product/product&language=en-gb&product_id=43",
            "name": "MacBook",
        },
        {
            "url": "http://localhost/demo/index.php?route=product/product&language=en-gb&product_id=40",
            "name": "iPhone",
        },
    ]

    for product in products:
        # Access the product page
        chrome_driver.get(product["url"])
        WebDriverWait(chrome_driver, 10).until(
            EC.presence_of_element_located((By.ID, "input-quantity"))
        )
        print(f"Accessed product page: {product['url']}")

        # Random quantity from 1 to 10
        random_quantity = random.randint(1, 10)
        quantity_field = chrome_driver.find_element(By.ID, "input-quantity")
        quantity_field.clear()  # Clear the field before entering new quantity
        quantity_field.send_keys(str(random_quantity))
        print(f"Selected quantity: {random_quantity} for {product['name']}")

        # Click "Add to Cart" button
        add_to_cart_button = chrome_driver.find_element(By.ID, "button-cart")
        add_to_cart_button.click()
        print(f"Clicked 'Add to Cart' button for {product['name']}")

        # Wait for and verify the success message
        try:
            success_message_element = WebDriverWait(chrome_driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-success"))
            )
            success_message = success_message_element.text
            expected_message = f"Success: You have added {product['name']} to your shopping cart!"
            assert expected_message in success_message, \
                f"Unexpected success message for {product['name']}: {success_message}"
            print(f"Success message verified for {product['name']}: {success_message}")
        except Exception as e:
            print(f"Error while verifying success message for {product['name']}: {e}")

    print("-" * 40)