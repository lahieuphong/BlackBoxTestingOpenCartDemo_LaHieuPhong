# BlackBox Testing OpenCart Demo 

## Overview ✨
This project is a collection of black box tests for the OpenCart demo application. The tests focus on evaluating the application's functionality from an end-user perspective, ensuring that features such as adding items to the cart, checkout, and form submissions work as expected. The testing is done using Selenium WebDriver and Python-based frameworks to simulate user interactions with the site. The project also includes additional tests for error handling, responsive design, and cross-browser compatibility.

## Directory Structure ✨

```plaintext
BlackBoxTestingOpenCartDemo_LaHieuPhong/
├── assets/
│   └── style.css 
├── pages/
│   ├── add_to_cart_page.py
│   ├── add_to_cart_page.py
│   └── navigate_page.py
├── tests/
│   ├── conftest.py 
│   ├── test_add_to_cart.py     
│   ├── test_all_links_status_report.py  
│   ├── test_checkout_process.py    
│   ├── test_error_handling.py  
│   ├── test_form_submission.py     
│   ├── test_login_logout.py  
│   ├── test_responsive_design.py   
│   ├── test_search_across_browsers.py  
│   └── test_search_functionality.py
├── utils/
│   └── base_driver.py  
├── all_links_status_report.txt   
├── README.md 
├── report.html             
├── requirements.txt         
└── run_tests.py             
```

## Installation and Running Tests ✨

### Prerequisites 
- Python 3.x
- pip (Python package installer)
- Selenium
- WebDriver (ChromeDriver for Chrome, GeckoDriver from FireFox...)
- OpenCart running locally at http://localhost/demo/index.php?route=common/home&language=en-gb

### Setup 

1. **Clone the repository:**
   ```bash
   git clone <https://github.com/lahieuphong/BlackBoxTestingOpenCartDemo_LaHieuPhong.git>
   cd <BlackBoxTestingOpenCartDemo_LaHieuPhong>
    ```
   
2. **Install the required packages:**

    Run the following command to install all the required libraries from `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

3. **Setting Up WebDriver**

   - **Chrome**: You will need `ChromeDriver`.
   - **Firefox**: You can download `GeckoDriver`.

   Once downloaded, ensure the appropriate WebDriver executable is placed in your system's PATH or specify its location in the `base_driver.py` file.

### Running Tests

You can run all tests by using the `run_tests.py` script:

   ```bash
   python run_tests.py
   ```

Alternatively, you can run specific tests using `pytest`. For example, to run the tests related to the Add to Cart functionality:

   ```bash
   pytest tests/test_add_to_cart.py
   ```
The test results will be generated in an `HTML` format and stored in the `report.html` file.

### Notes

- Ensure that the WebDriver executable (`chromedriver`, `firefoxdrive`...) is in your system's PATH or specify its location in your test setup.
- You can customize the test configurations and add more test cases as needed.

## Project Structure ✨

- `tests/`: Contains all the test cases.
- `pages/`: Contains page object models for different pages of the OpenCart demo website.
- `utils/`: Contains utility files and configurations.

## Test Details ✨

1. **Test Add to Cart (`test_add_to_cart.py`)**
- Verifies that users can successfully add items to the shopping cart.

2. **Test All Links Status (`test_all_links_status_report.py`)**
- Checks the status of all the links on the page to ensure none are broken.
- The results are saved in all_links_status_report.txt.

3. **Test Checkout Process (`test_checkout_process.py`)**
- Tests the end-to-end checkout process, ensuring users can complete a purchase.

4. **Test Error Handling (`test_error_handling.py`)**
- Verifies that the system handles invalid inputs and errors gracefully.

5. **Test Form Submission (`test_form_submission.py`)**
- Tests forms like login, contact, and registration to ensure successful submission.

6. **Test Login/Logout (`test_login_logout.py`)**
- Verifies the login and logout functionalities of the OpenCart demo.

7. **Test Responsive Design (`test_responsive_design.py`)**
- Verifies that the website is responsive and adjusts to different screen sizes and devices.

8. **Test Search Functionality (`test_search_functionality.py`)**
- Tests that the search bar works as expected by returning relevant results.

9. **Test Cross-Browser Search (`test_search_across_browsers.py`)**
- Ensures the search functionality is consistent across different browsers.

## Page Object Model ✨

This project follows the **Page Object Model (POM)** design pattern for better maintainability and readability. The key page files in `pages/` represent different parts of the website and abstract the interaction with those parts:

- `add_to_cart_page.py`: Contains methods for interacting with the **Add to Cart** page elements.
- `navigate_page.py`: Contains navigation-related actions.

## Test Reporting ✨
After running the tests, an **HTML** report is generated (`report.html`). This report provides a detailed overview of the test results, including:

- The number of tests **passed**/**failed**
- A summary of each test case
- Screenshots (if any failures occur)

## Utilities ✨
### BaseDriver (`base_driver.py`)
The BaseDriver class in the `utils/` directory is responsible for setting up and managing the **WebDriver** instance. It is used across all tests to initiate and close the browser. The class supports both **Chrome** and **Firefox** browsers.

## Contributing ✨
1. **Fork the repository.**
2. **Create a new branch.**
    ```bash
    git checkout -b feature/your-feature
    ```
3. **Make your changes.**
4. **Commit your changes.**
    ```bash
   git commit -am 'Add new feature'
   ```
5. **Push to the branch**
    ```bash
   git push origin feature/your-feature
   ```
6. **Create a new Pull Request.**

## License ✨
This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgments ✨
- **Selenium WebDriver** for browser automation.
- `pytest` for test management.
- OpenCart for providing the demo site for testing.

## Contacts ✨
* Email: **hieuphong144@gmail.com**
* Project Link: https://github.com/lahieuphong/BlackBoxTestingOpenCartDemo_LaHieuPhong

### --- THE END ---
