import requests
import os

API_URL = 'https://api.github.com"
REPO = os.getenv('GITHUB_REPOSITORY')
TOKEN = os.getenv('GITHUB_TOKEN')

def fetch_open_issues(repo):
    url = f"{API_URL}/repos/{repo}/issues"
    headers = {"Authorization": f"token={TOKEN}"}
    response = requests.get(url, headers=headers, params={"state": "open"})
    if response.status_code == 200:
        issues = response.json()
        if issues:
            print(f"open issues in repository {repo}:")
            for issue in issues:
                print(f"- {issue['title']} :({issue['number']})")
        else:
            print(f"No open issues found in repository {repo}.")
    else:
        print(f"Error fetching open issues: {response.status_code}")
    

if __name__ == "__main__":
    fetch_open_issues(REPO)