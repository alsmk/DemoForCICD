import requests
import sys
import os 

# GitHub API URL format
API_URL = "https://api.github.com"
REPO = os.getenv('GITHUB_REPOSITORY')  # Replace with the target repository (e.g., 'owner/repo')
TOKEN = os.getenv('GITHUB_TOKEN')
  # Replace with your GitHub Personal Access Token

# Function to make authenticated GitHub API requests
def github_api_request(url, params=None):
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.json().get('message')}")
        sys.exit(1)

# Fetch the latest commit
def fetch_latest_commit(repo):
    url = f"{API_URL}/repos/{repo}/commits"
    commits = github_api_request(url, params={"per_page": 1})
    latest_commit = commits[0]
    print("Latest Commit Details:")
    print(f"Commit SHA: {latest_commit['sha']}")
    print(f"Author: {latest_commit['commit']['author']['name']}")
    print(f"Message: {latest_commit['commit']['message']}")
    print(f"Date: {latest_commit['commit']['author']['date']}\n")

# Fetch the list of open issues
def fetch_open_issues(repo):
    print("Open Issues:")
    page = 1
    while True:
        url = f"{API_URL}/repos/{repo}/issues"
        issues = github_api_request(url, params={"state": "open", "per_page": 30, "page": page})
        if not issues:
            break
        for issue in issues:
            # Exclude pull requests (GitHub considers PRs as issues with a 'pull_request' field)
            if "pull_request" not in issue:
                print(f"Issue: {issue['title']} (Status: {issue['state']})")
        page += 1
    print()

# Fetch the list of pull requests
def fetch_pull_requests(repo):
    print("Pull Requests:")
    page = 1
    while True:
        url = f"{API_URL}/repos/{repo}/pulls"
        pulls = github_api_request(url, params={"state": "open", "per_page": 30, "page": page})
        if not pulls:
            break
        for pr in pulls:
            print(f"PR: {pr['title']} (Status: {pr['state']})")
        page += 1
    print()

# Main function to execute all tasks
def main():
    fetch_latest_commit(REPO)
    fetch_open_issues(REPO)
    fetch_pull_requests(REPO)

if __name__ == "__main__":
    main()
