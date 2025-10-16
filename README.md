
# System Design:
<img width="579" height="532" alt="image" src="https://github.com/user-attachments/assets/9a7cc572-5f60-478e-a44d-59fff8c980cd" />


# Description of the process:
## 1. job_search.py: 
### collect_clean_data(): <br>
This function returns a list of unique LinkedIn job IDs by cleaning the raw job data: filtering job titles, removing reposted jobs, and dropping duplicates

This script scrapes job data from the LinkedIn API.
1. Logs into LinkedIn API using cookies stored in environment variables
2. Data Extraction: <br>
function fetches LinkedIn jobs with the keyword "Data" posted within the last 36 hours, with a maximum limit of 10,000 results 
```bash
data = api.search_jobs(limit = 10000, keywords = 'Data',listed_at = 129600)
```

- search_jobs function creates these fields: 'trackingUrn', 'repostedJob', 'title', '$recipeTypes', 'posterId',
       '$type', 'contentSource', 'entityUrn'


3. Data transformation: <br>
- job_id field is created from the 'trackingUrn'
```bash 
original_df['job_id'] = original_df['trackingUrn'].str.split(':').str[-1]
```
- Only keep the necessary fields: 'title', 'job_id', 'repostedJob'
- Filters out jobs with titles that don’t match entry-level
```bash
    filtered_df = df[~df['title'].str.contains("Manager|Lead|Principal|Sr|Senior|Director|III|Mid|Java|JAVA|Intern|Part|Coordinator|Clerk|Head|Entry|Chief|President|VP", case=False)]
```

- Removes reposted jobs:
```bash
    filtered_df2 = filtered_df[filtered_df['repostedJob'] == False]
```

- Removes duplicates:
```bash
    filtered_df2 = filtered_df2.drop_duplicates(subset=['job_id'], keep='first')
```

### job_data_scrape(): <br>
scrapes LinkedIn job pages for details using job IDs, cleans the data, and returns it as a structured DataFrame
1. 



## 2. linkedinAPI.py
### Main_df():
Runs both functions, collect_clean_data and job_data_scrape, together to create a complete dataset of target job lists with information called sample2

## 3. main.py:
The script uses Google API authentication to write job data extracted from linkedinAPI.py into a Google Sheet, ensuring data deduplication

## 4. actions.yml:
Path: .github/workflows/actions.yml
This file contains a YAML-based GitHub Actions workflow that triggers automation

# Final Product:
https://docs.google.com/spreadsheets/d/1tk33s7cDus-1kPTsMZECGD7kocLNU5KfShpgV_wHrVg/edit?gid=0#gid=0 

### Miscellaneous: 
1. To get out of conda base: conda config --set auto_activate_base False
To make it true again: conda config --set auto_activate_base True
2. activating virtual env:
```bash 
python3 -m venv myvenv
source myvenv/bin/activate
deactivate
```
> [!NOTE]
> The linkedin-api Python library is unofficial and has been discontinued as of October 2025.
> To use the official LinkedIn API, visit LinkedIn’s Developer Documentation. Access is granted only to approved partners who meet LinkedIn’s eligibility requirements.
```
