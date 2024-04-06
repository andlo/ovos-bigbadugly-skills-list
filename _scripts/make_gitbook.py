import io
import json
import urllib.request
from PIL import Image
from bs4 import BeautifulSoup
from markdown import markdown
import re
import datetime


json_data = open('../_data/github_skills.json')
github_data = json.load(json_data)
json_data = open('../_data/skills.json')
skills_data = json.load(json_data)

def make_skills_md(skills):
    for skill in skills:
        txt = []
        txt.append('---\n')
        #of.write('titel: ' + skill["skill_info"]["title"] + '\n')
        #short_desc = clean_txt(skill["skill_info"]["short_desc"][:100])
        txt.append('description: ' + 'short description' + '\n')
        #txt.append('categories: ')
        #for category in skill["skill_info"]["categories"]:
        #    txt.append(category + ' ')
        #txt.append('  \n')
        #txt.append('tags: ')
        #for tag in skill["skill_info"]["tags"]:
        #    txt.append(tag + ' ')
        #txt.append('  \n')
        txt.append('---\n\n')
        #txt.append('# ' + skill["skill_info"]["name"] + '  \n')
        txt.append('### _' + skill["skill_id"] + '_  \n')
        
        #icon_img = '../img/' + skill["owner"]["login"] + '_icon.png'
        #get_img(skill["skill_info"]["icon_img"], icon_img)
        #resize_img(icon_img, 50)
        #txt.append(skill["skill_info"]["title"] + '\n\n')
        txt.append('## Description:  \n')
        description = skill["description"]
        description.replace('\n\n', '  \n')
        txt.append(description + '  \n  \n')
        #avatar = '../img/' + skill["owner"]["login"] + '_avatar.png'
        #avatar = get_img(skill["owner"]["avatar_url"], avatar)
        #resize_img(avatar, 50)
        #if not skill["stargazers_count"] == 0: 
        #    for x in range(skill["stargazers_count"]):
        #        txt.append('![](../.gitbook/assets/star.png)')
        #    txt.append('  \n')               
        txt.append('  \n')               
        txt.append('  \n')
        txt.append('## Summary:  \n')
        #txt.append('**Github:** [' + skill["html_url"] + ']' + '(' + skill["html_url"] + ')  \n') 
        #txt.append('**Owner:** [@' + skill["owner"]["login"] + 
        #           '](' + skill["owner"]["html_url"] + 
        #           ')  \n')
        #txt.append('**Created:** ' + nice_time(skill["created_at"]) + 
        #           '  **Last updated:** ' + nice_time(skill["updated_at"]) + '  \n')
        #try:
        #    txt.append('**License:** ' + skill["license"]["name"] + '  \n')
        #    license = True
        #except Exception:
        #    txt.append('**License:** No License  \n')
        #    license = False
        
        skillfile = '../gitbook/skills/' + skill["skill_id"] + '.md' 
        of = open(skillfile, 'w')
        of.writelines(txt)
        of.close()


def nice_time(timestamp):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for c in ['T', 'Z', '-', ':']:
        timestamp = timestamp.replace(c, ' ')
    out = timestamp.split()
    out[1] = months[int(out[1]) - 1]
    return "{} {} {} {}:{}:{} UTC".format(*out)

  
def clean_txt(txt):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    result = re.sub(cleanr, '', txt)
    html = markdown(result)
    result =  ''.join(BeautifulSoup(html,features="html.parser").findAll(text=True))
    result = re.sub(r'http\S+', '', result)
    result = result.replace('[', "")
    result = result.replace(']', "")
    result = result.replace('(', "")
    result = result.replace(')', "")
    result = result.replace('~', "")
    result = result.replace('/', "")
    result = result.replace(':', "")
    result = result.replace('"', "")
    return result     

def get_img(url, filename):
        print(url)
        result = urllib.request.urlretrieve(url, filename)

def resize_img(imgfile, size):
    print(imgfile)
        
    basewidth = size
    img = Image.open(imgfile)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save(imgfile) 

def categories():
    f = open('../_data/skills.json')
    skills = json.load(f)
    tags = {} 
    categories = []
    non_categories = ['-', 'skill', 'ovos', 'neongecko', 'neonai']
    for skill in skills:
        for tag in skill['tags']:
            tag = tag.lower()
            tags[tag] = tags.get(tag, 0) +1
    for tag in tags:        
        if tags.get(tag) > 5:
            if tag not in non_categories:
                categories.append(tag)
    return(categories)

def make_categorylist(skills):
    categorylist = {}
    for skill in skills:
        skillfile = 'skills/' + skill["skill_id"] + '.md' 
        #if not skill["skill_id"].get("categories"):
        #    skill["skill_info"]["categories"] = ['uncategorized']
        for category in skill["skill_info"]["categories"]:
            if (skill["skill_info"]["title"] == "YOUR SKILL NAME") or (skill["skill_info"]["title"] == ""):
                text = "    * [" + clean_txt(skill["name"]) + "](" + skillfile + ")\n"
            else:
                text = "    * [" + clean_txt(skill["skill_info"]["title"]) + "](" + skillfile + ")\n"
            categoryitem = [text]
            if categorylist.get(category):
                cat =  categorylist.get(category)
                cat.append(text)
                categorylist[category] = cat
            else:
                categorylist[category] = categoryitem
    return categorylist

def make_readme(skills):
    #num_of_skills = len(skills)
    skillslist = []
    #for skill in skills:
    #    if skill["skill_info"].get("market_status") == 'In Market':
    #        skillslist.append(skill)
    #num_in_market = len(skillslist)
    
    #skillslist = []
    #for skill in skills:
    #    if skill["skill_info"].get("market_status") == 'Pending Market':
    #        skillslist.append(skill)
    #num_pending = len(skillslist)

    #skillwriters = {}
    #for skill in skills:
    #    if not skillwriters.get(skill["owner"]["login"]):
    #        skillwriters[skill["owner"]["login"]] = skill["owner"]["login"]
    #num_of_writers = len(skillwriters)
    

    readme = open('../gitbook/README.md', 'w')
    readme.write('# Introduction\n')
    readme.write('This list containing most of the Mycroft skills found on GitHub.')
    readme.write('The list includes working, not working new and old skills. The list is ')
    readme.write('not ment as a replacement for the Mycroft Market.  \n')
    readme.write('Installing skills found through this list is only recomended if you know')
    readme.write('what you are doing.  \n')
    readme.write('If you have any issues by using skills found on this list please open a issue on ')
    readme.write('the specific skills github page.  \n')
    readme.write('The Mycroft market can be found at [mycroft.market.ai](http://mycroft.market.ai)  \n')
    readme.write('  \n')
    readme.write('This list is generated and updated at ' + str(datetime.datetime.now().date()) + ' and has been made by searching github ')
    readme.write('looking throu around 1800 ' + ' reposotories that look like mycroft skills. Form those there were found ')
    #readme.write(str(num_of_skills) + 'skills by ' + str(num_of_writers) + ' skill writers. Right now ')
    #readme.write(str(num_in_market) + ' is in Mycroft Market aproved by Mycroft skill tester team. There are ')
    #readme.write(str(num_pending) + ' new skills or updates to skills pending aproval to the Market.') 
    

def make_summary(skills):
    summary = open('../gitbook/SUMMARY.md', 'w')
    summary.write('# Table of contents\n')
    summary.write('* [Introduction](README.md)\n')
    summary.write('* [FAQ](FAQ.md)\n')
    summary.write('## Skills\n')


    skillslist = []
    #summary.write('* In Market  \n')
    #for skill in skills:
    #    if skill["skill_info"].get("market_status") == 'In Market':
    #        skillslist.append(skill)
    categorylist = make_categorylist(skills)
    for category in categorylist:
        summary.write('  * ' + category + '\n')
        summary.writelines(categorylist[category])
    skillslist = []
    for skill in skills:
            skillslist.append(skill)

def make_skillwritermd(skills):
    txt = open('../SUMMARY.md', 'a')
    skillwriters = {}
    for skill in skills:
        if not skillwriters.get(skill["owner"]["login"]):
            skillwriters[skill["owner"]["login"]] = skill["owner"]["login"]
    skillfile = 'skills/' + skill["name"] + '.' + skill["owner"]["login"] + '.md' 

    for writer in skillwriters:
        txt.write('  * @' + writer + '  \n')
        for skill in skills:
            if writer == skill["owner"]["login"]:
                skillfile = 'skills/' + skill["name"] + '.' + skill["owner"]["login"] + '.md' 
                if (skill["skill_info"]["title"] == "YOUR SKILL NAME") or (skill["skill_info"]["title"] == ""):
                    text = "    * [" + clean_txt(skill["name"]) + "](" + skillfile + ")\n"
                else:
                    text = "    * [" + clean_txt(skill["skill_info"]["title"]) + "](" + skillfile + ")\n"
                txt.write(text)
    print(len(skillwriters))





make_readme(skills_data)
make_summary(skills_data)
#make_skillwritermd(skillsdata)
make_skills_md(skills_data)

#print(len(skillsdata))
#resize_img('../.gitbook/assets/star.png', 30)


