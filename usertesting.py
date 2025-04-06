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
    print("Usage: python usertesting.py <name>")
    sys.exit(1)

user = sys.argv[1]

with open('realconfig.json') as jason: # format in fakeconfig.json
    config = json.load(jason)

email = config[user]['email']
password = config[user]['ut_password']
pb = Pushbullet(config['PB_API_KEY'])

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless
chrome_options.add_argument("--no-sandbox")  # Optional for laptop, required for Pi
chrome_options.add_argument("--disable-dev-shm-usage")  # Optional, helps on low-memory systems

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://auth.usertesting.com/signin")
wait = WebDriverWait(driver, 10)

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
logon_button.click()
# driver.get("https://app.usertesting.com/my_dashboard/available_tests_v3") #it goes there automatically

time.sleep(5)

while True:
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    tests = driver.find_elements(By.CLASS_NAME, "available-tests__tile")
    test_count = len(tests)
    print(f"Found {test_count} test(s) available")
    if test_count>0:
        formatted_time = datetime.now().strftime('%I:%M %p')  # Format time as 12-hour clock with AM/PM
        pb.push_note(f'UserTesting: {test_count}',f'{formatted_time}: {email}')
        print('waiting a bit for kristine to check it out', formatted_time)
        time.sleep(5*60) # 5 mins

    driver.refresh()
    time.sleep(5+random.uniform(0.5, 2))  # Wait to observe

