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

print("\"Fırsatlarım\" sayfası açılıyor...")

while True:
    driver.get("https://pro.armut.com/opportunities")

    wait = WebDriverWait(driver, 10)

    wait.until(
        EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/opportunities/")]'))
    )

    print("Fırsatlarım sayfası açıldı.")

    input("Lütfen istediğiniz filtreleri seçin ve ENTER basın...")

    print("Tüm ilanlar alınıyor...")

    anchors = driver.find_elements(By.XPATH, '//a[contains(@href, "/opportunities/")]')
    links = [a.get_attribute('href') for a in anchors]
    
    if (len(links)) == 0:
        print("Bu filtrede iş ilanı yok.")
        continue

    for (inx, link) in enumerate(links):
        print(f"{link[::-1][:8][::-1]} ilanı açılıyor...")
        
        driver.get(f"{link}")
        
        reject_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="Reddet"]]'))
        )
        
        print("İlan sayfası açıldı!")

        reject_button.click()
        
        print("Reddet butonuna tıklandı.")
        
        radio_label = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//input[@value="13"]/ancestor::label')
        ))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio_label)
        driver.execute_script("arguments[0].click();", radio_label)
        
        print("\"Hizmet (meslek) uygun değil\" seçeneği seçildi.")
    
        submit_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[.//span[text()="Gönder"]]')
        ))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
        driver.execute_script("arguments[0].click();", submit_btn)
        
        print("Gönder butonuna tıklandı")
        
        if (inx >= len(links) - 1):
            print("Alınabilen tüm ilanlar dolaşıldı. Ana ekrana yönlendiriliyor.")
        else:
            print(f"Sıradaki ilan açılıyor...")
            time.sleep(1)