
import requests 
from datetime import datetime


def get_github_repos(date, language='python'):
        results = requests.get(f'https://api.github.com/search/repositories?q=created:">{date}"language:{language}&sort=stars&order=desc&per_page=10').json()

        repo_list = []
        for repo in results['items']:
                d_tmp = {'repository_ID': repo['id'],
                        'name': repo['name'],
                        'URL': repo['html_url'],
                        'created_date': datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ'),


                        'number_of_stars': repo['stargazers_count']}
                repo_list.append(d_tmp)
        return repo_list

date = "2023-04-30"
repo_list = get_github_repos(date)
for repo in repo_list:
        print(repo['name'])
        print(repo['URL'])
        print('---')

