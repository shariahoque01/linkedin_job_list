# Linkedin API 



## job_search.py: 
### collect_clean_data: <br>
This function returns a list of unique LinkedIn job IDs by cleaning the raw job data: filtering job titles, removing reposted jobs, and dropping duplicates

This script scrapes job data from linkedin api.
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

### job_data_scrape: <br>
scrapes LinkedIn job pages for details using job IDs, cleans the data, and returns it as a structured DataFrame
1. 






### Miscellneous
1. To get out of conda base: conda config --set auto_activate_base False
To make it true again: conda config --set auto_activate_base True
2. activating vrtual env:
```bash 
python3 -m venv myvenv
source myvenv/bin/activate
deactivate

-- to do:
clean the data: html tag
```