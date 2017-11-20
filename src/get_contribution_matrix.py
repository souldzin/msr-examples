""" get_contribution_matrix.py
"""
import csv
import sys
import xml.etree.ElementTree as ET

def getContributorNetwork(root):
    network = {}
    for item in root.find("channel").findall("item"):
        item_contributors = getContributorsForItem(item)
        network = addToNetwork(network, item_contributors)
    return network

def getContributorsForItem(item_node):
    assignee = item_node.find("assignee").attrib["username"]
    reporter = item_node.find("reporter").attrib["username"]
    comments_parent = item_node.find("comments")
    comments = comments_parent.findall("comment") if comments_parent else []
    commenters = {x.attrib["author"] for x in comments}

    contributors = {assignee, reporter} | commenters

    return [x for x in contributors if x and str(x) != "-1"]

def addToNetwork(network, items):
    for item in items:
        connections = network.get(item, {})
        for inner_item in items:
            connections[inner_item] = connections.get(inner_item, 0) + 1
        network[item] = connections
    return network

def printContributorNetwork(network):
    contributors = sorted(network.keys())
    fields = ["_"] + contributors
    writer = csv.DictWriter(sys.stdout, fieldnames=fields, lineterminator="\n")

    writer.writeheader()
    for contributor in contributors:
        record = network[contributor].copy()
        record["_"] = contributor
        record[contributor] = "-"
        writer.writerow(record)

def main():
    args = sys.argv
    arg_file = args[1] if len(args) > 1 else False

    if not arg_file:
        sys.exit("argument is required (expected XML file).")

    tree = ET.parse(arg_file)
    root = tree.getroot()
    network = getContributorNetwork(root)
    printContributorNetwork(network)

if __name__ == "__main__":
    main()
