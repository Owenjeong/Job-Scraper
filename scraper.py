import streamlit as st
import sys
sys.path.insert(0, 'C:/Projects/Project/job_scraping/job-scraper')
from glassdoor.acct import glassdoor_acct
from illinoisjoblink.acct import illinois_acct
from indeed.indeed_scrap import indeed_acct
from ziprecruiter.zip_acct import zip_acct
import pandas as pd
from io import BytesIO
import time

def to_csv(df):
    output = BytesIO()
    df.to_csv(output, index=False, encoding='utf-8')
    output.seek(0)
    return output

st.set_page_config(page_title="Job Scraper",
                  page_icon=":chart_with_upwards_trend:", 
                  layout="wide",
                  menu_items=None)


skill = st.selectbox('Title', ('Financial Analyst','Accountant'))
place = st.selectbox('Location',('Chicago, IL','United States'))
no_of_pages = 5
age = '7'

indeed, ziprecruiter = st.tabs(['Indeed', 'ZipRecruiter'])

start_time = time.time()

with indeed:
    with st.spinner('In progress...'):
        summit_btm = st.button('Find Indeed')

        if summit_btm:
            df = indeed_acct(skill, place, age, no_of_pages)
            time = (time.time() - start_time)
            st.write("It took {t:.2f} seconds to pull pull posts".format(t=time))
            st.dataframe(df)

            
            if not df.empty:
                csv = to_csv(df) 
                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name='jobs_data.csv',
                    mime='text/csv',
                )


with ziprecruiter:
    with st.spinner('In progress...'):
        summit_btm2 = st.button('Find ZipRecruiter')

        if summit_btm2:
            df = zip_acct(skill, place, age, no_of_pages)
            time = (time.time() - start_time)
            st.write("It took {t:.2f} seconds to pull pull posts".format(t=time))
            st.dataframe(df)

            
            if not df.empty:
                csv = to_csv(df) 
                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name='jobs_data.csv',
                    mime='text/csv',
                )
