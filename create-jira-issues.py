#!/usr/bin/env python3

# Modules
import argparse
import re
import os
import json
import base64
import requests
from requests.auth import HTTPBasicAuth
from github_action_utils import set_output

def parse_args():
    # Arguments
    parser = argparse.ArgumentParser(description='Create Jira issues')
    parser.add_argument('--input', type=str, help='input file (JSON)')
    parser.add_argument('--url', type=str, help='URL to Jira instance')
    parser.add_argument('--user_email', type=str, help='User email')
    parser.add_argument('--api_token', type=str, help='API token')
    args = parser.parse_args()
    return args

def main():
    # Default values
    input = 'issues.json'
    url = ''
    token = ''

    # Get arguments
    args = parse_args()
    if args.input:
        input = args.input
    if args.url:
        url = args.url
    else:
        print("Error: --url <URL> required", file=sys.stderr)
        raise SystemExit(1)
    if args.user_email:
        user_email = args.user_email.strip()
    else:
        print("Error: --user_email <user email> required", file=sys.stderr)
        raise SystemExit(1)
    if args.api_token:
        api_token = args.api_token.strip()
    else:
        print("Error: --api_token <API token> required", file=sys.stderr)
        raise SystemExit(1)

    # Create authentication token - user_email:api_token (base64)
    token = base64.b64encode(bytes(user_email + ':' + api_token, 'utf-8')).decode('utf-8')

    # Read issues (JSON)
    with open(input) as file:
        data = json.load(file)

    # Create Jira issues
    url = url + '/rest/api/2/issue'
    headers = {'Content-Type': 'application/json', 'Authorization': 'Basic ' + token}
    issues = []
    for issue in data['issue']:
        payload = json.dumps(issue)
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 201:
            issue_key = response.json()["key"]
            issues.append(issue_key)
            print('Jira issue {} created successfully!'.format(issue_key))
        else:
            print('Failed to create Jira issue. Status code:', response.status_code)
            error_messages = response.json().get("errorMessages")
            if error_messages:
                for error_message in error_messages:
                    print(error_message)


    # Set GitHub Action output
    if "GITHUB_OUTPUT" in os.environ:
        set_output('issues', ','.join(issues))
    else:
        print("{}".format(','.join(issues)))

if __name__ == '__main__':
    main()
# End of file
