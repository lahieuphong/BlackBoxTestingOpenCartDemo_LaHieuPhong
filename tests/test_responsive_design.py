import time

import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.base_driver import chrome_driver
from pages.navigate_page import navigate_to_homepage


# Dùng parametrize để kiểm tra với các kích thước màn hình khác nhau
@pytest.mark.parametrize("width, height", [
    (320, 480),  # Thiết bị màn hình nhỏ, vd: iPhone 4s
    (480, 800),  # Thiết bị Android nhỏ, vd: Motorola Moto E, Sony Xperia U
    (600, 1024), # Màn hình tablet cỡ nhỏ, vd: iPad Mini 1, Amazon Kindle Fire
    (768, 1280), # Màn hình tablet, vd: iPad 2, Samsung Galaxy Tab 10.1
    (1366, 768), # Laptop phổ thông, vd: HP Pavilion, Lenovo IdeaPad
    (1920, 1080), # Màn hình Full HD, vd: laptop Dell XPS 13, TV Full HD
    (2560, 1440), # Màn hình Quad HD, vd: Samsung Galaxy S6, MacBook Pro
    (3840, 2160)  # Màn hình 4K, vd: Dell XPS 15
])

def test_check_ui_on_large_screen(chrome_driver, width, height):
    # Ghi lại thời gian bắt đầu tải trang
    start_time = time.time()

    # Thiết lập kích thước cửa sổ trình duyệt
    chrome_driver.set_window_size(width, height)
    print(f"\n\nKiểm tra với độ phân giải: {width}x{height}")

    # Mở trang web
    navigate_to_homepage(chrome_driver)  # URL bạn muốn kiểm tra

    # Đảm bảo trang đã tải xong
    WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )

    # Tính thời gian tải trang
    load_time = time.time() - start_time
    print(f"\nThời gian tải trang: {load_time:.2f} giây")

    # Kiểm tra xem thời gian tải có vượt quá 3 giây không
    assert load_time < 3, f"\nTrang tải quá lâu: {load_time:.2f} giây"

    # Kiểm tra các yếu tố quan trọng không bị kéo dài, chồng chéo
    try:
        # Kiểm tra xem phần tử header và footer có hiển thị đầy đủ không
        header = chrome_driver.find_element(By.TAG_NAME, 'header')
        footer = chrome_driver.find_element(By.TAG_NAME, 'footer')

        # Kiểm tra kích thước của header và footer
        print(f"\nHeader Height: {header.size['height']}")  # In chiều cao của header
        print(f"Footer Height: {footer.size['height']}")  # In chiều cao của footer

        assert header.size['height'] > 0, "Header bị ẩn hoặc không hiển thị đúng"
        assert footer.size['height'] > 0, "Footer bị ẩn hoặc không hiển thị đúng"

        # Kiểm tra các phần tử chính trên trang (thay bằng selector phù hợp)
        try:
            elements = chrome_driver.find_elements(By.CSS_SELECTOR, '.container')  # Thay đổi selector nếu cần
            print(f"Số lượng phần tử chính tìm thấy: {len(elements)}")  # In số lượng phần tử chính
            assert len(elements) > 0, "Các phần tử chính không hiển thị đúng"
        except Exception as e:
            pytest.fail(f"Không tìm thấy phần tử chính trên trang: {str(e)}")

    except Exception as e:
        pytest.fail(f"Kiểm tra giao diện thất bại: {str(e)}")

    # Kiểm tra tổng thể: chiều cao của trang không được vượt quá một giới hạn nào đó
    body_scroll_height = chrome_driver.execute_script("return document.body.scrollHeight")  # Lấy chiều cao trang
    window_inner_height = chrome_driver.execute_script("return window.innerHeight")  # Lấy chiều cao cửa sổ trình duyệt

    # Giới hạn chiều cao cho phép (có thể điều chỉnh tùy thuộc vào thiết bị)
    max_allowed_height = window_inner_height * 10  # Giới hạn chiều cao có thể được điều chỉnh, thử gấp 7 lần

    # In thông tin ra terminal để kiểm tra
    print(f"Chiều cao trang: {body_scroll_height}")
    print(f"Chiều cao cửa sổ trình duyệt: {window_inner_height}")
    print(f"Giới hạn chiều cao cho phép: {max_allowed_height}")

    # Kiểm tra xem chiều cao của trang có vượt quá giới hạn cho phép không
    assert body_scroll_height <= max_allowed_height, \
        f"Trang bị kéo dài quá nhiều ngoài vùng hiển thị. Chiều cao trang: {body_scroll_height}, " \
        f"Chiều cao cửa sổ: {window_inner_height}, Giới hạn cho phép: {max_allowed_height}"

    # Kiểm tra và cuộn trang nếu cần thiết
    if body_scroll_height > window_inner_height:
        chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Cuộn trang xuống dưới cùng

    # Kiểm tra lại sau khi cuộn trang: đảm bảo không có thanh cuộn thừa hoặc phần tử bị thiếu
    body_scroll_height_after = chrome_driver.execute_script("return document.body.scrollHeight")
    print(f"Chiều cao trang sau khi cuộn: {body_scroll_height_after}")
    assert body_scroll_height_after <= max_allowed_height, \
        f"Sau khi cuộn, trang vẫn bị kéo dài quá nhiều ngoài vùng hiển thị. " \
        f"Chiều cao trang: {body_scroll_height_after}, Giới hạn cho phép: {max_allowed_height}"

    time.sleep(5)