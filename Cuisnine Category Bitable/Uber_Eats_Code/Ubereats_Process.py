import pandas as pd
import requests
from API_Request_Acess_Token import get_access_token
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

response = get_access_token()
access_Token = response['tenant_access_token']
print(f'Access Token Number : Bearer {access_Token}')
url = 'https://open.larksuite.com/open-apis/bitable/v1/apps/basuspDo7viuUtnUvnrylTaC2hf/tables/tblhd366GznVcz4W/records'
headers = {'Authorization': f'Bearer {access_Token}'}
params = {'view_id': 'vewouIsjPj', 'field_names': '["location","Test Uber Original Category"]'}

response = requests.get(url, headers=headers, params=params)
count = 1
data_list = []

if response.status_code == 200:
    data = response.json()['data']
    items = data['items']

    for item in items:
        record_id = item['record_id'].strip()
        fields = item['fields']
        location = fields['location'][0]['text'].strip()
        if 'Test Uber Original Category' not in fields:
            #print(count)
            #print(f"record_id = {record_id}")
            #print(f"location = {location}")
            data_list.append({'record_id': record_id, 'location': location})
            count += 1
else:
    print('Error:', response.status_code)

df = pd.DataFrame(data_list)
#df.to_csv('record_location.csv', index=False)

'''# get a list of unique values from the 'location' column
unique_locations = df['location'].unique().tolist()

# print the list of unique locations
print(unique_locations)'''

# get a list of unique values from the 'location' column
unique_locations = df['location'].unique().tolist()
print(f'\nThis are All Location from Base\n\n{str(unique_locations)}\n')

#-------------------UberEats Search-------------------------
#chrome_driver_path = 'E:/chromedriver/chromedriver_win32/chromedriver'
chrome_driver_path = './Cuisnine Category Bitable/Chrome_Driver/chromedriver_win32/chromedriver.exe'
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)
# Maximize the browser window
driver.maximize_window()
print("Starting Category extraction...")


Ignored_Category_List = ['Personal care', 'Deals', 'Grocery', 'Convenience', 'Pharmacy', 'Baby', 'Pet supplies','Flowers', 'Retail']

# Navigate to the webpage
url = 'https://www.ubereats.com/ca/feed?diningMode=DELIVERY&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMjg1MTElMjBBbGV4YW5kcmElMjBSZCUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMkNoSUpFY2FSX2k5MWhsUVJnQlBnMXdRRk16MCUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJnb29nbGVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0E0OS4xNzg1NDUwMDAwMDAwMSUyQyUyMmxvbmdpdHVkZSUyMiUzQS0xMjMuMTI4OTEzOSU3RA%3D%3D'
# url = "https://www.ubereats.com/ca/feed?diningMode=DELIVERY&pl=JTdCJTIyYWRk"
driver.get(url)

# Wait for the page to load completely
time.sleep(15)
# loop over each unique location
for location in unique_locations:
    #print(f"Location = {location}")
    # Location
    in_Location = location
    #...................UberEats_Category Search.....................

    # Find the Click_addrs
    #time.sleep(3)
    Click_addrs = driver.find_element(By.XPATH, '//*[@id="wrapper"]/header/div/div/div[1]/span')
    # Click on the category element
    Click_addrs.click()
    time.sleep(5)

    # Find the Click_addrs
    Change_Addrs = driver.find_element(By.XPATH,'//*[@id="wrapper"]/div[3]/div/div/div[2]/div[3]/div/div[2]/div[1]/div[2]/a')
    Change_Addrs.click()
    time.sleep(5)

    input_field = driver.find_element(By.XPATH, '//*[@id="location-typeahead-location-manager-input"]')

    # Type "Test" in the input field
    input_field.send_keys(in_Location)
    time.sleep(5)

    # Press the Enter key
    input_field.send_keys(Keys.ENTER)
    time.sleep(10)

    category_element = driver.find_elements(By.XPATH, '//*[@id="main-content"]/div/div[1]/div/nav/ul/li/a/span/div')
    category_list = []

    if len(category_element) > 0:
        for category in category_element:
            if category.text not in Ignored_Category_List:
                category_list.append(category.text)
    else:
        print("No category elements found")
        category_list.append("No Category Found")

    print("Data Extraction Complete")

    # Print the list of categories
    print(category_list)

    #--------------------------------------------

    # filter the DataFrame to include only records with that location
    location_df = df[df['location'] == location]
    # create a list of the 'record_id' values for those records
    record_ids = location_df['record_id'].tolist()
    # print the location and the list of record IDs
    print(f"Location = {location} \nrecord_id = {record_ids}\n")

    for record_id_list in record_ids:
        print(record_id_list)
        # Path variables
        #-------------Update Base--------------------
        Update_record_id = record_id_list
        Update_app_token = "basuspDo7viuUtnUvnrylTaC2hf"
        Update_table_id = "tblhd366GznVcz4W"

        # URL
        url = f"https://open.larksuite.com/open-apis/bitable/v1/apps/{Update_app_token}/tables/{Update_table_id}/records/{Update_record_id}"

        # Authorization header value
        token = f'Bearer {access_Token}'
        #print(token)
        headers = {"Authorization": token}

        # Request body data
        data = {"fields": {"Test Uber Original Category": str(category_list)}}

        # Send the PUT request
        response = requests.put(url, headers=headers, json=data)

        # Print the response status code and body
        print(f"Status code: {response.status_code}")
        #print(f"Response body: {response.json()}")
        #-------------------------------------------
    time.sleep(3)
driver.quit()