# !pip install linkedin-api requests
from linkedin_api import Linkedin
import pandas as pd
from bs4 import BeautifulSoup
import requests
# jsessionid_cookie = "ajax:4340456177189035515"
def main():
    session_cookie = "AQEDATN2zwoBXh4rAAABlXRzjqMAAAGVmIASo00AgdkromPexE3o29Gu9bJI4pzOHtS2jY7VialLBVzRoFXfegUSSM-Bei4w-Lw0QBnIMaKhdrdfN33acYDN4_ohEbl4aVl54iD0dkmtDswvdBH-Pv4W"
    jsessionid_cookie = "ajax:4340456177189035515"
    print('hello')
    cookie_jar = requests.cookies.RequestsCookieJar()
    cookie_jar.set("li_at", session_cookie)
    cookie_jar.set("JSESSIONID", jsessionid_cookie)
    api = Linkedin("", "", cookies=cookie_jar)
    print(api)

if __name__ == "__main__":
    main()