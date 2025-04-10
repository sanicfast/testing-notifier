import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pushbullet import Pushbullet 
from datetime import datetime  # Import datetime module
import json
import sys
import platform

print(datetime.now())

if len(sys.argv) < 2:
    print("Usage: python usertesting.py <name>")
    sys.exit(1)

user = sys.argv[1]

with open('realconfig.json') as jason: # format in fakeconfig.json
    config = json.load(jason)

email = config[user]['email']
password = config[user]['ut_password']
pb = Pushbullet(config['PB_API_KEY'])
pb.push_note(f'UserTesting','Script starting! {email} {datetime.now}')

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless
chrome_options.add_argument("--no-sandbox")  # Optional for laptop, required for Pi
chrome_options.add_argument("--disable-dev-shm-usage")  # Optional, helps on low-memory systems

if 'Ubuntu' in platform.version():
    driver = webdriver.Chrome(options=chrome_options)
elif 'Debian' in platform.version():
    driver = webdriver.Chrome(options=chrome_options, 
                              service=Service('/snap/bin/chromium.chromedriver'))
else:
    raise Exception('Unsupported OS...')
driver.get("https://auth.usertesting.com/signin")
wait = WebDriverWait(driver, 30)

email_field = driver.find_element(By.ID, "okta-signin-username")
pw_field = driver.find_element(By.ID, "okta-signin-password")
logon_button = driver.find_element(By.ID, "okta-signin-submit")

email_field.clear()
time.sleep(random.uniform(0.5, 1))  


for char in email:
    email_field.send_keys(char)
    time.sleep(random.uniform(0.01, 0.05))  # 50–150 ms per keystroke

time.sleep(random.uniform(0.5, 1))  # Pause before password

pw_field.clear()
time.sleep(random.uniform(0.5, 1))
# Type password character-by-character
for char in password:
    pw_field.send_keys(char)
    time.sleep(random.uniform(0.01, 0.05))

time.sleep(random.uniform(0.5, 2))  # Pause before clicking

print('ut: logging in')
logon_button.click()
# driver.get("https://app.usertesting.com/my_dashboard/available_tests_v3") #it goes there automatically

time.sleep(5)
last_chirp = 0
while datetime.now().hour<23:
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    except:
        driver.refresh()
        continue
    test_page = 'https://app.usertesting.com/my_dashboard/available_tests_v3'
    if driver.current_url!=test_page:
        pb.push_note('UserTesting Script Error!',f'''Unexpected URL: {driver.current_url}\nExpected: {test_page}, {user}''')
        raise Exception(f'''Unexpected URL: {driver.current_url}\nExpected: {test_page}, {user}''')

    tests = driver.find_elements(By.CLASS_NAME, "available-tests__tile")
    test_count = len(tests)
    formatted_time = datetime.now().strftime('%I:%M %p')  # Format time as 12-hour clock with AM/PM
    if test_count>0:
        print(f"Found {test_count} test(s) available!")        
        pb.push_note(f'UserTesting: {test_count}',f'{formatted_time}: {email}')
        print('waiting a bit for kristine to check it out', formatted_time)
        time.sleep(5*60) # 5 mins
    else:
        print(f'nothing rn... {formatted_time}')

    driver.refresh()
    time.sleep(10+random.uniform(0.5, 2))  
    if last_chirp + 3 <= datetime.now().hour:
        last_chirp=datetime.now().hour
        pb.push_note(f'UserTesting {email}','still running!')
else:
    print('terminating because its time to go to bed')
driver.quit()
