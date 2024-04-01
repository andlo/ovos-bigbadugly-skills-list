import requests
import json
import ast
from datetime import datetime
from pytz import timezone
import time
import re

from github import Github
from os.path import isfile

from collections import OrderedDict
from typing import Optional
from difflib import SequenceMatcher
import urllib.parse
import pypi_search  

def search_github():
    if not isfile('github.json'):
        print('Searching Github...')
        github_tokenfile = open("token.txt", "r")
        GITHUB_TOKEN = github_tokenfile.readline().rstrip('\n')
        skills = []
        total = 0
        added = 0
        page = 1

        proc = 1
        page = 0
#        print('Daterange: ' + date)
#           GITHUB_API_URL = "https://api.github.com/search/repositories?q='language:python+OVOS'in:readme+'OVOS'in:description+'OVOS'in:name+archived:false+created:" + date
#            GITHUB_API_URL = "https://api.github.com/search/search?q='entry_points' +'ovos.plugin.skill'"
#            GITHUB_API_URL = "https://api.github.com/search/repositories?q=ovos-skill+'language:python+archived:false+created:" + date
        search_words = ['ovos', 'mycroft', 'neon', 'skill']
        for word in search_words:
            GITHUB_API_URL = "https://api.github.com/search/repositories?q=" + word + "+archived:false+language:python" 
            request = requests.get(GITHUB_API_URL + '&per_page=100&page=0', headers={ 'Authorization': 'Bearer ' + GITHUB_TOKEN})
            result = request.json()
            for item in result['items']:
                skills.append(item)
                total = total +1
            while 'next' in request.links.keys():
                request=requests.get(request.links['next']['url'],headers={"Authorization": 'Bearer ' + GITHUB_TOKEN})
                result = request.json()
                for item in result['items']:
                    skills.append(item)
                    list.append(item['full_name'])
                    total = total +1
            #print('total ' + str(len(skills)))
        repo_file = open('github.json', 'w')
        repo_file.write(json.dumps(skills, ensure_ascii=False, indent=2))
        repo_file.close()
        repo_file = open('github_list.json', 'w')
        repo_file.write(json.dumps(list, ensure_ascii=False, indent=2))
        repo_file.close()
        
        print(skills.count)    
        print('Total git repos: ' + str(total))

#search_github()



result = pypi_search
print(result)