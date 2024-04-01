import requests
import json
import ast
from datetime import datetime
from pytz import timezone
import time
import re

#from github import Github
from os import listdir, getcwd
from os.path import isfile, dirname, join

from collections import OrderedDict
from typing import Optional
from difflib import SequenceMatcher
import urllib.parse


'''
Generates a json data with all skills found nby searching github. For every skill
skills info is added so endresult is a json data with all github info and skill find_title_info

skill info is same info as used my market, and added market status and evt. pending lables.

skill __init__.py is parsed ad checked by AST to check if it looks OK.

'''
ACCESS_TOKEN = ''

request = requests.get(
    "https://api.github.com/search/issues?q=repo:MycroftAI/mycroft-skills+state:open+type:pr&sort=created&order=asc").text
MARKET_PR = json.loads(request)

request = requests.get(
    'https://raw.githubusercontent.com/MycroftAI/mycroft-skills-data/19.08/skill-metadata.json').text
MARKET = json.loads(request)


def check_if_skill(repo_url, branch):
    """ Checks if a repo has setuip.py and it has OVOSSkill inside """
    setup_py = None
    setup_py_txt = None
    setup_py = repo_url.replace(
        'https://github.com/', 'https://raw.githubusercontent.com/') + '/' + branch + '/setup.py'
    setup_py_txt = requests.get(setup_py).text
    if setup_py_txt.find('ovos.plugin.skill') != -1:
        return True
    else:
        return False

def check_source_code(repo_url, branch):
    """ Checks quality of code using ast """
    init_py = None
    init_py_txt = None
    init_py = repo_url.replace(
        'https://github.com/', 'https://raw.githubusercontent.com/') + '/' + branch + '/__init__.py'
    init_py_txt = requests.get(init_py).text
    try:
        result = ast.parse(init_py_txt)
        return True
    except SyntaxError as exc:
        return False

def cleanhtml(raw_html):
    """ Clean html from text """
    # cleanr = re.compile('<.*?>')
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def extract_sections(readme_content: str) -> OrderedDict:
    """ Extracts sections from README.MD """
    last_section = ''
    sections = OrderedDict({last_section: ''})
    for line in readme_content.split('\n'):
        line = line.strip()
        if line.startswith('# ') or line.startswith('## '):
            last_section = line.strip('# ')
            sections[last_section] = ''
        else:
            sections[last_section] += '\n' + line
    for section_name in list(sections):
        sections[section_name] = sections[section_name].strip()
    sections[''] = sections.pop('')  # Shift to end
    return sections

def format_sentence(s: str) -> str:
    """ 'this is a test' -> 'This is a test.' """
    s = caps(s)
    if s and s[-1].isalnum():
        return s + '.'
    return s

def find_title_info(sections: dict) -> tuple:
    """ Get title from the section with an icon """
    title_section = None
    for section in sections:
        if "<img" in section:
            title_section = section
            break
    if not title_section:
        # Attempt old scheme - first section header is the title
        title_section = next(iter(sections))
        return title_section, ""   # Should never be allowed in repo!

    # Remove traces of any <img> tag that might exist, get text that follows
    title = title_section.split("/>")[-1].strip()
    short_desc = sections[title_section]
    return title, short_desc

def find_icon(sections: dict, repo: str, tree: str) -> tuple:
    """ Get first section's title (icon is in the title itself), like:
        <img src='https://rawgi...' card_color='maroon' height='50'/> Skill Name
        Get first section's title """
    # Get section name with the icon
    title_section = None
    for section in sections:
        if "<img" in section:
            title_section = section
            break
    if not title_section:
        return None, None, None
    url = None
    name = None
    color = None
    prev = ''
    for part in title_section.split("'"):
        part = part.strip()
        if prev.endswith("src="):
            url = part
        elif prev.endswith("card_color="):
            color = part
        prev = part

    # Check if URL is a Font Awesome preview image
    if url and url.startswith("https://rawgithub.com/FortAwesome/Font-Awesome"):
        # Break down down just the filename part, e.g.
        #   "https://rawgithub...vg/solid/microchip.svg" -> "microchip"
        name = url.split('/')[-1].split(".")[0]
        url = None
    elif url:
        if not urllib.parse.urlparse(url).netloc:
            # Assume this is a local reference, expand it to a full-path
            url = (repo.replace("github.com", "raw.githubusercontent.com") +
                   '/' + tree + '/' + url)
    return url, name, color

def find_section(name: str, sections: dict, min_conf: float = 0.5) -> Optional[str]:
    """ Return the section with heading that matches `name` most closely """
    title, conf = max([(title, compare(title, name)) for title in sections], key=lambda x: x[1])

    return None if conf < min_conf else sections[title]

def find_examples(sections: dict) -> list:
    """ Example: {'Examples': ' - "Hey Mycroft, how are you?"\n - "Hey Mycroft, perform test" <<< Does a test'}  # nopep8
        Returns: ['How are you?', 'Perform test.'] """
    return re.findall(
        string=(find_section('examples', sections) or
                find_section('usage', sections) or ''),
        pattern=r'(?<=[-*]).*', flags=re.MULTILINE
    )

def make_credits(lines: str) -> list:
    """ Convert multiline credits into list
        Ex: @acmcgee\nMycroftAI (@MycroftAI)\nTom's great songs """
    result = []
    for line in lines.splitlines():
        words = []
        username = None
        for word in line.split():
            word = word.strip("()")
            if word.startswith("@"):
                username = word[1:]
            else:
                words.append(word)
        if words and username:
            result.append({"name": " ".join(words),
                           "github_id": username})
        elif words:
            result.append({"name": " ".join(words)})
        elif username:
            result.append({"github_id": username})
    return result

def parse_example(example: str) -> str:
    """ "hey mycroft, what is this" -> What is this? """
    example = example.strip(' \n"\'`')
    example = re.split(r'["`]', example)[0]
    # Remove "Hey Mycroft, "
    for prefix in ['hey mycroft', 'mycroft', 'hey-mycroft']:
        if example.lower().startswith(prefix):
            example = example[len(prefix):]
    example = example.strip(' ,')  # Fix ", " from "Hey Mycroft, ..."
    if any(
            example.lower().startswith(word + suffix + ' ')
            for word in ['who', 'what', 'when', 'where']
            for suffix in ["'s", "s", "", "'d", "d" "'re", "re"]
    ):
        example = example.rstrip('?.') + '?'
    example = format_sentence(example)
    return example

def caps(s: str) -> str:
    """ Capitalize first letter without lowercasing the rest"""
    return s[:1].upper() + s[1:]

def compare(a: str, b: str) -> float:
    """ compare str a with b """
    return SequenceMatcher(a=a.lower(), b=b.lower()).ratio()

def norm(x: str) -> str:
    """ Normalize str"""
    return x.lower().replace('-', ' ')

def search_github():
    if not isfile('github_search.json'):
        print('Searching Github...')
        github_tokenfile = open("token.txt", "r")
        GITHUB_TOKEN = github_tokenfile.readline().rstrip('\n')
        repo = []
        total = 0
        search_words = ['ovos', 'mycroft', 'neon', 'skill']
        #search_words = ['ovos-skill']
        for word in search_words:
            print('Searching for ' + word)
            GITHUB_API_URL = "https://api.github.com/search/repositories?q=" + word + "+archived:false+language:python" 
            request = requests.get(GITHUB_API_URL + '&per_page=100&page=0', headers={ 'Authorization': 'Bearer ' + GITHUB_TOKEN})
            result = request.json()
            print('Found: ' + str(result['items'].count))
            for item in result['items']:
                repo.append(item)
                total = total +1
            while 'next' in request.links.keys():
                request=requests.get(request.links['next']['url'],headers={"Authorization": 'Bearer ' + GITHUB_TOKEN})
                result = request.json()
                for item in result['items']:
                    repo.append(item)
                    total = total +1
        f = open('github_search.json', 'w')
        f.write(json.dumps(repo, ensure_ascii=False, indent=2))
        f.close()

def process_repos():
    print('Processing Github repos...')
    f = open('github_search.json')
    github_search = json.load(f)
    skills = []
    added = 0
    proc = 0
    for repo in github_search:
        #print("Processing " + str(proc) +"/" + str(len(github_search)) + " " + repo['full_name'])
        if check_if_skill(repo['html_url'], repo['default_branch']) is True:
            skills.append(repo)
            #list.append(repo['full_name'])
            print("Added " + repo['name'] + '.' + repo['owner']['login'])
            added = added + 1
        proc = proc + 1
    f = open('github_skills.json', 'w')
    f.write(json.dumps(skills, ensure_ascii=False, indent=2))
    f.close()
    #f = open('github_list.json', 'w')
    #f.write(json.dumps(list, ensure_ascii=False, indent=2))
    #f.close()
    print('Found skills: ' + str(added))
    return skills

def make_skill_json():
    print('Processing skills and making .json files...')
        
    result = []
    f = open('github_skills.json')
    repos = json.load(f)
    proc = 0
    total = 0
    added = 0
    for repo in repos:
        print("Processing " + str(proc) +"/" + str(len(result)) + " " + repo['full_name'])
        """ Generate an skil-repo entry """
        skill = {}
        readme_url = repo['html_url'].replace(
            'https://github.com/', 'https://raw.githubusercontent.com/') + '/' + repo["default_branch"] + '/README.md'
        readme_txt = requests.get(readme_url).text
        sections = extract_sections(readme_txt)
        skill['skill_id'] = repo['name'] + '.' + repo['owner']['login']
        skill['source'] = repo['html_url']
        #skill['package_name']
        #skill['pip_spec']
        if repo['license']:
            skill['license'] = repo['license']['spdx_id']
        #skill['exta_plugins']
        skill['name'] = cleanhtml(find_title_info(sections)[0])
        skill['description'] = cleanhtml(format_sentence(find_section('About', sections) or
                                                         find_section('Description', sections) or ''))
        skill['examples'] = [parse_example(i) for i in find_examples(sections)]
        skill['tags'] = [cat.replace('*', '') for cat in sorted((find_section('Category', sections, 0.9) or '').split()) +
                        (find_section('Tags', sections) or '').replace('#', '').split()]
        skill['icon'] = find_icon(sections, repo['html_url'], repo["default_branch"])[0]
        #skill['images'] 
        skill['source'] = repo['html_url']
        #skill['package_name'] = repo['name']
        if repo['license']:
            skill['license'] = repo['license']['spdx_id']
        skill['author'] = repo['owner']['login']
        #skill['name'] = repo[]
        #skill['description'] = 

        filename = "../_data/" + repo['name'] + '.' + repo['owner']['login'] + '.json'
        f = open(filename, 'w')
        f.write(json.dumps(skill, ensure_ascii=False, indent=2))
        f.close()

def make_skill_store():
    output = {
        "version": "https://jsonfeed.org/version/1",
        "title": "The big, bad and ugly skills store",
        "description": "Welcome to The big, bad and ugly skills store",
        "home_page_url": "https://andlo.github.io/bigbadugly-skills-store",
        "feed_url": "https://andlo.github.io/bigbadugly-skills-store/skills.json",
        "items": []
    }
    dir_to_check = dirname(__file__) + '/../_data/' or join(getcwd() + '/../_data/', "main")
    print(dir_to_check)
    for skill in [f for f in listdir(dir_to_check) if f.endswith(".json")]:
        with open(join(dir_to_check, skill)) as f:
            output["items"].append(json.load(f))

    with open(join(dir_to_check, "skills.json"), "w") as f:
        json.dump(output, f, indent=4)

#search_github()
process_repos()
make_skill_json()
make_skill_store()

