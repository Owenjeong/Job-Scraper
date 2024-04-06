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
# import smtplib
# from email.message import EmailMessage
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# from email import encoders
from parsel import Selector

def indeed_acct(skill, place, age, no_of_pages):
    # this was used for the person contacting me who had these details for their system
    headers = {
        "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}

    # Skills & Place of Work
    # skill = input('Enter your Skill: ').strip()
    # place = input('Enter the location: ').strip()
    # no_of_pages = int(input('Enter the # of pages to scrape: '))
    # age = input('Enter the age: ').strip()


    indeed_posts=[]

    # # Chrome Driver setup
    # def set_chrome_driver(headless=True):
    #     options = Options()
    #     if headless:
    #         options.add_argument('headless')
    #     #options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36")
    #     chrome_driver_path = ChromeDriverManager().install()
    #     driver = webdriver.Chrome(chrome_driver_path, options=options)
    #     return driver

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
            
                # Job Title:
                # if i.find('h2', {'class': 'jobTitle css-mr1oe7 eu4oa1w0'}) is not None:
                #     elif jobs = i.find('h2', {'class': 'jobTitle css-mr1oe7 eu4oa1w0'}).find('span').get('title') is None
                #     elif jobs = i.find('h2', {'class': 'jobTitle css-1u6tfqq eu4oa1w0'}).find('span').get('title')
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

    # (create a dictionary with keys and a list of values from above "indeed_posts")

    indeed_dict_list=defaultdict(list)

    # # Fields for our DF 

    indeed_spec=['Company','Job','Link','Salary','Location','Job_Posted_Date']

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
    # csv_file= 'output.csv'
    # df.to_csv(csv_file, index=False)


    # def send_email(to_email, attachment_path):
    #     email = "dailyreports530@gmail.com"        # Your Gmail email
    #     password = "eoykzgqohlmgpqox"                 # Your Gmail password

    #     msg = MIMEMultipart()
    #     msg["From"] = email
    #     msg["To"] = to_email
    #     msg["Subject"] = f"{skill} roles from Indeed in {place}"

    #     # Attach the CSV file
    #     with open(attachment_path, 'rb') as file:
    #         attachment = MIMEBase("application", "octet-stream")
    #         attachment.set_payload(file.read())
    #         encoders.encode_base64(attachment)
    #         attachment.add_header("Content-Disposition", "attachment", filename=csv_file)
    #         msg.attach(attachment)

    #     # Send the email
    #     with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    #         server.login(email, password)
    #         server.send_message(msg)
    #         server.quit()

    # to_email = 'dailyreports530@gmail.com; owenjeong530@gmail.com'
    # send_email(to_email, csv_file)

