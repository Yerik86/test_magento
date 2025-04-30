import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    #options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

def login(driver):
    driver.get("https://magento.softwaretestingboard.com/")
    wait = WebDriverWait(driver, 10)
    login_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "li.authorization-link a"))
    )
    login_button.click()
   
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='email']")))
    email_field = driver.find_element(By.XPATH, "//*[@id='email']")         
    email = "ddzon9188@gmail.com"
    #action = ActionChains(driver)
    #for char in email:
        #action.send_keys_to_element(email_field, char).pause(0.1)
    #action.perform()
    email_field.send_keys(email)
    password_field = driver.find_element(By.XPATH, "//*[@id='pass']")
    password = "tp6Z21#17"
    password_field.send_keys(password)

    button1 = driver.find_element(By.XPATH, "//*[@id='send2']")
    button1.click()

    wait.until(EC.url_to_be("https://magento.softwaretestingboard.com/"))

    assert "magento.softwaretestingboard" in driver.current_url
    return driver

def test_first_choice(driver):
    driver = login
    wait = WebDriverWait(driver, 10)

    women_menu = wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='ui-id-4']/span[2]"))
    )
    ActionChains(driver).move_to_element(women_menu).perform()

    
    first_choice = wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='ui-id-9']/span[2]"))
    )
    ActionChains(driver).move_to_element(first_choice).perform()

    hoodies_choice = wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='ui-id-12']/span"))
    )
    ActionChains(driver).move_to_element(hoodies_choice).perform()
    hoodies_choice.click()
    assert "hoodies" in driver.current_url

def test_add_jacket_in_to_cart(login):
    driver = login
    wait = WebDriverWait(driver, 10)

    yoga_jacket = driver.find_element(By.XPATH, "//*[@id='maincontent']/div[3]/div[1]/div[3]/ol/li[5]/div")
    driver.execute_script("arguments[0].scrollIntoView(true);", yoga_jacket)
    jade_jacket = wait.until(
       EC.presence_of_element_located(yoga_jacket) 
    )
    ActionChains(driver).move_to_element(jade_jacket).perform()