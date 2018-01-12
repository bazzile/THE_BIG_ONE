#!/usr/bin/python
import os
import requests
import urllib.parse
import bs4
import re

dst_dir = r'V:\POKROV\04_ASTER\BASIC\4'
link = 'https://e4ftl01.cr.usgs.gov/PullDir/030429753818118/'
username = "lobanov"
password = "RAjf_Ude2jo854fg"


# overriding requests.Session.rebuild_auth to mantain headers when redirected
# from https://wiki.earthdata.nasa.gov/display/EL/How+To+Access+Data+With+Python


class SessionWithHeaderRedirection(requests.Session):
    AUTH_HOST = 'urs.earthdata.nasa.gov'

    def __init__(self, username, password):
        super().__init__()
        self.auth = (username, password)
        # Overrides from the library to keep headers when redirected to or from
        # the NASA auth host.

    def rebuild_auth(self, prepared_request, response):
        headers = prepared_request.headers
        url = prepared_request.url
        if 'Authorization' in headers:
            original_parsed = requests.utils.urlparse(response.request.url)
            redirect_parsed = requests.utils.urlparse(url)
            if (original_parsed.hostname != redirect_parsed.hostname) \
                    and redirect_parsed.hostname != self.AUTH_HOST \
                    and original_parsed.hostname != self.AUTH_HOST:
                del headers['Authorization']
        return

# create session with the user credentials that will be used to authenticate access to the data
session = SessionWithHeaderRedirection(username, password)

web_content = requests.get(link)
soup = bs4.BeautifulSoup(web_content.text, "html.parser")

dem_links = soup.find_all(text=re.compile(r'.*\.zip$', re.IGNORECASE), href=True)
total_file_num = len(dem_links)
for i, dem_link in enumerate(dem_links):
    print('Processing {}/{} - {}'.format(i + 1, total_file_num, dem_link['href']))
    full_dem_link = urllib.parse.urljoin(link, dem_link['href'])
    response = session.get(full_dem_link)
    with open(os.path.join(dst_dir, dem_link['href']), 'wb') as f:
        f.write(response.content)
