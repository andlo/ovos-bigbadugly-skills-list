import json

f = open('../_data/skills.json')
skills = json.load(f)
tags = {} 
categories = []
non_categories = ['-', 'skill', 'ovos', 'neongecko', 'neonai']
for skill in skills:
    for tag in skill['tags']:
        tag = tag.lower()
        #print(tag)
        tags[tag] = tags.get(tag, 0) +1
for tag in tags:        
    if tags.get(tag) > 5:
        if tag not in non_categories:
            categories.append(tag)
        #print(tag)
#print(tags)
print(categories)