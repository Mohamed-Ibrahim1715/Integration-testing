import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_successful_registration(driver):
    driver.get("http://localhost:5000/register")
    driver.find_element(By.NAME, "username").send_keys("moMOHAMEDSE")
    driver.find_element(By.NAME, "password").send_keys("moMOHAMEDSE")
    driver.find_element(By.XPATH, "//button").click()
    WebDriverWait(driver, 10).until(EC.url_to_be("http://localhost:5000/success"))
    assert "Well done" in driver.page_source

def test_failed_registration_existing_user(driver):
    driver.get("http://localhost:5000/register")
    driver.find_element(By.NAME, "username").send_keys("moMOHAMEDSE")  # Using the same username
    driver.find_element(By.NAME, "password").send_keys("moMOHAMEDSE")
    driver.find_element(By.XPATH, "//button").click()
    # Assuming you have an error handling mechanism to stay on the same page and show a message
    assert "Username already exists" in driver.page_source
    assert driver.current_url == "http://localhost:5000/register"