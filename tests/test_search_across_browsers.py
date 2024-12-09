import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.base_driver import chrome_driver, firefox_driver
from pages.navigate_page import navigate_to_homepage


def test_open_home_page_chrome(chrome_driver):
    try:
        # Mở trang web
        navigate_to_homepage(chrome_driver)
        time.sleep(5)  # Đợi trang tải xong

        # Kiểm tra tiêu đề trang
        if chrome_driver.title == "Your Store":  # Thay tiêu đề trang cụ thể nếu cần
            print("\nTrang web đã mở thành công!")
        else:
            print("\nTrang web không mở thành công.")

        # Kiểm tra sự tồn tại của hình ảnh
        img_element = chrome_driver.find_element(By.CSS_SELECTOR, "img[alt='Your Store']")

        # Kiểm tra thuộc tính src của thẻ img
        img_src = img_element.get_attribute("src")
        if img_src == "http://localhost/demo/image/catalog/opencart-logo.png":
            print("Hình ảnh đã tải thành công!")
        else:
            print("Hình ảnh không tải thành công.")

    except Exception as e:
        print(f"Đã có lỗi xảy ra: {e}")

    chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")

    time.sleep(5)

def test_open_home_page_firefox(firefox_driver):
    try:
        # Mở trang web
        navigate_to_homepage(firefox_driver)

        # Chờ cho đến khi hình ảnh xuất hiện trên trang (timeout 10 giây)
        img_element = WebDriverWait(firefox_driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='Your Store']"))
        )

        # Kiểm tra tiêu đề trang
        if firefox_driver.title == "Your Store":  # Thay tiêu đề trang cụ thể nếu cần
            print("\nTrang web đã mở thành công!")
        else:
            print("\nTrang web không mở thành công.")

        # Kiểm tra thuộc tính src của thẻ img
        img_src = img_element.get_attribute("src")
        if img_src == "http://localhost/demo/image/catalog/opencart-logo.png":
            print("Hình ảnh đã tải thành công!")
        else:
            print("Hình ảnh không tải thành công.")

    except Exception as e:
        print(f"Đã có lỗi xảy ra: {e}")

    firefox_driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")

    time.sleep(5)