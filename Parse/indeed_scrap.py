import requests # http requests
from bs4 import BeautifulSoup # Webscrape
from selenium import webdriver
from collections import defaultdict # Default dictionary: store a list with each key
import pandas as pd     # DF
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from parsel import Selector

def indeed_acct(skill, place, age, no_of_pages):
    # this was used for the person contacting me who had these details for their system
    headers = {
        "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}


    indeed_posts=[]

def set_chrome_driver(headless=True, path_to_chromedriver='/Parse/122.chromedriver-win64/chromedriver.exe'):
    options = Options()
    if headless:
        options.add_argument('--headless')
    # ChromeDriver의 경로를 직접 지정합니다.
    chrome_service = Service(executable_path=path_to_chromedriver)
    driver = webdriver.Chrome(service=chrome_service, options=options)
    return driver

# 함수를 호출할 때, 다운로드한 ChromeDriver의 실제 경로를 지정해야 합니다.
driver = set_chrome_driver(headless=False, path_to_chromedriver='/Parse/122.chromedriver-win64/chromedriver.exe')

    
    driver = set_chrome_driver(headless=False)

    for page in range(no_of_pages):
        
        # Connecting indeed
            url = 'https://www.indeed.com/jobs?q=' + skill + \
                '&l=' + place +'&sort=date'+'&fromage=' + age + '&start=' + str(page * 10) #binary number, 0 = 1st page, 10 = 2nd page, 11 = 3rd page

            # Get request to indeed with headers above (you don't need headers!)
            driver.get(url)
            time.sleep(10)
            #response = requests.get(url, headers=headers)
            html = driver.page_source

            # Scrapping the Web (you can use 'html' or 'lxml')
            soup = BeautifulSoup(html, 'lxml')

            # Outer Most Entry Point of HTML:
            outer_most_point=soup.find('div',attrs={'id':'mosaic-provider-jobcards'})
            #print(outer_most_point)
            # "UL" lists where the data are stored:
            
            for i in outer_most_point.find('ul'):
            
                job_title = None


                
                # 1st if
                h2_tag = i.find('h2', {'class': 'jobTitle css-14z7akl eu4oa1w0'})
                if h2_tag is not None:
                    span_tag = h2_tag.find('span')
                    if span_tag is not None:
                        job_title = span_tag.get('title')

                # if the 1st can't find anything it goes to 2nd if
                if job_title is None:
                    sel = Selector(text=str(i))
                    h2_tag_text = sel.xpath('//*[contains(@id, "jobTitle")]/text()').extract_first()
                    if h2_tag_text:    
                        job_title = h2_tag_text.strip()

                jobs = job_title
                # Company Name:
            
                if i.find('span', {'data-testid': 'company-name'}) is not None:
                    company = i.find('span', {'data-testid': 'company-name'}).text.strip()
                        
                # Links: these Href links will take us to full job description
                
                if i.find('a', {'class': 'jcs-JobTitle css-jspxzf eu4oa1w0'}) is not None:
                    links = i.find('a', {'class': 'jcs-JobTitle css-jspxzf eu4oa1w0'}).get('href')
                        
                # Salary if available:
                
                if i.find('div', {'data-testid': 'attribute_snippet_testid'}) is not None:
                    salary = i.find('div', {'data-testid': 'attribute_snippet_testid'}).text.strip()

                else:
                    salary='No Salary'
                
                # location
                if i.find('div', {'data-testid': 'text-location'}) is not None:
                    location = i.find('div', {'data-testid': 'text-location'}).text.strip()                
                else:
                    location='Not Available'
                # Job Post Date:

                if i.find('span', attrs={'data-testid': 'myJobsStateDate'}) != None:
                    post_date = i.find('span', attrs={'data-testid': 'myJobsStateDate'}).text
                else:
                    post_date = 'Not Available'

    # Put everything together in a list of lists for the default dictionary
                    
                indeed_posts.append([company,jobs,f"indeed.com{links}",salary,location,post_date])

    # put together in list

    indeed_dict_list=defaultdict(list)

    # # Fields for our DF 

    indeed_spec=['Company','Job','Link','Salary','Location','Job_Posted_Date']

    driver.quit()  # Close the webdriver


    df = pd.DataFrame(indeed_posts,columns=indeed_spec)

    return df


