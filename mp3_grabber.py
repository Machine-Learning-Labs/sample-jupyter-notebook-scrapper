#!/usr/bin/env python
# coding: utf-8

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

output_url = {}

# TODO Edit here to replace for the REAL URL (line 14)
input_url = [
    {
        "url":f"http://language.courseware/les/<%page%>/",
        "initial":80,
        "ending":84,
        "folder_name": "lesson_1"
    }
]

## Prepare all url to download
for lesson in input_url:
    
    url=lesson.get('url')
    start=lesson.get('initial')
    end=lesson.get('ending')
    folder=lesson.get('folder_name')
    
    elements = range(start, end)
    output_url[folder]=[]
    
    for element in elements:
        url_fulfilled = url.replace('<%page%>', str(element))
        output_url[folder].append(url_fulfilled)


for folder in output_url:
    
    print(f'>>> Preparing to download: {folder}')
    for url_specific in output_url[folder]:

        # Prepare the url base
        uri_components = urlparse(url_specific)

        # Download the page
        html_doc = requests.get(url_specific)
        soup = BeautifulSoup(html_doc.content, 'html.parser')
        candidate_links = soup.find_all('a', class_="adownload")
        mp3_link = candidate_links.pop().get('href')

        # Download the mp3
        #mp3_uri = f'{uri_components.scheme}://{uri_components.netloc}/{mp3_link}'
        mp3_uri = f'{uri_components.scheme}://{uri_components.netloc}{mp3_link}'
        mp3_file = requests.get(mp3_uri, allow_redirects=True)
        filename = f'{folder}{uri_components.path}.mp3'.replace('/','_')
        open(filename, 'wb').write(mp3_file.content)
        
        print(f'{filename} saved')

