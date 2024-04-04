import re
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture(scope="module")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def perform_login(driver, username, password):
    driver.implicitly_wait(20)
    driver.find_element(By.ID, "email").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    login_button = driver.find_element(By.CSS_SELECTOR, 'input[type="button"][value="Login"]')
    login_button.click()


def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password):
    return (
        len(password) >= 8 and
        any(char.islower() for char in password) and
        any(char.isupper() for char in password) and
        any(char.isdigit() for char in password) and
        any(char in '@$!%*?&' for char in password)
    )


def is_success_message_green(browser):
    success_message = browser.find_element(By.ID, "validMsg")
    color = success_message.value_of_css_property("color")
    return "rgba(0, 128, 0, 1)" in color  # Green color


def is_error_message_red(browser):
    error_message = browser.find_element(By.ID, "errorMsgMail")
    color = error_message.value_of_css_property("color")
    return "rgba(255, 0, 0, 1)" in color  # Red color

def is_error_message_red_password(browser):
    error_message = browser.find_element(By.ID, "errorMsgPwd")
    color = error_message.value_of_css_property("color")
    return "rgba(255, 0, 0, 1)" in color  # Red color


@pytest.mark.selenium
# Login with valid credentials will fail since multiple bugs are found:
# 1. Valid message for Email is not displayed
# 2. Valid Password message is displayed for the Email field instead of Password field
# 3. Valid Passsword message is displayed in red identified as an error instead of green color message

def test_valid_second_login(browser):
    browser.get("http://127.0.0.1:5500/QA_Task.html")
    browser.implicitly_wait(20)

    # Initial login
    browser.find_element(By.ID, "candidateName").send_keys('Ciubotariu Mihai')
    browser.find_element(By.ID, "candidateMail").send_keys('Mihai@test.com')
    browser.find_element(By.ID, "startButton").click()

    # login with valid credentials
    perform_login(browser, 'validemail@test.com', 'ValidPass1!')

    # Validate successful login
    assert "Success" in browser.page_source
    assert is_success_message_green(browser)


@pytest.mark.parametrize("invalid_email", [
    "invalidemail",
    "invalidemail@",
    "invalidemail.com",
    "invalid@.com",
    "invalid@domain",
    "invalid@domain.",
    "invalid@domain.c",
    "invalid@domain.co.",
])
@pytest.mark.selenium
def test_invalid_email_second_login(browser, invalid_email):
    browser.get("http://127.0.0.1:5500/QA_Task.html")
    browser.implicitly_wait(20)

    # Initial login
    browser.find_element(By.ID, "candidateName").send_keys('Ciubotariu Mihai')
    browser.find_element(By.ID, "candidateMail").send_keys('Mihai@test.com')
    browser.find_element(By.ID, "startButton").click()

    # login with invalid email
    perform_login(browser, invalid_email, 'ValidPass1!')

    # Validate error message or failure to login
    assert "Error" in browser.page_source or "Invalid credentials" in browser.page_source
    assert is_error_message_red(browser)


@pytest.mark.parametrize("invalid_password", [
    "password",
    "password123",
    "Passw0rd",
    "PASSWORD!",
    "Password",
    "test",
])
@pytest.mark.selenium
def test_invalid_password_second_login(browser, invalid_password):
    browser.get("http://127.0.0.1:5500/QA_Task.html")
    browser.implicitly_wait(20)

    # Initial login
    browser.find_element(By.ID, "candidateName").send_keys('Ciubotariu Mihai')
    browser.find_element(By.ID, "candidateMail").send_keys('Mihai@test.com')
    browser.find_element(By.ID, "startButton").click()

    # login with invalid password
    perform_login(browser, 'validemail@test.com', invalid_password)

    # Validate error message or failure to login
    assert "Error" in browser.page_source or "Invalid credentials" in browser.page_source
    assert is_error_message_red_password(browser)
