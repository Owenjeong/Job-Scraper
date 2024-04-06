import requests # http requests
from bs4 import BeautifulSoup # Webscrape
from selenium import webdriver
from collections import defaultdict # Default dictionary: store a list with each key
import pandas as pd     # DF
import time
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def zip_acct(skill, place, age, no_of_pages):
    # this was used for the person contacting me who had these details for their system
    headers = {
        "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}


    indeed_posts=[]

    # Chrome Driver setup
    def set_chrome_driver(headless=True):
        options = Options()
        if headless:
            options.add_argument('--headless')
        
        chrome_service = Service(ChromeDriverManager().install())
        
        driver = webdriver.Chrome(service=chrome_service, options=options)
        return driver

    driver = set_chrome_driver(False)
    
    for page in range(no_of_pages):
        # Connecting linkedin
            url = 'https://www.ziprecruiter.com/jobs-search?search=' + skill + \
                '&location=' + place +'&radius=25' + '&page=' + str(page + 1) 
            
            # Get request to indeed with headers above (you don't need headers!)
            driver.get(url)
            time.sleep(10)
            #response = requests.get(url, headers=headers)
            html = driver.page_source

            # Scrapping the Web (you can use 'html' or 'lxml')
            soup = BeautifulSoup(html, 'html.parser')

            # Outer Most Entry Point of HTML:
            outer_most_point=soup.find('div',attrs={'id':'react-job-results-root'})
            #print(outer_most_point)
            # "UL" lists where the data are stored:
            
            for i in outer_most_point.find_all('div'):

                # 1st if
                if i.find('h2', {'class': 'font-bold text-black text-header-sm'}) is not None:
                    jobs = i.find('h2', {'class': 'font-bold text-black text-header-sm'}).text.strip()
                
                # Company Name:
            
                if i.find('p', {'class': 'text-black normal-case line-clamp-1 text-body-md'}) is not None:
                    company = i.find('p', {'class': 'text-black normal-case line-clamp-1 text-body-md'}).text.strip()
                        
                # Links: these Href links will take us to full job description
                
                header_tag = i.find('h2', {'class': 'font-bold text-black text-header-sm'})
                if header_tag is not None:
                    a_tag = header_tag.find('a')
                    if a_tag is not None:
                        links = a_tag.get('href')
                    
                # Salary if available:
                
                if i.find('div', {'class': 'mr-8'}) is not None:
                    salary = i.find('div', {'class': 'mr-8'}).text.strip()

                else:
                    salary='No Salary'

                # location
                if i.find('p', {'class': 'text-black normal-case text-body-md'}) is not None:
                    location = i.find('p', {'class': 'text-black normal-case text-body-md'}).text.strip()


    # Put everything together in a list of lists for the default dictionary
                    
                indeed_posts.append([company,jobs,links,salary,location])


    # put together in list

    # (create a dictionary with keys and a list of values from above "indeed_posts")

    indeed_dict_list=defaultdict(list)

    # # Fields for our DF 

    indeed_spec=['Company','job','link','Salary','Location']

    driver.quit()  # Close the webdriver



    df = pd.DataFrame(indeed_posts,columns=indeed_spec)
    return df



