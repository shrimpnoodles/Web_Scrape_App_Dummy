import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

glassdoor_companies = []
career_sites = []

#there are actually 63,741 pages
for pageNum in range(1, 2):
    target_url = "https://www.glassdoor.com/Reviews/index.htm?overall_rating_low=3&page="+str(pageNum)+"&locId=1&locType=N&locName=United%20States&filterType=RATING_OVERALL"

    driver = webdriver.Chrome()
    driver.get(target_url)
    #driver.get_screenshot_as_file("debug1.png")
    resp = driver.page_source
    
    soup = BeautifulSoup(resp)

    container = soup.find("div", {"class": "col-md-12 col-lg-8"})
    comps = container.find_all("h2", {"data-test": "employer-short-name"})
    
    for comp in comps:
        glassdoor_companies.append(comp.text)
        
#print(glassdoor_companies)

for company in glassdoor_companies:
    target_url = "https://www.google.com/search?q="+str(company)+"+careers+usa"

    driver = webdriver.Chrome()
    driver.get(target_url)
    #driver.get_screenshot_as_file("debug2.png")
    resp = driver.page_source

    soup = BeautifulSoup(resp)
    
    search = soup.find("a", {"jsname": "UWckNb"})
    link = search.get("href")
    career_sites.append(link)
    
#print(career_sites)

company_career_sites = dict(zip(glassdoor_companies, career_sites))

#print(company_career_sites)

df = pd.DataFrame.from_dict(company_career_sites, orient='index')
df.columns=["Career page"]
df.to_clipboard()
df.head()
df.to_csv('company_careers.csv', index=False, encoding= 'utf-8')

for site in career_sites:
    target_url = site

    options= Options()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    driver.get(target_url)

    print(site)
    #search_bar = driver.find_elements(By.CSS_SELECTOR, "[id*='search']")
    #search_bar = driver.find_elements(By.XPATH, "//input[@type='text']")
    search_bar = driver.find_elements(By.CSS_SELECTOR, "[type='text']")
    for elem in search_bar:
        print(elem.get_attribute("placeholder"))
    