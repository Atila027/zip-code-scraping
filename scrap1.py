# Never change other part of this script

from selenium import webdriver  
import time  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import csv



# ------------------- You need to update only this part -----------------------
startRow = 100 # this will be changed on each script
endRow = 200 # this will be changed on each script
ResultCSVName = "result-1.csv" # this will be changed on each script
# -----------------------------------------------------------------------------




# ------------------- Never change this part of this script -----------------------
scrappingCnt = 1
header = ['City', 'Address', 'House number', 'Zip code']

# chrome driber option part
args = ["hide_console"]
chrome_options = Options()
chrome_options.add_argument("--log-level=3")
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--hide-scrollbars")
s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(options = chrome_options, service = s, service_args=args)
driver.maximize_window()  
driver.get("https://israelpost.co.il/%D7%A9%D7%99%D7%A8%D7%95%D7%AA%D7%99%D7%9D/%D7%90%D7%99%D7%AA%D7%95%D7%A8-%D7%9E%D7%99%D7%A7%D7%95%D7%93/")  


# Read data from excel file that you want to scrap
dataFrame = pd.read_excel('addresses_result.xlsx')
city = pd.DataFrame(dataFrame, columns=['Unnamed: 0']).values
address = pd.DataFrame(dataFrame, columns=['Unnamed: 1']).values

with open(ResultCSVName, 'w', encoding='utf-8-sig', newline='') as f:
    print("********** Scrapping has just been started ************\n")  
    writer = csv.writer(f)
    writer.writerow(header)
   
    for index in range(startRow, endRow):   
        for index2 in range(1, 501):

            print("Row: " + str(index))
            print("House Number: " + str(index2))
            print("Scrapping count: " + str(scrappingCnt))

            driver.find_element("id", "City").send_keys(city[index])  
            driver.find_element("id", "Street").send_keys(address[index])  
            driver.find_element("id", "House").send_keys(index2) 
            
            time.sleep(0.1) 
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            searchElement = soup.find('button', attrs = {'id':'SearchZipSearch'})['class']
            print(len(searchElement))
            
            if len(searchElement) == 3:
                driver.find_element("id", "SearchZipSearch").send_keys(Keys.ENTER)  
                
                time.sleep(1)  
                element = soup.find('div', attrs = {'id':'searchresult'})
                value = element.text.strip()

                zipcode = ''
                for character in value:
                    if character.isdigit():
                        zipcode = zipcode + character

                print("Zip Code: " + zipcode + "\n")

                if zipcode != '':
                    scrappingCnt = scrappingCnt + 1
                    cityValue = (city[index]).astype('U')
                    addressValue = (address[index]).astype('U')                
                    data = [* cityValue, * addressValue, index2, zipcode]
                    writer.writerow(data)

                else:          
                    driver.find_element("id", "City").clear()
                    driver.find_element("id", "Street").clear()
                    driver.find_element("id", "House").clear()
                    break

                driver.find_element("id", "City").clear()
                driver.find_element("id", "Street").clear()
                driver.find_element("id", "House").clear()

            else:              
                driver.find_element("id", "City").clear()
                driver.find_element("id", "Street").clear()
                driver.find_element("id", "House").clear()
                continue


print("************ Scrapping has been successfully completed ************")  
# -----------------------------------------------------------------------------