import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

@pytest.fixture
def driver():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    options = Options()
    #options.add_argument("--headless")  # для CI
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, service=service)
    yield driver
    driver.quit()

def login(driver):
    driver.get("https://magento.softwaretestingboard.com/")
    wait = WebDriverWait(driver, 10)
    login_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "li.authorization-link a"))
    )
    login_button.click()

    email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='email']")))
    email_field.send_keys("ddzon9188@gmail.com")
    driver.find_element(By.XPATH, "//*[@id='pass']").send_keys("tp6Z21#17")
    driver.find_element(By.XPATH, "//*[@id='send2']").click()
    wait.until(EC.url_to_be("https://magento.softwaretestingboard.com/"))
    assert "magento.softwaretestingboard" in driver.current_url

def go_to_jacket(driver):
    wait = WebDriverWait(driver, 20)
    ActionChains(driver).move_to_element(wait.until(
        EC.visibility_of_element_located((By.ID, "ui-id-4"))
    )).perform()
    ActionChains(driver).move_to_element(wait.until(
        EC.visibility_of_element_located((By.ID, "ui-id-9"))
    )).perform()
    hoodies_choice = wait.until(
        EC.presence_of_element_located((By.ID, "ui-id-12"))
    )
    ActionChains(driver).move_to_element(hoodies_choice).perform()
    hoodies_choice.click()
    assert "hoodies" in driver.current_url
    
def add_first_choise(driver):
    wait = WebDriverWait(driver, 10)
    sweatshirt = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR, ".product-item-info a.product.photo.product-item-photo"
    )))
    driver.execute_script("arguments[0].scrollIntoView(true);", sweatshirt)
    sweatshirt.click()

    wait.until(EC.element_to_be_clickable((
        By.ID, "option-label-size-143-item-168"
    ))).click()
    wait.until(EC.element_to_be_clickable((
        By.ID, "option-label-color-93-item-57"
        ))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='product-addtocart-button']"))).click()
    success = wait.until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, "div.message-success.success.message"))
    )   
    assert "You added" in success.text


def test_login_only(driver):
    login(driver)

def test_add_product(driver):
    login(driver)
    go_to_jacket(driver)
    add_first_choise(driver) 