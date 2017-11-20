#!/usr/bin/env python
"""parse_cochanged_files
"""

import itertools
import re
import sys

def is_commit(line):
    return re.match("^[0-9a-f]{40}", line)

def parse_commit_files_log(source):
    commit = False
    files = set()
    for line in source:
        if is_commit(line):
            if files:
                yield {
                    'key': commit,
                    'values': files
                }
            commit = line.strip()
            files = set()
        else:
            files.add(line.strip())
    if files:
        yield {
            'key': commit,
            'values': files
        }

def log(message):
    print("[info] " + message)
    sys.stdout.flush()

def find_frequent_combinations(records, n, threshold, comb_limit):
    """
    Args:
        records - this is an iterator of dictionaries with { key, values }
        n - this is the maximum count of combinations to look for
        threshold - the minimum count to keep
        comb_limit - the maximum number of combinations to look at
    """
    counts = {}
    includes = set()
    prunes = set()
    filter_combinations = lambda combs: limit_combinations(combs, comb_limit)
    for i in range(1, n+1):
        log("starting " + str(i) + "-way search")

        if includes:
            records = [x for x in records if is_include(x, includes)]

        log("searching through " + str(len(records)) + " records")
        counts = get_combination_counts(records, i, filter_combinations)

        includes = {k:counts[k] for k in counts if len(counts[k]) >= threshold}
        prunes = {k for k in counts if len(counts[k]) < threshold}

        log("found " + str(len(includes)) + " combinations to include")
        log("found " + str(len(prunes)) + " combinations to potentially prune")

    return includes

def get_combination_counts(records, n, filter_combinations):
    counts = {}
    for record in records:
        key = record['key']
        values = record['values']
        combs = filter_combinations(get_combinations(values, n))
        for comb in combs:
            occurrences = counts.get(comb, [])
            occurrences.append(key)
            counts[comb] = occurrences
    return counts

def get_combinations(values, n):
    return itertools.combinations(values, n)

def prune_combinations(combs, prunes):
    if not prunes:
        return combs
    else:
        return {x for x in combs if not is_pruned(x, prunes)}

def limit_combinations(combs, count):
    return itertools.islice(combs, count)

def is_include(x, includes):
    return any(set(val).issubset(x['values']) for val in includes)

def is_pruned(x, prunes):
    n = len(x) - 1
    if not prunes:
        return False
    else:
        return any(x in prunes for x in itertools.combinations(x, n))

def main():
    args = sys.argv
    arg_n = int(args[1]) if len(args) > 1 else 2
    arg_threshold = int(args[2]) if len(args) > 2 else 3
    arg_comb_count = int(args[3]) if len(args) > 3 else 10

    log("parsing log...")
    history = list(parse_commit_files_log(sys.stdin))

    log("finding frequent combinations...")
    freqs = find_frequent_combinations(history, arg_n, arg_threshold, arg_comb_count)

    log("preparing result...")
    freqs_sorted = [(k, freqs[k]) for k in sorted(freqs, key=lambda x: len(freqs[x]), reverse=True)]

    for k in freqs_sorted:
        print("--------------------")
        print(str(len(k[1])) + " " + str(k[0]))
        for commit in k[1]:
            print(commit)

if __name__ == "__main__":
    main()
