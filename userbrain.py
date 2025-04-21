import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from datetime import datetime  # Import datetime module
from telegram_bot_message import tgram_message
import json
import sys
import platform

print('userbrain',datetime.now())

if len(sys.argv) < 2:
    print("Usage: python userbrain.py <name>")
    sys.exit(1)

user = sys.argv[1]

with open('realconfig.json') as jason: # format in fakeconfig.json
    config = json.load(jason)

email = config[user]['email']
password = config[user]['ub_password']

tgram_message(f'UserBrain: Script Starting! {email} {datetime.now()}')


chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless
chrome_options.add_argument("--no-sandbox")  # Optional for laptop, required for Pi
chrome_options.add_argument("--disable-dev-shm-usage")  # Optional, helps on low-memory systems

if 'Ubuntu' in platform.version():
    driver = webdriver.Chrome(options=chrome_options)
elif 'PREEMPT' in platform.version():
    driver = webdriver.Chrome(options=chrome_options, 
                              service=Service('/snap/bin/chromium.chromedriver'))
else:
    raise Exception('Unsupported OS...')

driver.get("https://tester.userbrain.com/auth/login")
wait = WebDriverWait(driver, 30)

cookies = driver.find_element(By.CSS_SELECTOR, "[data-type='necessary']")
time.sleep(random.uniform(0.5, 2))  # Pause before clicking
cookies.click()
time.sleep(random.uniform(0.5, 2))  # Pause before clicking

email_field = driver.find_element(By.ID, "email")
pw_field = driver.find_element(By.ID, "password")
# logon_button = driver.find_element(By.CLASS_NAME, "button-success")
logon_button = driver.find_element(By.CSS_SELECTOR, "[data-sitekey='6LfsXqweAAAAACaRb-L5LTzGIDJexzmMiQxQqNOJ']")
for char in email:
    email_field.send_keys(char)
    time.sleep(random.uniform(0.01, 0.05))  
time.sleep(random.uniform(0.5, 2))  # Pause before clicking
for char in password:
    pw_field.send_keys(char)
    time.sleep(random.uniform(0.01, 0.05))  
time.sleep(random.uniform(0.5, 2))  # Pause before clicking

print('ub: logging in')
logon_button.click()
time.sleep(5)
last_chirp=0
while datetime.now().hour<23:
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    except:
        driver.refresh()
        continue

    test_page = 'https://tester.userbrain.com/dashboard'
    if driver.current_url!=test_page:
        tgram_message(f'''Userbrain Script Error: Unexpected URL: {driver.current_url}\n
                        Expected: {test_page}\n {user}''')
        raise Exception(f'''Unexpected URL: {driver.current_url}\nExpected: {test_page}, {user}''')
    
    no_tests_elements = driver.find_elements(By.XPATH, "//div[@class='tiles__tile' and .//img[@src='https://tester.userbrain.com/img/no-test.png']]")
    formatted_time = datetime.now().strftime('%I:%M %p')  # Format time as 12-hour clock with AM/PM
    if len(no_tests_elements)==0:
        print(f'UserBrain: {formatted_time}: {email}')
        tgram_message(f'UserBrain: {formatted_time}: {email}')
        print('waiting a bit for kristine to check it out', formatted_time)
        time.sleep(5*60) # 5 mins
    else:
        print(f'ub: nothing rn... {formatted_time} {user}')

    driver.refresh()
    time.sleep(10+random.uniform(0.5, 2))  
    if last_chirp + 3 <= datetime.now().hour:
        last_chirp=datetime.now().hour
        tgram_message(f'UserBrain {email} still running!')
else:
    tgram_message(f'UserBrain {email}: terminating because it is bedtime!')
    print(f'UserBrain {email}: terminating because it is bedtime!')
   
driver.quit()
