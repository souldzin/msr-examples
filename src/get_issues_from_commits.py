#!/usr/bin/env python
""" get_issues_from_commits.py
"""
import csv
import sys
import re

def get_issues_from_commits(source, issue_regex):
    for line in source:
        issues = set(get_issues(line, issue_regex))
        for issue in issues:
            yield {
                "issue": issue.strip(),
                "commit": get_commit(line).strip(),
                "message": get_message(line).strip()
            }

def get_message(line):
    match = re.search("^([0-9a-f]{40,})(.*)", line.strip())
    return match.group(2) if match else line

def get_commit(line):
    match = re.search("^([0-9a-f]{40,})", line.strip())
    return match.group(1) if match else ""

def get_issues(line, regex):
    return re.findall(regex, line)

def print_issue_commits(records):
    fields = ["issue", "commit", "message"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)

def main():
    args = sys.argv
    arg_issue_regex = args[1] if len(args) > 1 else ""

    if not arg_issue_regex:
        sys.exit("argument required (expected regex for issue)")

    issues = get_issues_from_commits(sys.stdin, arg_issue_regex)
    print_issue_commits(issues)

if __name__ == "__main__":
    main()
