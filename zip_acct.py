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
    headers = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59', 
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
        'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36', 
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603'
        ]

    PROXY = "79.209.100.224:3707"  # IP:PORT or HOST:PORT

    # Skills & Place of Work
    # skill = input('Enter your Skill: ').strip()
    # place = input('Enter the location: ').strip()
    # no_of_pages = int(input('Enter the # of pages to scrape: '))
    # age = input('Enter the age: ').strip()


    indeed_posts=[]

    # Chrome Driver setup
    def set_chrome_driver(headless=True):
        options = Options()
        if headless:
            options.add_argument('--headless')
        # 추가적으로 필요한 옵션들은 여기에 추가하십시오.
        
        # ChromeDriverManager를 통해 자동으로 드라이버 경로를 관리합니다.
        chrome_service = Service(ChromeDriverManager().install())
        
        # Service 객체를 사용하여 Chrome 드라이버 초기화
        driver = webdriver.Chrome(service=chrome_service, options=options)
        return driver

    driver = set_chrome_driver(False)

    # https://www.ziprecruiter.com/jobs-search?search=valuation&location=Chicago%2C+IL&radius=25&page=1&impression_superset_id=CFRAY%3A8373ac236b92e148-IAD
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
            
                # Job Title:
                # if i.find('h2', {'class': 'jobTitle css-mr1oe7 eu4oa1w0'}) is not None:
                #     elif jobs = i.find('h2', {'class': 'jobTitle css-mr1oe7 eu4oa1w0'}).find('span').get('title') is None
                #     elif jobs = i.find('h2', {'class': 'jobTitle css-1u6tfqq eu4oa1w0'}).find('span').get('title')

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

                # # Job Post Date:

                # if i.find('time', attrs={'class': 'job-search-card__listdate'}) != None:
                #     post_date = i.find('time', attrs={'class': 'job-search-card__listdate'}).text

    # Put everything together in a list of lists for the default dictionary
                    
                indeed_posts.append([company,jobs,links,salary,location])


    # put together in list

    # (create a dictionary with keys and a list of values from above "indeed_posts")

    indeed_dict_list=defaultdict(list)

    # # Fields for our DF 

    indeed_spec=['Company','job','link','Salary','Location']

    driver.quit()  # Close the webdriver


    # pd.set_option('display.max_colwidth', None)

    # print('These Href links will go to a new page containing full job description')
    # print('\n')
    # print(pd.DataFrame(indeed_posts,columns=indeed_spec)['link'][0]) 
    # #these are not the same, probably from recruiter(s)
    # print(pd.DataFrame(indeed_posts,columns=indeed_spec)['link'][1])
    # print(pd.DataFrame(indeed_posts,columns=indeed_spec)['link'][2])


    df = pd.DataFrame(indeed_posts,columns=indeed_spec)
    return df



