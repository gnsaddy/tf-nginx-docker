import pandas as pd
from sqlalchemy import types, create_engine
from sqlalchemy.orm import sessionmaker
import json
import requests
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np

GITHUB_USERNAME = 'gnsaddy'
GITHUB_TOKEN = ''

github_api = "https://api.github.com"
gh_session = requests.Session()
gh_session.auth = (GITHUB_USERNAME, GITHUB_TOKEN)
url = github_api + '/repos/gnsaddy/tf-nginx-docker/commits'

commits = gh_session.get(url=url)
commits_json = commits.json()


def commits_of_repo_github(repo, owner, api):
    commits = []
    next = True
    i = 1
    while next == True:
        url = f"{api}/repos/{owner}/{repo}/commits?page={i}"
        commit_pg = gh_session.get(url=url)

        if commit_pg.status_code == 200:
            commit_pg_list = [
                dict(item, **{'repo_name': '{}'.format(repo)}) for item in commit_pg.json()]
            commit_pg_list = [
                dict(item, **{'owner': '{}'.format(owner)}) for item in commit_pg_list]
            commits = commits + commit_pg_list
            if 'Link' in commit_pg.headers:
                if 'rel="next"' not in commit_pg.headers['Link']:
                    next = False
            i = i + 1

        else:
            next = False
            print(f"Error: {commit_pg.status_code} - {commit_pg.reason}")

    commit_json = []
    for data in commits:
        commit_json.append({
            'commit_sha': data['sha'],
            'commit_message': data['commit']['message'],
            'commit_date': str(data['commit']['author']['date']),
            'commit_author_name': data['commit']['author']['name'],
            'commit_author_email': data['commit']['author']['email'],
            'commit_committer_name': data['commit']['committer']['name'],
            'commit_committer_email': data['commit']['committer']['email'],
            'repo_name': data['repo_name'],
            'owner': data['owner'],
            'insertion_date': str(pd.to_datetime('today')),
        })

    # insert only if there are new commits
    if len(commit_json) > 0:
        df = pd.DataFrame(commit_json)
        df['commit_date'] = pd.to_datetime(df['commit_date'])
        df['insertion_date'] = pd.to_datetime(df['insertion_date'])

        # convert insertion_date to string
        df['insertion_date'] = df['insertion_date'].dt.strftime(
            '%Y-%m-%d %H:%M:%S')

        df = df.drop_duplicates(subset=['commit_sha'])
        df = df.sort_values(by=['commit_date'])

        # convert commit_date to string
        df['commit_date'] = df['commit_date'].dt.strftime('%Y-%m-%d %H:%M:%S')

        df = df.reset_index(drop=True)
        df['commit_id'] = df.index + 1

        df = df[['commit_id', 'commit_sha', 'commit_message', 'commit_date', 'commit_author_name',
                 'commit_author_email', 'commit_committer_name', 'commit_committer_email', 'repo_name', 'owner', 'insertion_date']]

        # insert to json file
        df.to_json('git-commits.json', orient='records')

    return commits


commits_of_repo_github('tf-nginx-docker', 'gnsaddy', github_api)
