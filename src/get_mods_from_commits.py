#!/usr/bin/env python
""" get_mods_from_commits.py
"""
import csv
import re
import sys

def is_commit(line):
    return re.match("^[0-9a-f]{40}", line)

def get_mod(line):
    match = re.match("^[A-Z]", line)
    return match[0] if match else ""

def get_path(line):
    match = re.match("^([A-Z]\s+)(.*)", line)
    return match[2] if match else ""

def parse_commit_mod_log(source):
    commit = False
    files = []
    for line in source:
        if is_commit(line):
            if files:
                yield {
                    "commit": commit,
                    "files": files
                }
            files = []
            commit = line.strip()
        else:
            files.append({
                "mod": get_mod(line).strip(),
                "path": get_path(line).strip()
            })
    if files:
        yield {
            "commit": commit,
            "files": files
        }

def print_commit_mod_csv(records):
    fields = ["commit", "mod", "path"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fields, lineterminator="\n")

    writer.writeheader()
    rows = [{
        "commit": record["commit"],
        "mod": f["mod"],
        "path": f["path"]
    } for record in records for f in record["files"]]
    writer.writerows(rows)

def main():
    records = parse_commit_mod_log(sys.stdin)
    print_commit_mod_csv(records)


if __name__ == "__main__":
    main()
