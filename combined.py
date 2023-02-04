#!/usr/bin/env python3

import argparse
import requests
import unicodedata
import json
from prettytable import PrettyTable

import logging

logger = logging.getLogger()
formatter = logging.Formatter("%(asctime)s: %(message)s")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s: %(message)s',
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", action='append')
    args = parser.parse_args()

    output = {}
    print(args.i)
    for filename in args.i:
        with open(filename, "r", encoding="utf-8") as fd:
            infile = json.load(fd)
            for k, v in infile.items():
                if output.get(k, None) is None:
                    output[k] = v
                else:
                    output[k]["count"] += v["count"]
                    if v["max_enrage"] > output[k]["max_enrage"]:
                        output[k]["max_enrage"] = v["max_enrage"]

    sorted_output = dict(
        sorted(
            output.items(), key=lambda x: (x[1]["count"]), reverse=True
        )
    )
    logger.info(f"Total Unique Players: {len(sorted_output)}")
    pt = PrettyTable(["Name", "Count", "Highest Enrage"])
    for k, v in sorted_output.items():
        pt.add_row([k, v["count"], v["max_enrage"]])
    print(pt)


if __name__ == '__main__':
    main()
