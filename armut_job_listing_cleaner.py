import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

WAIT_TIMEOUT = 10
WAIT_BETWEEN_REQUESTS = 1

def get_driver() -> WebDriver:
    os.popen("\"C:/Program Files/Google/Chrome/Application/chrome.exe\" --remote-debugging-port=9222 --user-data-dir=\"C:/chrome-temp\"")
    options = Options()
    options.debugger_address = "localhost:9222"
    return webdriver.Chrome(options=options)

driver: WebDriver = get_driver()
wait = WebDriverWait(driver, WAIT_TIMEOUT)

def open_opportunities_page():
    driver.get("https://pro.armut.com/opportunities")
    wait.until(
        EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/opportunities/")]'))
    )
    print("Fırsatlarım sayfası açıldı.")

def get_all_opportunities() -> list[str]:
    print("İlanlar alınıyor...")

    anchors = driver.find_elements(By.XPATH, '//a[contains(@href, "/opportunities/")]')
    return [a.get_attribute('href') for a in anchors]

def click_reject_button():
    reject_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="Reddet"]]'))
    )
    reject_button.click()
    print("Reddet butonuna tıklandı.")

def click_reject_reason_radio_button():
    radio_label : WebDriver
    
    select_other_option = random.randint(1, 10) > 5
    
    if not select_other_option:
        radio_label = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//input[@value="13"]/ancestor::label')
        ))
        print("\"Hizmet (meslek) uygun değil\" seçeneği seçildi.")
    else:
        radio_label = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//input[@value="17"]/ancestor::label')
        ))
        print("\"Diğer\" seçeneği seçildi.")
    
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio_label)
    driver.execute_script("arguments[0].click();", radio_label)
    
def click_submit_button():
    submit_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[.//span[text()="Gönder"]]')
    ))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
    driver.execute_script("arguments[0].click();", submit_btn)
        
    print("Gönder butonuna tıklandı")

def start_rejecting(links: list[str]):
    for (inx, link) in enumerate(links):
        print(f"{link[::-1][:8][::-1]} ilanı açılıyor...")
        
        driver.get(f"{link}")
        print("İlan sayfası açıldı!")
        
        click_reject_button()
        click_reject_reason_radio_button()
        click_submit_button()
        
        if (inx >= len(links) - 1):
            print("Alınabilen tüm ilanlar dolaşıldı. Ana ekrana yönlendiriliyor.")
        else:            
            print(f"Sıradaki ilan açılıyor...")
            time.sleep(WAIT_BETWEEN_REQUESTS)

def main():
    print("\"Fırsatlarım\" sayfası açılıyor...")

    while True:
        open_opportunities_page()
        
        input("Lütfen istediğiniz filtreleri seçin ve ENTER basın...")
        
        links = get_all_opportunities()
        
        if not links:
            print("Bu filtrede iş ilanı yok.")
            continue
        
        print(f"Toplam {len(links)} adet ilan alındı!")
        
        start_rejecting(links)
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
    except TimeoutException:
        print("Timeout...")