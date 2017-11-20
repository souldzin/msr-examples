""" get_issues.py
"""
import json
import sys
import urllib.parse as urlparse
import requests

def get_issues(base_url, jql):
    reqfn = lambda count, start_at: request_search(base_url, jql, count, start_at)
    responses = request_all_recursive(reqfn, 1000, 0)
    issues = [issues for response in responses for issues in response.json()["issues"]]
    return [x["key"] for x in issues]

def request_all_recursive(reqfn, count, start_at):
    response = reqfn(count, start_at)
    yield response
    data = response.json()
    total = data["total"]
    if start_at + count < total:
        for response in request_all_recursive(reqfn, count, start_at + count + 1):
            yield response


def request_search(base_url, jql, count, start_at):
    url = urlparse.urljoin(base_url, "search")
    data = {
        "startAt": start_at,
        "maxResults": count,
        "fields": ["created"]
    }

    if jql:
        data["jql"] = jql

    return requests.post(url, json=data)

def print_issues(issues):
    for issue in issues:
        print(issue)

def main():
    args = sys.argv
    arg_url = args[1] if len(args) > 1 else ""
    arg_jql = args[2] if len(args) > 2 else ""

    if not arg_url:
        sys.exit("Argument is required. Expected url to JIRA api.")

    issues = get_issues(arg_url, arg_jql)
    print_issues(issues)

if __name__ == '__main__':
    main()