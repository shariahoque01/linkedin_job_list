# !pip install linkedin-api requests
from linkedin_api import Linkedin
import pandas as pd
from bs4 import BeautifulSoup
import requests
jsessionid_cookie = "ajax:4340456177189035515"

# Create a RequestsCookieJar object
cookie_jar = requests.cookies.RequestsCookieJar()
cookie_jar.set("li_at", session_cookie)
cookie_jar.set("JSESSIONID", jsessionid_cookie)

api = Linkedin("", "", cookies=cookie_jar)

# print(api)

# Fetch the profile using the public ID or urn_id
profile = api.get_profile('dummy-account-9a21aa201')
print(profile)