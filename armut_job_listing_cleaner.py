import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

os.popen("\"C:/Program Files/Google/Chrome/Application/chrome.exe\" --remote-debugging-port=9222 --user-data-dir=\"C:/chrome-temp\"")

options = Options()
options.debugger_address = "localhost:9222"

driver = webdriver.Chrome(options=options)

print("Opening opportunities tab...")

driver.get("https://pro.armut.com/opportunities")

wait = WebDriverWait(driver, 10)

wait.until(
    EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/opportunities/")]'))
)

print("Opportunities tab loaded.")

input("Press enter if you selected your filters...")

print("Getting all listings available now...")

anchors = driver.find_elements(By.XPATH, '//a[contains(@href, "/opportunities/")]')
links = [a.get_attribute('href') for a in anchors]

for link in links:
    print(f"Waiting for {link[::-1][:8][::-1]} opening...")
    
    driver.get(f"{link}")
    
    reject_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="Reddet"]]'))
    )
    
    print("Page Opened!")

    reject_button.click()
    
    print("Clicked to reject button...")
    
    radio_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@type="radio" and @value="13"]'))
    )
    
    print("Selected \"Hizmet (meslek) uygun değil\" option...")

    radio_button.click()
    
    submit_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="Gönder"]]'))
    )

    print("Clicked Submit button.")
    
    submit_button.click()
    
    time.sleep(1)
    
    print("Opening new page...")
    
    time.sleep(1)