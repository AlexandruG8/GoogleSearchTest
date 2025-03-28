from re import search

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setting up the WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") #Start browser maximized
options.add_argument("--disable-blink-features=AutomationControlled") # Reduce bot detection
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=options)

def solve_captcha():
    try:
        # Wait for Captcha checkbox if it appears
        captcha_checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@title, 'reCAPTCHA')]"))
        )
        print("Captcha detected. Please solve it manually.")
        time.sleep(10) # Allow user to solve captcha manually
    except:
        print("No captcha detected.")

try:
    # Open Google
    driver.get("https://www.google.com/")

    # Wait for coockies pop-up and close it
    time.sleep(2)
    try:
        accept_cookies_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='L2AGLb']"))
        )
        accept_cookies_button.click()
    except:
        print("No cookies pop-up found or already closed.")

    # Wait briefly to ensure interaction
    time.sleep(1)

    # Solve captcha if present
    solve_captcha()

    # Select the search bar
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )

    # Enter the search word
    search_box.send_keys("gaming monitors")

    # Wait before hitting Enter
    time.sleep(3)

    # Press the search button (Enter key)
    search_box.send_keys(Keys.RETURN)

    #Wait for results to load
    time.sleep(5)

    #Scroll to the bottom of the page (smooth human-like scrolling)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        for _ in range(10): # Scroll in small increments
            driver.execute_script("window.scrollBy(0, 250);") # Scroll by small steps
            time.sleep(1) # Short delay to mimic human-like scrolling
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height is None or last_height is None:
            break # Avoid comparing Nonetype values
        if new_height <= last_height:
            break
        last_height = new_height

    # Wait before closing the browser
    time.sleep(5)

    print("Test completed succesfully!")

finally:
    # Close the browser
    driver.quit()
