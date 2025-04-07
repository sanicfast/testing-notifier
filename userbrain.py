import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pushbullet import Pushbullet 
from datetime import datetime  # Import datetime module
import json
import sys

if len(sys.argv) < 2:
    print("Usage: python userbrain.py <name>")
    sys.exit(1)

user = sys.argv[1]

with open('realconfig.json') as jason: # format in fakeconfig.json
    config = json.load(jason)

email = config[user]['email']
password = config[user]['ub_password']
pb = Pushbullet(config['PB_API_KEY'])

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless
chrome_options.add_argument("--no-sandbox")  # Optional for laptop, required for Pi
chrome_options.add_argument("--disable-dev-shm-usage")  # Optional, helps on low-memory systems

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://tester.userbrain.com/auth/login")
wait = WebDriverWait(driver, 10)

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

logon_button.click()

time.sleep(5)

while True:
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    test_page = 'https://tester.userbrain.com/dashboard'
    if driver.current_url!=test_page:
        pb.push_note('Userbrain Script Error!',f'''Unexpected URL: {driver.current_url}\nExpected: {test_page}, {user}''')
        raise Exception(f'''Unexpected URL: {driver.current_url}\nExpected: {test_page}, {user}''')
    
    no_tests_elements = driver.find_elements(By.XPATH, "//div[@class='tiles__tile' and .//img[@src='https://tester.userbrain.com/img/no-test.png']]")
    formatted_time = datetime.now().strftime('%I:%M %p')  # Format time as 12-hour clock with AM/PM
    if len(no_tests_elements)==0:
        print('woah we have a test??')
        pb.push_note(f'UserBrain',f'{formatted_time}: {email}')
        print('waiting a bit for kristine to check it out', formatted_time)
        time.sleep(5*60) # 5 mins
    else:
        print(f'nothing rn... {formatted_time}')

    driver.refresh()
    time.sleep(10+random.uniform(0.5, 2))  
