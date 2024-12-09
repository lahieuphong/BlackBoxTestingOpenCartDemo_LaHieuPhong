from datetime import datetime
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common import TimeoutException

from utils.base_driver import chrome_driver
from pages.navigate_page import navigate_to_homepage, navigate_to_product_macbook, navigate_to_login, navigate_to_forgotten, navigate_to_checkout_success, navigate_to_product_hp_lp3065
from pages.login_page import login_success_chrome, count_account_menu_items


# BUG: Mất Session Sau Khi Quay Lại (Back Navigation)
def test_lost_session_when_navigating_back_from_order_creation(chrome_driver):
    # First, login successfully
    print("Step 1: Logging in...")
    login_success_chrome(chrome_driver)
    my_account_dropdown = chrome_driver.find_element(By.CSS_SELECTOR, "a.dropdown-toggle i.fa-user")
    my_account_dropdown.click()
    time.sleep(2)  # Wait for dropdown to open

    item_count = count_account_menu_items(chrome_driver)
    assert item_count == 5, f"Expected 5 menu items in My Account dropdown, but found {item_count}. Login likely failed."

    # Navigate to 'Order History' page by clicking the 'Order History' link
    print("Step 2: Navigating to Order History page...")
    order_history_link = chrome_driver.find_element(By.CSS_SELECTOR, "a.dropdown-item[href*='route=account/order']")
    order_history_link.click()
    time.sleep(2)  # wait for the page to load

    # Check if we are on the order history page
    assert "order" in chrome_driver.current_url, "Failed to navigate to Order History page"
    print(f"Navigated to Order History page. Current URL: {chrome_driver.current_url}")

    # Click on the 'View' button to view order details
    print("Step 3: Clicking on the 'View' button for order details...")
    view_button = chrome_driver.find_element(By.CSS_SELECTOR, "a.btn.btn-info")
    view_button.click()
    time.sleep(2)  # wait for the order details page to load

    # Check if we are on the order details page
    assert "order.info" in chrome_driver.current_url, "Failed to navigate to order details page"
    print(f"Navigated to Order Details page. Current URL: {chrome_driver.current_url}")

    # After navigating to the order details page (Step 7 complete)
    print("Step 4: Scrolling down to ensure 'Return' button is visible...")
    # Scroll down to make sure the 'Return' button is visible (you can also use JavaScript scroll)
    chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)  # wait for scroll to complete

    # Find and click on the 'Return' button
    print("Step 5: Clicking on the 'Return' button to initiate a return request...")
    return_button = chrome_driver.find_element(By.CSS_SELECTOR, "a.btn.btn-danger")
    chrome_driver.execute_script("arguments[0].click();", return_button)
    time.sleep(2)  # wait for the return page to load

    # Check if we are on the return page
    assert "returns.add" in chrome_driver.current_url, "Failed to navigate to return page"
    print(f"Navigated to Return page. Current URL: {chrome_driver.current_url}")

    # Scroll down again to ensure the 'Back' button is visible
    print("Step 6: Scrolling down to ensure 'Back' button is visible...")
    chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)  # wait for scroll to complete

    # Find and click on the 'Back' button
    print("Step 7: Clicking on the 'Back' button to return to the previous page...")
    back_button = chrome_driver.find_element(By.CSS_SELECTOR, "a.btn.btn-light")
    back_button.click()
    time.sleep(2)  # wait for the back navigation to complete

    # Check if we're redirected to the login page
    assert "login" in chrome_driver.current_url, "Session should be lost and redirected to login page"
    print(f"Redirected to login page. Current URL: {chrome_driver.current_url}")

    time.sleep(5)


# BUG: Giao Diện Người Dùng (UI) Bị Vỡ Khi Tìm Kiếm Với 1 Chuỗi Từ Khoá Quá Dài
def test_search_invalid_long_term(chrome_driver):
    # Step 1: Navigate to the homepage
    navigate_to_homepage(chrome_driver)

    # Step 2: Use a long search term (not a valid product)
    search_box = chrome_driver.find_element(By.NAME, "search")
    search_term = "A" * 255  # Using a very long string to simulate an invalid search
    search_box.send_keys(search_term)
    time.sleep(1)  # Wait after entering the keyword
    print(f"Entered '{search_term}' into the search box.")

    # Step 3: Click the search button
    search_button = chrome_driver.find_element(By.CSS_SELECTOR, "button.btn.btn-light.btn-lg")
    search_button.click()
    time.sleep(5)  # Wait for the search results page to load
    print("Clicked the search button and navigated to the results page.")

    # Step 4: Verify the URL of the search results page
    expected_url = f"http://localhost/demo/index.php?route=product/search&language=en-gb&search={search_term}"
    actual_url = chrome_driver.current_url
    assert actual_url == expected_url, f"Expected URL to be '{expected_url}', but got '{actual_url}'"
    print(f"Verified URL: {actual_url}")

    # Step 5: Verify the search result heading
    search_heading = chrome_driver.find_element(By.TAG_NAME, "h1").text
    expected_heading = f"Search - {search_term}"
    assert search_heading == expected_heading, f"Expected heading '{expected_heading}', but got '{search_heading}'"
    print(f"Verified heading: '{search_heading}'")

    # Step 6: Verify that the 'no product matches' message appears
    try:
        no_results_message = chrome_driver.find_element(By.XPATH, "//p[contains(text(), 'There is no product that matches the search criteria.')]").text
        expected_message = "There is no product that matches the search criteria."
        assert no_results_message == expected_message, f"Expected message '{expected_message}', but got '{no_results_message}'"
        print(f"Verified 'no product matches' message: '{no_results_message}'")
    except Exception as e:
        print("No 'no product matches' message found, UI might be broken:", e)

    # Step 7: Scroll horizontally to the end of the page
    print("Scrolling horizontally to the end of the page...")
    chrome_driver.execute_script("window.scrollTo(0, 0);")  # Scroll to top first if needed
    chrome_driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);")  # Scroll horizontally to the end of the page

    time.sleep(5)  # Wait after scrolling


# BUG: Nhập Vượt Quá Số Lượng Sản Phẩm Trong Giỏ Hàng
def test_error_page_displayed_when_adding_product_to_cart_fails(chrome_driver):
    # Step 1: Navigate to the product page
    driver = chrome_driver
    navigate_to_product_macbook(chrome_driver)
    print("Navigated to the product page.")

    # Step 2: Find the quantity input field and set the value to an extremely large number
    quantity_field = driver.find_element(By.ID, "input-quantity")
    quantity_field.clear()  # Clear any existing value
    quantity_field.send_keys("2147483648")
    print("Entered the quantity: 2147483648")

    # Step 3: Find the 'Add to Cart' button and click it
    add_to_cart_button = driver.find_element(By.ID, "button-cart")
    add_to_cart_button.click()
    print("Clicked on 'Add to Cart' button.")

    # Step 4: Wait for a moment for the response to show up (could be replaced with explicit wait)
    time.sleep(2)  # This could be replaced with a more explicit wait for an element

    # Step 5: Check the success message
    try:
        success_message = driver.find_element(By.CSS_SELECTOR, ".alert-success")
        print(f"Success message: {success_message.text}")
    except Exception as e:
        print(f"Error finding success message: {e}")

    # Step 6: Check the cart button and print the cart content
    cart_button = driver.find_element(By.CSS_SELECTOR, "button[data-bs-toggle='dropdown']")
    cart_text = cart_button.text
    print(f"Cart button text: {cart_text}")

    # Step 7: Verify that the cart content message is showing the extremely high item quantity
    assert "2147483647 item(s)" in cart_text, f"Expected cart to show '2147483647 item(s)', but found: {cart_text}"
    print("Verified the cart button shows the expected number of items.")


# BUG: Nhập Số Âm Lượng Sản Phẩm Trong Giỏ Hàng
def test_error_page_displayed_when_adding_product_with_negative_quantity(chrome_driver):
    # Step 1: Navigate to the product page
    driver = chrome_driver
    navigate_to_product_macbook(chrome_driver)
    print("Navigated to the product page.")

    # Step 2: Find the quantity input field and set the value to a negative number (-1)
    quantity_field = driver.find_element(By.ID, "input-quantity")
    quantity_field.clear()  # Clear any existing value
    quantity_field.send_keys("-1")
    print("Entered the quantity: -1")

    # Step 3: Find the 'Add to Cart' button and click it
    add_to_cart_button = driver.find_element(By.ID, "button-cart")
    add_to_cart_button.click()
    print("Clicked on 'Add to Cart' button.")

    # Step 4: Wait for the error message to appear
    try:
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-danger"))
        )
        print(f"Error message: {error_message.text}")
    except TimeoutException:
        print("Error message did not appear within the wait time.")

    # Step 5: Check the cart button and print the cart content
    cart_button = driver.find_element(By.CSS_SELECTOR, "button[data-bs-toggle='dropdown']")
    cart_text = cart_button.text
    print(f"Cart button text: {cart_text}")

    # Step 6: Verify that the cart button shows '0 item(s) - $0.00'
    assert "0 item(s)" in cart_text, f"Expected cart to show '0 item(s)', but found: {cart_text}"
    assert "$0.00" in cart_text, f"Expected cart to show '$0.00', but found: {cart_text}"
    print("Verified the cart button shows '0 item(s) - $0.00' after attempting to add a negative quantity.")


# BUG: Hệ Thống Quay Lại Trang Login Mà Không Hiển Thị Trang Nhập Mật Khẩu Mới Sau Khi Người Dùng Yêu Cầu Đặt Lại Mật Khẩu
def test_password_reset_redirect_without_new_password_field(chrome_driver):
    # Step 1: Navigate to the login page
    print("Step 1: Navigating to login page...")
    navigate_to_login(chrome_driver)
    # Wait for the page to load and ensure the "Email Address" field is visible
    WebDriverWait(chrome_driver, 10).until(
        EC.visibility_of_element_located((By.ID, "input-email"))
    )

    # Step 2: Enter email into the "Email Address" field
    print("Step 2: Entering email address...")
    email_input = chrome_driver.find_element(By.ID, "input-email")
    email_input.send_keys("hieuphong144@gmail.com")
    time.sleep(2)

    # Wait for the input value to be populated
    WebDriverWait(chrome_driver, 2).until(
        lambda driver: email_input.get_attribute("value") == "hieuphong144@gmail.com"
    )

    # Step 3: Click on the "Forgotten Password" link
    print("Step 3: Clicking on 'Forgotten Password' link...")
    forgotten_password_link = WebDriverWait(chrome_driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Forgotten Password"))
    )
    forgotten_password_link.click()

    # Step 4: Wait for the page to redirect and check the URL
    print("Step 4: Checking the redirect URL...")
    WebDriverWait(chrome_driver, 10).until(
        EC.url_contains("account/forgotten")
    )

    # Verify the current URL matches the expected URL
    expected_url = navigate_to_forgotten(chrome_driver)
    current_url = chrome_driver.current_url
    assert current_url == expected_url, f"Expected URL '{expected_url}', but got '{current_url}'"

    print(f"Test passed! Current URL: {current_url}")

    time.sleep(2)

    # Step 5: Enter email address again in the forgotten password page
    print("Step 5: Entering email address in the forgotten password page...")
    email_input_forgotten = WebDriverWait(chrome_driver, 10).until(
        EC.visibility_of_element_located((By.ID, "input-email"))
    )
    email_input_forgotten.send_keys("hieuphong144@gmail.com")
    time.sleep(2)

    # Step 6: Click the "Continue" button
    print("Step 6: Clicking on the 'Continue' button...")
    continue_button = WebDriverWait(chrome_driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
    )
    continue_button.click()
    time.sleep(1)

    # Step 7: Wait for the success message to appear after clicking "Continue"
    print("Step 7: Waiting for success message to appear...")
    WebDriverWait(chrome_driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert.alert-success"))
    )

    # Step 8: Assert that the success message is displayed
    success_message = chrome_driver.find_element(By.CSS_SELECTOR, "div.alert.alert-success")
    assert success_message.is_displayed(), "Success message was not displayed!"

    # Verify the content of the success message
    assert "Your password has been successfully updated" in success_message.text, \
        f"Expected success message, but got: {success_message.text}"

    print(f"Test passed! Message: {success_message.text}")

    time.sleep(5)


# BUG: Lỗi "Delivery Date" Nhưng Vẫn Checkout Thành Công
def test_check_delivery_date_with_error_handling(chrome_driver):
    print("\nPRODUCT 'HP LP3065' PAGE:")
    # Truy cập trang sản phẩm
    navigate_to_product_hp_lp3065(chrome_driver)

    # Lấy tên sản phẩm
    product_name = chrome_driver.find_element(By.XPATH, "//div[@class='col-sm']/h1").text
    print(f"Product Name: {product_name}")

    # Lấy thông tin trong danh sách đầu tiên
    details = chrome_driver.find_elements(By.XPATH, "//div[@class='col-sm']//ul[@class='list-unstyled'][1]/li")
    for detail in details:
        print(detail.text)

    # Lấy giá sản phẩm
    price = chrome_driver.find_element(By.XPATH, "//div[@class='col-sm']//span[@class='price-new']").text
    print(f"Price: {price}")

    # Lấy giá trước thuế (Ex Tax)
    ex_tax = chrome_driver.find_element(By.XPATH, "//div[@class='col-sm']//li[contains(text(),'Ex Tax')]").text
    print(f"Ex Tax: {ex_tax}")

    # Lấy giá quy đổi reward points
    reward_points_price = chrome_driver.find_element(
        By.XPATH, "//div[@class='col-sm']//li[contains(text(),'Price in reward points')]"
    ).text
    print(f"{reward_points_price}")

    # Lấy trạng thái sản phẩm (Availability)
    availability = chrome_driver.find_element(By.XPATH,
                                              "//div[@class='col-sm']//li[contains(text(),'Availability')]").text
    print(f"{availability}")

    # Lấy thông tin trong form "Available Options"
    print(f"\nAvailable Options:")
    delivery_date_label = chrome_driver.find_element(By.XPATH,
                                                     "//form[@id='form-product']//label[@for='input-option-225']").text
    delivery_date_value = chrome_driver.find_element(By.XPATH,
                                                     "//form[@id='form-product']//input[@id='input-option-225']").get_attribute(
        "value")
    print(f"{delivery_date_label}: {delivery_date_value}")



    # Chuyển delivery_date_value thành kiểu datetime để so sánh với ngày thực tế
    delivery_date = datetime.strptime(delivery_date_value, "%Y-%m-%d")
    current_date = datetime.now()

    print(f"-" * 40)
    # In ra ngày hôm nay
    print(f"Today's date is: {current_date.strftime('%Y-%m-%d')}")

    # So sánh ngày giao hàng với ngày hiện tại
    if delivery_date < current_date:
        # Nếu ngày giao hàng trong quá khứ, thông báo cảnh báo
        print(f"Warning: The delivery date {delivery_date_value} is in the past!")
        # Bạn có thể ném một exception ở đây hoặc xử lý theo cách khác nếu muốn.
    else:
        print(f"The delivery date {delivery_date_value} is valid and in the future.")

    print(f"-" * 40)



    # Lấy thông tin số lượng (Qty)
    qty_label = chrome_driver.find_element(By.XPATH, "//form[@id='form-product']//label[@for='input-quantity']").text
    qty_value = chrome_driver.find_element(By.XPATH, "//form[@id='form-product']//input[@id='input-quantity']").get_attribute("value")
    print(f"{qty_label}: {qty_value}")

    # Cuộn xuống dưới cùng của trang
    chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Đợi một chút để trang load hoàn toàn

    # Nhấn nút "Add to Cart"
    add_to_cart_button = chrome_driver.find_element(By.ID, "button-cart")
    add_to_cart_button.click()

    # Đợi một chút để đảm bảo sản phẩm đã được thêm vào giỏ hàng
    time.sleep(5)

    # Lấy thông báo thành công
    alert_message_element = chrome_driver.find_element(By.CSS_SELECTOR, "#alert .alert-success")
    alert_message = alert_message_element.text.strip()

    # In ra thông báo thành công
    print(alert_message)

    # Cuộn lên trên cùng của trang
    chrome_driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)  # Đợi một chút để cuộn lên hoàn tất

    # Nhấn nút Checkout
    checkout_button = chrome_driver.find_element(By.XPATH, "//a[contains(@href, 'route=checkout/checkout')]")
    checkout_button.click()

    # Đợi một chút sau khi nhấn để trang Checkout load
    time.sleep(2)

    print("=" * 40)
    print("\nCHECKOUT PAGE: ")

    # Kiểm tra xem trang hiện tại có phải là trang checkout không
    current_url = chrome_driver.current_url
    assert current_url == "http://localhost/demo/index.php?route=checkout/checkout&language=en-gb", f"Expected URL 'http://localhost/demo/index.php?route=checkout/checkout&language=en-gb', but got {current_url}"

    # Chọn "Guest Checkout" (value = 1)
    guest_checkout_radio_button = chrome_driver.find_element(By.ID, "input-guest")
    guest_checkout_radio_button.click()

    # Điền thông tin vào các trường
    chrome_driver.find_element(By.ID, "input-firstname").send_keys("La Hiểu")
    chrome_driver.find_element(By.ID, "input-lastname").send_keys("Phong")
    chrome_driver.find_element(By.ID, "input-email").send_keys("hieuphong144@gmail.com")
    chrome_driver.find_element(By.ID, "input-shipping-company").send_keys("CÔNG TY CỔ PHẦN ĐẠI NAM")
    chrome_driver.find_element(By.ID, "input-shipping-address-1").send_keys("Số 1765A Đại lộ Bình Dương")
    chrome_driver.find_element(By.ID, "input-shipping-address-2").send_keys("Khu Du Lịch Đại Nam")
    chrome_driver.find_element(By.ID, "input-shipping-city").send_keys("Thành phố Thủ Dầu Một, Tỉnh Bình Dương")

    # Cuộn xuống để các trường còn lại có thể xuất hiện
    chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # Điền thêm thông tin vào các trường
    chrome_driver.find_element(By.ID, "input-shipping-postcode").send_keys("75000")

    # Chọn "Viet Nam" trong dropdown (value = 230)
    country_dropdown = chrome_driver.find_element(By.ID, "input-shipping-country")
    select_country = Select(country_dropdown)
    select_country.select_by_value("230")  # Chọn Viet Nam

    # Chọn "Binh Duong" trong dropdown zone (value = 3759)
    time.sleep(1)  # Đảm bảo dropdown zone đã được load
    zone_dropdown = chrome_driver.find_element(By.ID, "input-shipping-zone")
    select_zone = Select(zone_dropdown)
    select_zone.select_by_value("3759")  # Chọn Binh Duong

    # Đợi một chút để việc chọn zone hoàn tất
    time.sleep(1)

    # Chọn checkbox "Newsletter" nếu chưa được chọn
    newsletter_checkbox = chrome_driver.find_element(By.ID, "input-newsletter")
    if not newsletter_checkbox.is_selected():
        newsletter_checkbox.click()  # Chọn nếu chưa chọn

    # Nhấn nút "Continue"
    continue_button = chrome_driver.find_element(By.ID, "button-register")
    continue_button.click()

    # Đợi trang load sau khi nhấn
    time.sleep(2)

    # Cuộn ngược lên đầu trang
    chrome_driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)  # Đợi một chút để cuộn lên hoàn tất


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

    print(f"Order Summary:")
    print(f"Sub-Total: {sub_total}")
    print(f"Flat Shipping Rate: {shipping}")
    print(f"Total: {total}")

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

    time.sleep(5)