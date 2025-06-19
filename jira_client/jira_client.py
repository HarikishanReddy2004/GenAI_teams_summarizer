# jira_client/jira_client.py

import requests
from requests.auth import HTTPBasicAuth
from config import JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

def get_active_sprint(board_id):
    url = f"{JIRA_BASE_URL}/rest/agile/1.0/board/{board_id}/sprint?state=active"
    response = requests.get(url,auth=auth)
    if response.status_code == 200:
        sprints = response.json().get('values', [])
        if sprints:
            return sprints[0]['id']
    return None

def get_issues_in_sprint(sprint_id):
    url = f"{JIRA_BASE_URL}/rest/agile/1.0/sprint/{sprint_id}/issue"
    response = requests.get(url, headers=headers, auth=auth)
    issues = {}
    if response.status_code == 200:
        for issue in response.json().get('issues', []):
            issues[issue['key']] = issue['fields']['summary']
    return issues




def post_comment(issue_key, comment_body):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/comment"

    # Prepare the payload using Jira's Atlassian Document Format (ADF)
    payload = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": comment_body
                        }
                    ]
                }
            ]
        }
    }

    response = requests.post(url, json=payload ,auth=auth)

    if not response.ok:
        print(f"Error posting comment to {issue_key}: {response.status_code} - {response.text}")

    return response.status_code
