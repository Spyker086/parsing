
import requests
import json

url = 'https://api.github.com/users/'
username = 'Spyker086'
p = url + username + '/repos'

repos = requests.get(url + username + '/repos').json()
repos_list = []

for i in range(len(repos)):
    repos_list.append(repos[i].get('name'))

with open('task1.json', 'w') as f:
    json.dump(repos_list, f, indent=1)

print(repos_list)
