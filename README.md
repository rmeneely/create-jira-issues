# Create Jira issues
This GitHub Action creates Jira issues specified via an input file (JSON).

## Usage
```yaml
    - uses: rmeneely/create-jira-issues@v1
      with:
        input: <filename>
        url: <base url>
        user_email: Jira user email
        api_token: Jira user API token
```

### Inputs

| Name       | Description                               | Default     | Required |
| ---------- |:----------------------------------------- | :-----------|:---------|
| input      | File specifying issues to create (JSON)   | issues.json | False    |
| url        | Base URL e.g. http://myjira.atlassian.com | none        | True     |
| user_email | Jira email for authentication        | none        | True     |
| api_token  | Jira API token for authentication    | none        | True     |


## Examples
```yaml
    # Creates Jira issues specified via an input file (JSON)
    - uses: rmeneely/create-jira-issues@v1
      with:
        input: jira_issues.json
        url: http://myjira.atlassian.com
        user_email: me@mydomain.com
        api_token: asdasdasdasdfafsldjfhnsdfkjsdbfskfbjskfbksjlsjfkjsbndvkjsbksbfksjbfknjnbfklj
```

### Example input file - creating Sub-tasks for existing issue
```json
{
  "issue": [
    {
      "fields": {
        "project": {
          "key": "RT"
        },
        "parent": {
          "key": "RT-9"
        },
        "summary": "QA feature 38",
        "description": "Complete QA testing for feature 38",
        "issuetype": {
          "name": "Sub-task"
        },
        "assignee": {
          "id": "624c8e42ad6b4e006aa89b65"
        }
      }
    },
    {
      "fields": {
        "project": {
          "key": "RT"
        },
        "parent": {
          "key": "RT-9"
        },
        "summary": "QA feature 39",
        "description": "Complete QA testing for feature 39",
        "issuetype": {
          "name": "Sub-task"
        },
        "assignee": {
          "id": "624c8e42ad6b4e006aa89b65"
        }
      }
    }
  ]
}
```
See [Jira REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-post) for details on JSON file options


## Output
```shell
steps.create-jira-issues.outputs.issues - Set to comma separated list of created issue keys
```

## License
The MIT License (MIT)
