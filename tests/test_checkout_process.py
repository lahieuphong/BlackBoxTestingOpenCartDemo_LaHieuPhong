import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.base_driver import chrome_driver
from pages.add_to_cart_page import add_two_products_to_cart
from pages.login_page import login_success_chrome
from pages.navigate_page import navigate_to_checkout_success, navigate_to_dashboard, navigate_to_product_macbook, navigate_to_product_iphone, navigate_to_shopping_cart


def test_checkout_and_admin_dashboard_validation(chrome_driver):
    # ========================
    # CHECKOUT PAGE (LOGIN SUCCESS)
    # ========================
    login_success_chrome(chrome_driver)
    add_two_products_to_cart(chrome_driver)

    try:
        # Step 1: Clicking the Checkout link
        WebDriverWait(chrome_driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-success"))
        )

        # Click the Checkout link
        checkout_link = WebDriverWait(chrome_driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[title='Checkout']"))
        )
        checkout_link.click()

        # Wait for the checkout page to load (use more flexible URL check)
        WebDriverWait(chrome_driver, 10).until(
            EC.url_contains("route=checkout/checkout")
        )

        # Wait for the shipping address dropdown to be visible and select the address
        WebDriverWait(chrome_driver, 10).until(
            EC.presence_of_element_located((By.ID, "input-shipping-address"))
        )

        # Step 2: Select Shipping Address
        shipping_address_dropdown = WebDriverWait(chrome_driver, 10).until(
            EC.element_to_be_clickable((By.ID, "input-shipping-address"))
        )
        shipping_address_dropdown.click()

        time.sleep(1)

        shipping_address_option = chrome_driver.find_element(By.XPATH, "//option[@value='1']")
        shipping_address_option.click()

        time.sleep(1)

        # Wait for success message
        WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-success"))
        )

        # Step 3: Choose Shipping Method
        # Wait for the 'Choose' button to be clickable
        choose_button = WebDriverWait(chrome_driver, 10).until(
            EC.element_to_be_clickable((By.ID, "button-shipping-methods"))
        )
        choose_button.click()

        time.sleep(1)

        # Optionally wait for confirmation or success message (if any)
        WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-success"))
        )

        # Wait for the shipping method radio button to be clickable
        shipping_method_radio_button = WebDriverWait(chrome_driver, 10).until(
            EC.element_to_be_clickable((By.ID, "input-shipping-method-flat-flat"))
        )
        # Click the radio button to select the shipping method
        shipping_method_radio_button.click()

        time.sleep(1)

        # Wait for the 'Continue' button to be clickable
        continue_button = WebDriverWait(chrome_driver, 10).until(
            EC.element_to_be_clickable((By.ID, "button-shipping-method"))
        )
        # Click the 'Continue' button
        continue_button.click()

        time.sleep(1)

        # Optionally, wait for a confirmation or success message that the shipping method has been applied
        WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-success"))
        )

        # Step 4: Choose Payment Method
        # Wait for the 'Choose' button to be clickable
        choose_payment_button = WebDriverWait(chrome_driver, 10).until(
            EC.element_to_be_clickable((By.ID, "button-payment-methods"))
        )
        choose_payment_button.click()

        time.sleep(1)

        # Optionally wait for confirmation or success message (if any)
        WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-success"))
        )

        # Wait for the payment method radio button to be clickable
        payment_method_radio_button = WebDriverWait(chrome_driver, 10).until(
            EC.element_to_be_clickable((By.ID, "input-payment-method-cod-cod"))
        )
        # Click the radio button to select the payment method (e.g., COD)
        payment_method_radio_button.click()

        time.sleep(1)

        # Wait for the 'Continue' button to be clickable
        continue_payment_button = WebDriverWait(chrome_driver, 10).until(
            EC.element_to_be_clickable((By.ID, "button-payment-method"))
        )
        # Click the 'Continue' button
        continue_payment_button.click()

        time.sleep(1)

        # Optionally, wait for a confirmation or success message that the payment method has been applied
        WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-success"))
        )

        # Step 5: Add Comments About Your Order
        comment_field = WebDriverWait(chrome_driver, 10).until(
            EC.element_to_be_clickable((By.ID, "input-comment"))
        )

        chrome_driver.execute_script("arguments[0].scrollIntoView(true);", comment_field)
        time.sleep(1)
        comment_field.send_keys("Please double-check the item before shipping. Thanks!")

        time.sleep(2)

        # Step 6: Extract and Print Order Summary
        order_summary_table = WebDriverWait(chrome_driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-bordered.table-hover"))
        )

        print("CHECKOUT PAGE")
        # Extract product details from the table
        rows = order_summary_table.find_elements(By.XPATH, ".//tbody/tr")
        for row in rows:
            product_name = row.find_element(By.CSS_SELECTOR, ".text-start").text
            total_price = row.find_element(By.CSS_SELECTOR, ".text-end").text
            print(f"Product: {product_name} | Total: {total_price}")

        # Extract footer values like Sub-Total, Shipping, and Total
        footer = order_summary_table.find_element(By.XPATH, ".//tfoot")
        sub_total = footer.find_element(By.XPATH, ".//tr[1]/td[2]").text
        shipping = footer.find_element(By.XPATH, ".//tr[2]/td[2]").text
        total = footer.find_element(By.XPATH, ".//tr[3]/td[2]").text

        print(f"\nOrder Summary:")
        print(f"Sub-Total: {sub_total}")
        print(f"Flat Shipping Rate: {shipping}")
        print(f"Total: {total}")

        print("-" * 40)
        print("-" * 40)

        # Step 6: Confirm Order
        confirm_button = WebDriverWait(chrome_driver, 10).until(
            EC.element_to_be_clickable((By.ID, "button-confirm"))
        )

        chrome_driver.execute_script("arguments[0].scrollIntoView(true);", confirm_button)

        time.sleep(2)

        actions = ActionChains(chrome_driver)
        actions.move_to_element(confirm_button).click().perform()

        WebDriverWait(chrome_driver, 10).until(
            EC.url_to_be(navigate_to_checkout_success(chrome_driver))
        )

        # ========================
        # DASHBOARD PAGE
        # ========================

        # Step 1: Access the dashboard page
        dashboard_url = navigate_to_dashboard(chrome_driver)
        chrome_driver.get(dashboard_url)

        # Step 2: Close the alert pop-up (assuming it's a Bootstrap modal close button)
        close_button = chrome_driver.find_element(By.CSS_SELECTOR, "button.btn-close[data-bs-dismiss='alert']")
        close_button.click()

        # Step 3: Login
        username_input = chrome_driver.find_element(By.CSS_SELECTOR, "input#input-username")
        password_input = chrome_driver.find_element(By.CSS_SELECTOR, "input#input-password")

        # Enter credentials
        username_input.send_keys("admin")
        # time.sleep(2)
        password_input.send_keys("admin")
        # time.sleep(2)

        # Submit login form
        login_button = chrome_driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")
        login_button.click()

        # Wait for the page to load after login
        time.sleep(3)

        # Verify if redirected to the correct dashboard page
        assert "route=common/dashboard" in chrome_driver.current_url, "Login failed or incorrect redirection."

        # Step 4: Close modal (if exists)
        modal_close_button = chrome_driver.find_element(By.CSS_SELECTOR, "button.btn-close[data-bs-dismiss='modal']")
        modal_close_button.click()

        # Scroll to the bottom of the page
        chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        print("DASHBOARD PAGE")

        # Step 6: Locate and verify Latest Orders
        orders_table = chrome_driver.find_element(By.CSS_SELECTOR, "div.card.mb-3 .table tbody")
        order_rows = orders_table.find_elements(By.TAG_NAME, "tr")

        # Check if there are any order rows
        if order_rows:
            # Access the first row and print the details
            first_order = order_rows[0]

            order_id = first_order.find_element(By.CSS_SELECTOR, "td.text-end").text
            customer_name = first_order.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
            order_status = first_order.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
            date_added = first_order.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text
            total_amount = first_order.find_element(By.CSS_SELECTOR, "td.text-end:nth-child(5)").text

            # Print the first order details
            print(f"Order ID: {order_id}")
            print(f"Customer: {customer_name}")
            print(f"Status: {order_status}")
            print(f"Date Added: {date_added}")
            print(f"Total: {total_amount}")
            print("-" * 40)

            # Compare the total from the order summary and the admin order table
            print(f"Comparing checkout total ({total}) with admin total ({total_amount}):")

            if total == total_amount:
                print("The totals match!")
            else:
                print(f"The totals do not match: {total} != {total_amount}")

        time.sleep(5)

    except Exception as e:
        print(f"Error while confirming order: {e}")


def test_product_addition_and_checkout_without_login(chrome_driver):
    try:
        # ========================
        # PRODUCT PAGE
        # ========================

        # Product details for testing
        products = [
            {
                "url": navigate_to_product_macbook(chrome_driver),
                "name": "MacBook",
            }
        ]

        for product in products:
            # Access the product page
            chrome_driver.get(product["url"])
            WebDriverWait(chrome_driver, 10).until(
                EC.presence_of_element_located((By.ID, "input-quantity"))
            )
            # print(f"Accessed product page: {product['url']}")

            # Random quantity from 1 to 10
            random_quantity = random.randint(1, 10)
            quantity_field = chrome_driver.find_element(By.ID, "input-quantity")
            quantity_field.clear()  # Clear the field before entering new quantity
            quantity_field.send_keys(str(random_quantity))

            # Extract the new price and ex-tax price
            try:
                new_price_text = chrome_driver.find_element(By.CSS_SELECTOR, ".price-new").text
                # Remove any non-numeric characters (currency symbol and commas)
                new_price = float(new_price_text.replace('$', '').replace(',', ''))

                # Calculate total price
                total_price = new_price * random_quantity

                # Format the total price with commas and two decimal places
                formatted_total_price = f"${total_price:,.2f}"

                print(f"\nProduct: {product['name']}")
                print(f"Price/{product['name']}: {new_price_text}")
                print(f"Qty: {random_quantity}")
                print(f"==> Total Price: {formatted_total_price}")
            except Exception as e:
                print(f"Error extracting price details for {product['name']}: {e}")

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
            except Exception as e:
                print(f"Error while verifying success message for {product['name']}: {e}")

        print("-" * 40)

        # ========================
        # CHECKOUT PAGE (DON'T LOGIN)
        # ========================

        # Step 1: Clicking the Checkout link
        WebDriverWait(chrome_driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-success"))
        )

        # Click the Checkout link
        checkout_link = WebDriverWait(chrome_driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[title='Checkout']"))
        )
        checkout_link.click()

        # Wait for the checkout page to load (use more flexible URL check)
        WebDriverWait(chrome_driver, 10).until(
            EC.url_contains("route=checkout/checkout")
        )

        # Step 2: Wait for the Guest Checkout radio button and select it
        guest_checkout_radio_button = WebDriverWait(chrome_driver, 10).until(
            EC.element_to_be_clickable((By.ID, "input-guest"))
        )
        # Click the "Guest Checkout" radio button
        guest_checkout_radio_button.click()

        time.sleep(2)

        # Step 3: Scroll down to the bottom of the page
        chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        # Wait for the order summary table to be visible
        WebDriverWait(chrome_driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-bordered.table-hover"))
        )

        # Step 4: Extract order summary from the table
        order_summary_table = chrome_driver.find_element(By.CSS_SELECTOR, ".table.table-bordered.table-hover")

        # Extract product details (Product Name and Total)
        rows = order_summary_table.find_elements(By.XPATH, ".//tbody/tr")
        print("Order Summary:")
        for row in rows:
            product_name = row.find_element(By.CSS_SELECTOR, ".text-start").text
            total_price = row.find_element(By.CSS_SELECTOR, ".text-end").text
            print(f"Product: {product_name} | Total: {total_price}")


        # Extract footer values like Sub-Total, Eco Tax, VAT, and Total
        footer = order_summary_table.find_element(By.XPATH, ".//tfoot")
        sub_total = footer.find_element(By.XPATH, ".//tr[1]/td[2]").text
        eco_tax = footer.find_element(By.XPATH, ".//tr[2]/td[2]").text
        vat = footer.find_element(By.XPATH, ".//tr[3]/td[2]").text
        total = footer.find_element(By.XPATH, ".//tr[4]/td[2]").text

        # Print footer values
        print(f"\nOrder Summary Footer:")
        print(f"Sub-Total: {sub_total}")
        print(f"Eco Tax: {eco_tax}")
        print(f"VAT: {vat}")
        print(f"Total: {total}")

        print("-" * 40)

        # Format the order footer total
        formatted_footer_total = float(total.replace('$', '').replace(',', ''))

        # Compare the formatted total price with the total from the footer
        if formatted_total_price == f"${formatted_footer_total:,.2f}":
            print(
                f"Success: The calculated total price {formatted_total_price} matches the order summary total {total}.")
        else:
            print(
                f"Error: The calculated total price {formatted_total_price} does not match the order summary total {total}.")

    except Exception as e:
        print(f"Error while confirming order: {e}")

    time.sleep(5)


def test_compare_product_info(chrome_driver):
    # ========================
    # PRODUCT PAGE
    # ========================

    # Truy cập trang chi tiết sản phẩm
    product_url = navigate_to_product_iphone(chrome_driver)
    chrome_driver.get(product_url)

    # Lấy thông tin từ trang chi tiết sản phẩm
    product_name = chrome_driver.find_element(By.TAG_NAME, 'h1').text
    price_new = chrome_driver.find_element(By.CSS_SELECTOR, '.price-new').text
    price_new_value = float(price_new.replace('$', '').replace(',', '').strip())  # Convert price to float

    # Lấy thêm thông tin khác từ trang
    brand = chrome_driver.find_element(By.XPATH, "//li[contains(text(), 'Brand')]").text
    product_code = chrome_driver.find_element(By.XPATH, "//li[contains(text(), 'Product Code')]").text
    availability = chrome_driver.find_element(By.XPATH, "//li[contains(text(), 'Availability')]").text

    # Chọn một số lượng ngẫu nhiên từ 1 đến 5
    quantity = random.randint(2, 10)
    quantity_input = chrome_driver.find_element(By.ID, 'input-quantity')
    quantity_input.clear()  # Xóa giá trị cũ
    quantity_input.send_keys(str(quantity))  # Nhập số lượng ngẫu nhiên

    # Nhấn nút "Add to Cart"
    add_to_cart_button = chrome_driver.find_element(By.ID, 'button-cart')
    add_to_cart_button.click()

    # Đợi giỏ hàng được cập nhật
    time.sleep(2)

    # Truy cập vào trang giỏ hàng
    navigate_to_shopping_cart(chrome_driver)

    # In thông tin sản phẩm ra terminal
    print("\nPRODUCT PAGE:")
    print(f"Name: {product_name}")
    print(f"Price: {price_new}")
    print(f"{brand}")
    print(f"{product_code}")
    print(f"{availability}")
    print(f"Quantity Added: {quantity}")

    print("-" * 40)

    # Nhấn vào nút giỏ hàng để xem chi tiết
    shopping_cart_button = chrome_driver.find_element(By.LINK_TEXT, "Shopping Cart")
    shopping_cart_button.click()

    # Đợi trang giỏ hàng tải
    time.sleep(2)

    # Lấy thông tin từ trang giỏ hàng
    cart_items = chrome_driver.find_elements(By.XPATH, "//div[@id='shopping-cart']//tbody/tr")

    # ========================
    # SHOPPING CART PAGE
    # ========================

    # In thông tin sản phẩm trong giỏ hàng
    print("\nSHOPPING CART PAGE:")
    for item in cart_items:
        item_name = item.find_element(By.XPATH, ".//td[contains(@class, 'text-start')]//a").text
        item_model = item.find_element(By.XPATH, ".//td[contains(@class, 'text-start') and not(contains(text(), 'Quantity'))]").text
        item_quantity = item.find_element(By.XPATH, ".//td[contains(@class, 'text-start')]//input[@name='quantity']").get_attribute('value')
        item_price = item.find_element(By.XPATH, ".//td[@class='text-end'][1]").text
        item_price_value = float(item_price.replace('$', '').replace(',', '').strip())  # Convert item price to float
        item_total = item.find_element(By.XPATH, ".//td[@class='text-end'][2]").text

        # In thông tin từng sản phẩm
        print(f"Name: {item_name}, Model: {item_model}, Quantity: {item_quantity}, Unit Price: {item_price}, Total: {item_total}")

        # Lấy thông tin tổng giá trong giỏ hàng
        totals = chrome_driver.find_elements(By.XPATH, "//tfoot[@id='checkout-total']//tr")
        for total in totals:
            total_description = total.find_element(By.XPATH, ".//td[contains(@class, 'text-end')][1]").text
            total_value = total.find_element(By.XPATH, ".//td[contains(@class, 'text-end')][2]").text
            print(f"{total_description}: {total_value}")

        print("-" * 40)
        print("-" * 40)

        # So sánh thông tin sản phẩm
        print("\nCOMPARING PRODUCT DETAILS:")
        print(f"Name: {product_name} vs Name: {item_name}")
        print(f"Price: {price_new} vs Unit Price: {item_price}")
        print(f"Quantity Added: {quantity} vs Quantity: {item_quantity}")

        # So sánh và in ra kết quả
        if product_name == item_name:
            print("Product name matches!")
        else:
            print("Product name does not match!")

        if price_new_value == item_price_value:
            print("Product price matches!")
        else:
            print("Product price does not match!")

        if quantity == int(item_quantity):
            print("Quantities match!")
        else:
            print("Quantities do not match!")

        print("\n")

    time.sleep(5)