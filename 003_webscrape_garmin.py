import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.service import Service as FirefoxService
import pandas as pd
import time
import random
#response = requests.get('https://connect.garmin.com/modern/profile/a6efebef-a669-4e51-b6f8-1c954210c976')

def sleep_for_period_of_time():
    limit = random.randint(7, 10)
    time.sleep(limit)

s=FirefoxService('/home/siathor/Documents/test/selenium_firefox/drivers/geckodriver')
driver = webdriver.Firefox(service=s)

driver.get("https://connect.garmin.com/modern/profile/a6efebef-a669-4e51-b6f8-1c954210c976")
driver.implicitly_wait(10)
alert = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Accept")]'))).click()

while True:
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep_for_period_of_time()
        button = driver.find_element('xpath', "//button[@class='Button_btn__3OaiJ Button_btnSecondary__YVdZe  Button_btnMedium__pmyUz  Button_block__2fuxF' and @type='button']")
        sleep_for_period_of_time()
        button.click()
        print("Button clicked")
        sleep_for_period_of_time()
    except:
        print("No more scroll down")
        break


html = driver.page_source
with open('html.html', 'w') as f:
    f.write(html)
print("html saved")
#####################################################################################Extracting Data#################################################


soup = BeautifulSoup(html, 'html.parser')

# Find all div elements with a class that contains the string "Activity_activityData"
training = soup.find_all('div', class_=lambda x: x and 'Activity_activityData' in x)


# Create empty lists to store the data
date_list = []
training_data_list = []

# Find all div elements with a class that contains the string "Activity_activityData"
training = soup.find_all('div', class_=lambda x: x and 'Activity_activityData' in x)

# Loop through the training list
for element in training:
    # Find the date element and training data elements for the current element
    date = element.find('span', class_=lambda x: x and 'Activity_activityDate' in x)
    training_data = element.find_all('div', class_=lambda x: x and 'DataBlock_dataField' in x)
   
    # Extract the text content of the date element and store it in a separate variable
    date_text = date.text
    
    # Loop through the training data elements and extract the text content
    training_data_text = []
    for i in training_data:
        training_data_text.append(i.text)
    
    # Add the text content to the lists
    date_list.append(date_text)
    training_data_list.append(training_data_text)

# Create a dataframe from the lists
df = pd.DataFrame({'date': date_list, 'training_data': training_data_list})

df.to_csv('data.csv', index=False)

# Print the dataframe
print(df.head(20))

df.to_pickle('data.pkl')