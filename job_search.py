from linkedin_api import Linkedin
import pandas as pd
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os

load_dotenv()

def collect_clean_data():
    session_cookie = os.getenv('SESSION_COOKIE')
    jsessionid_cookie = os.getenv('JSESSIOINID_COOKIE')
    cookie_jar = requests.cookies.RequestsCookieJar()
    cookie_jar.set("li_at", session_cookie)
    cookie_jar.set("JSESSIONID", jsessionid_cookie)
    api = Linkedin("", "", cookies=cookie_jar)
    profile = api.get_profile('dummy-account-9a21aa201')
    # print(profile)
    data = api.search_jobs(limit = 10, keywords = 'Data Engineer',listed_at = 86400)
    original_df = pd.DataFrame(data)
    original_df['job_id'] = original_df['trackingUrn'].str.split(':').str[-1]
    print(f'The original total API count: {original_df.shape}')
    #Reshaping the dataframe
    df = original_df[['title', 'job_id', 'repostedJob']]
    #filtering title to only data engineer
    #need to change it user input; options
    filtered_df = df[~df['title'].str.contains("Manager|Lead|Principal|Sr|Senior|Director|II|III|Mid Level|Java|JAVA", case=False)]
    #selecting only non-reposting job
    filtered_df2 = filtered_df[filtered_df['repostedJob'] == False]
    #dropping duplicates
    filtered_df2 = filtered_df2.drop_duplicates(subset=['job_id'], keep='first')
    #clean df
    print(f'The clean data:{filtered_df2.shape}')
    return filtered_df2['job_id']

def job_data_scrape(job_id):
  job_data2 = []
  for job_id_index in job_id:
    # Linkedin URL (api call)
    url = f"https://www.linkedin.com/jobs/view/{job_id_index}/"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Title
    title_element = soup.find('h1', class_='topcard__title')
    title_element = title_element.text.strip() if title_element else 'N/A'
    # print(title_element)

    #Location
    location = soup.find(class_="sub-nav-cta__meta-text")
    # print(location)

    #Company Apply URL
    application_url = soup.find(id="applyUrl")
    # print(application_url)

    #Days Posted Days
    posted_days = soup.find(class_="posted-time-ago__text topcard__flavor--metadata")
    posted_days = posted_days.text.strip() if posted_days else 'Less than 24 hours or other'
    # print(posted_days)

    #Total Linkedin Applicants(clicks)
    number_of_appplicants = soup.find(class_="num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet")
    number_of_appplicants = number_of_appplicants.text.strip() if number_of_appplicants else 'N/A'
    # print(number_of_appplicants)

    # Company Name
    company_element = soup.find('a', class_='topcard__org-name-link')
    company_element =   company_name = company_element.text.strip() if company_element else 'N/A'
    # print(company_element)

   # add the values in the list
    job_data2.append({
            "Job ID": job_id_index,
            "Company Name": company_name,
            "Title": title_element,
            "Location": location,
            "Linkedin URL": url,
            "Company Apply URL": application_url,
            "Posted Days": posted_days,
            "Total Linkedin Applicants": number_of_appplicants
            # "descriptioin": description
        })

    # Convert list to DataFrame
  pd.set_option('display.max_colwidth', None)
  sample =  pd.DataFrame(job_data2)
  sample = sample.drop_duplicates()
  target_job_data_df = sample[sample['Location'].astype(str).str.contains('NY|NJ|New York', na=False)]
  return sample

