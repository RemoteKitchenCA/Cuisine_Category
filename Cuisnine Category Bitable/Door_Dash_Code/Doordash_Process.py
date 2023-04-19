import time
import pandas as pd
import requests
import undetected_chromedriver as UC
# from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from API_Request_Acess_Token import get_access_token

response = get_access_token()
access_Token = response['tenant_access_token']
print(f'Access Token Number : Bearer {access_Token}')
url = 'https://open.larksuite.com/open-apis/bitable/v1/apps/basuspDo7viuUtnUvnrylTaC2hf/tables/tblhd366GznVcz4W/records'
headers = {'Authorization': f'Bearer {access_Token}'}
params = {'view_id': 'vewouIsjPj', 'field_names': '["location","Test Doordash Original Category"]'}

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
        if 'Test Doordash Original Category' not in fields:
            # print(count)
            # print(f"record_id = {record_id}")
            # print(f"location = {location}")
            data_list.append({'record_id': record_id, 'location': location})
            count += 1
else:
    print('Error:', response.status_code)

df = pd.DataFrame(data_list)
# df.to_csv('record_location.csv', index=False)

# get a list of unique values from the 'location' column
unique_locations = df['location'].unique().tolist()
print(f'\nThis are All Location from Base\n\n{str(unique_locations)}\n')

# ----------------------Browser Open------
options = UC.ChromeOptions()
profile = "C:\\Users\\joy.ballav\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
options.add_argument(f"--user-data-dir={profile}")
browser = UC.Chrome(options=options, use_subprocess=True)
browser.maximize_window()

Ignored_Category_List = ['Personal care', 'Deals', 'Grocery', 'Convenience', 'Pharmacy', 'Baby', 'Pet supplies',
                         'Flowers', 'Retail']

Sign_In_url = 'https://identity.doordash.com/auth?client_id=1666519390426295040&enable_last_social=false&intl=en-CA&last_login_action=login&last_login_method=email&layout=consumer_web&prompt=none&redirect_uri=https%3A%2F%2Fwww.doordash.com%2Fpost-login%2F&response_type=code&scope=%2A&state=%2Fhome%2F%7C%7C337965c7-5c0e-4b1b-8efa-b832a59bb42e&_ga=2.266962126.1707097451.1681674961-1146354601.1681674961'
browser.get(Sign_In_url)
WebDriverWait(browser, 10)
time.sleep(20)

if len(browser.find_elements(By.XPATH,
                             '//*[@id="root"]/div/div/div/div/div/div/div/div[@class="sc-bBrHrO dQhtAa card"]')) > 0:
    # Type "Test" in the input field
    email_input_field = browser.find_element(By.XPATH,
                                             '//*[@id="root"]/div/div/div/div/div/div/div/div[@class="sc-bBrHrO dQhtAa card"]/div/form[@id="login-form-guided-email"]/div/div/div/div/div/div/div/div/input[@id="FieldWrapper-0"]')
    email_input_field.send_keys("remotekitchenrpa@gmail.com")
    time.sleep(2)
    # Find the Change_Addrs
    Submit_btn = browser.find_element(By.XPATH,
                                      '//*[@id="root"]/div/div/div/div/div/div/div/div[@class="sc-bBrHrO dQhtAa card"]/div/form[@id="login-form-guided-email"]/button[@data-anchor-id="IdentityGuidedSubmitButton"]')
    Submit_btn.submit()
    time.sleep(3)

    try:
        if len(browser.find_elements(By.XPATH, '//*[@id="otc-submit-form"]/span')) > 0:
            print("Code Sent popup Message")
            print(browser.find_element(By.XPATH, '//*[@id="otc-submit-form"]/span').text)
            use_Password = browser.find_element(By.XPATH,
                                                '//*[@id="otc-submit-form"]/button[@class="styles__StyledButtonRoot-sc-1ldytso-0 cScKko"]')
            use_Password.click()
            time.sleep(2)
            pass_input_field = browser.find_element(By.XPATH,
                                                    '//*[@id="login-form"]/div/div/div/div/div/div/input[1]')
            pass_input_field.send_keys("Rpa@1234")
            time.sleep(2)
            print('test')
            try:
                sign_in_btn = browser.find_element(By.XPATH,
                                                   '//*[@id="login-form"]/button[@data-anchor-id="IdentityLoginSigninButton"]')
                sign_in_btn.submit()
            except Exception as e:
                print("exception found:")
            time.sleep(3)
        else:
            if len(browser.find_elements(By.XPATH, '//*[@id="guided-phone-form"]/div/span')) > 0:
                print('mobile no asking')
                use_Password = browser.find_element(By.XPATH,
                                                    '//*[@class="sc-bBrHrO dQhtAa card"]/div/form/button[2]')
                use_Password.click()
                pass_input_field = browser.find_element(By.XPATH,
                                                        '//*[@id="login-form"]/div/div/div/div/div/div/input[1]')
                pass_input_field.send_keys("Rpa@1234")
                time.sleep(3)
                try:
                    sign_in_btn = browser.find_element(By.XPATH,
                                                       '//*[@id="login-form"]/button[@data-anchor-id="IdentityLoginSigninButton"]')
                    sign_in_btn.submit()
                except Exception as e:
                    print("exception found:")
    except Exception as e:
        print("exception found: Trying Submit Again")
# --------------------------------------------------------------------
# loop over each unique location
for location in unique_locations:
    # print(f"Location = {location}")
    # ------------------------------------------------------------
    print('\n\nDoordash Data Page Data Extraction Starting ...\n')
    # Location
    in_Location = location
    time.sleep(2)
    click_addrs = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                   '//*[@id="__next"]/main/div/div[1]/div/div[1]/header/div/div[1]/div[4]/div/div/div/button/span/span/span/span/div/span')))

    click_addrs.click()
    time.sleep(2)
    category_list = []
    if len(browser.find_elements(By.XPATH,
                                 '//*[@id="layout-address-picker"]/div/div/div/div/div/div/div[@class="Input__InputRoot-sc-1o75rg4-0 iuNBmt"]/div/div[@class="Input__InputContentContainer-sc-1o75rg4-2 bUbsck"]/input')) > 0:
        change_addrs = browser.find_element(By.XPATH,
                                            '//*[@id="layout-address-picker"]/div/div/div/div/div/div/div[@class="Input__InputRoot-sc-1o75rg4-0 iuNBmt"]/div/div[@class="Input__InputContentContainer-sc-1o75rg4-2 bUbsck"]/input')
        # change_addrs.click()
        change_addrs.send_keys(in_Location)
        time.sleep(1.5)
        # click_location = browser.find_element(By.XPATH, '//*[@id="addressAutocompleteDropdown"]/span[1]')
        # click_location.click()
        try:
            if len(browser.find_elements(By.XPATH, '//*[@id="addressAutocompleteDropdown"]/span[1]')) > 0:
                click_location = browser.find_element(By.XPATH, '//*[@id="addressAutocompleteDropdown"]/span[1]')
                click_location.click()

                # click_save = browser.find_element(By.XPATH,'//*[@id="layout-address-picker"]/div/div/div/div/div[@class="InlineChildren__StyledInlineChildren-sc-6r2tfo-0 hzFtA"]/button[@data-anchor-id="AddressEditSave"]')
                click_save = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                              '//*[@id="layout-address-picker"]/div/div/div/div/div[@class="InlineChildren__StyledInlineChildren-sc-6r2tfo-0 hzFtA"]/button[@data-anchor-id="AddressEditSave"]')))

                click_save.click()
                time.sleep(5)

                try:
                    # Wait for the element to be visible before finding it
                    WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH,
                                                                                       '//*[@id="carousel_cuisine_filter"]/div/div[@class="sc-9b70f33b-3 hQubzb"]/div/div/div/span')))
                    category_element = browser.find_elements(By.XPATH,
                                                             '//*[@id="carousel_cuisine_filter"]/div/div[@class="sc-9b70f33b-3 hQubzb"]/div/div/div/span')
                    time.sleep(4)
                    if len(category_element) > 0:
                        # category_list.append(category_element[0].text)
                        # Loop through the category elements and add their text to the list
                        for category in category_element:
                            if category.text not in Ignored_Category_List:
                                category_list.append(category.text)
                    else:
                        print("No category elements found")
                        category_list.append("No Category Found")

                    print(category_list)

                except Exception as e:
                    print("Error occurred while finding category element:", e)
                    category_list.append("Error Occurred")

                # ----------------------Doordash Category Extraction End----------

                # filter the DataFrame to include only records with that location
                location_df = df[df['location'] == location]
                # create a list of the 'record_id' values for those records
                record_ids = location_df['record_id'].tolist()
                # print the location and the list of record IDs
                print(f"Location = {location} \nrecord_id = {record_ids}\n")

                for record_id_list in record_ids:
                    print(record_id_list)
                    # Path variables
                    # -------------Update Base--------------------
                    Update_record_id = record_id_list
                    Update_app_token = "basuspDo7viuUtnUvnrylTaC2hf"
                    Update_table_id = "tblhd366GznVcz4W"

                    # URL
                    url = f"https://open.larksuite.com/open-apis/bitable/v1/apps/{Update_app_token}/tables/{Update_table_id}/records/{Update_record_id}"
                    # Authorization header value
                    token = f'Bearer {access_Token}'
                    # print(token)
                    headers = {"Authorization": token}
                    # Request body data
                    data = {"fields": {"Test Doordash Original Category": str(category_list)}}
                    # Send the PUT request
                    response = requests.put(url, headers=headers, json=data)
                    # Print the response status code and body
                    print(f"Status code: {response.status_code}")
                    # print(f"Response body: {response.json()}")
                    # -------------------------------------------
            else:
                print('No Address Found')
        except Exception as e:
            print("exception found in location select")
            print('No Address Found')
            click_addrs.click()
        time.sleep(2)

browser.quit()
