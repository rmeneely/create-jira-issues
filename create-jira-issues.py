#!/usr/bin/env python3

# Modules
import argparse
import re
import os
import json
import requests
from github_action_utils import set_output

def parse_args():
    # Arguments
    parser = argparse.ArgumentParser(description='Create Jira issues')
    parser.add_argument('--input', type=str, help='input file (JSON)')
    parser.add_argument('--url', type=str, help='URL to Jira instance')
    parser.add_argument('--token', type=str, help='API token (base64)')
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
    if args.token:
        token = args.token
    else:
        print("Error: --token <API token> required", file=sys.stderr)
        raise SystemExit(1)

    # Read issues (JSON)
    with open(input) as file:
        data = json.load(file)

    url = url + '/rest/api/2/issue'
    headers = {'Content-Type': 'application/json', 'Authorization': 'Basic ' + token}
    issues = []
    for payload in data['issue']:
        #print("response = requests.post({}, headers={}, json={})".format(url, headers, payload))
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            issues.append(response['key'])
            print('Jira issue {} created successfully!'.format(response['key'])
        else:
            print('Failed to create Jira issue. Status code:', response.status_code)

    # Set GitHub Action output
    if "GITHUB_OUTPUT" in os.environ:
        set_output('issues', ','.join(issues))
	
if __name__ == '__main__':
    main()
# End of file
