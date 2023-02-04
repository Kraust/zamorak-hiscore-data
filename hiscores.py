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
    parser.add_argument("-o", default=None)
    parser.add_argument("-min", default=0, type=int)
    parser.add_argument("-size", default=1, type=int)
    args = parser.parse_args()

    output = {}
    size = 15
    page = 0
    entries = 0
    done = False
    logger.info(f"Fetching Zamorak Stats for Group Size = {args.size}")
    while True:
        res = requests.get(
            f"https://secure.runescape.com/m=group_hiscores//v1//groups?groupSize={args.size}&size={size}&bossId=1&page={page}")
        try:
            data = res.json()
        except requests.JSONDecodeError:
            logger.info(f"Failed fetching page {page}")
            continue
        for content in data["content"]:
            if content["enrage"] < args.min:
                done = True
                break
            entries += 1
            for member in content["members"]:
                name = unicodedata.normalize('NFKD', member["name"])
                if output.get(name, None) is None:
                    output[name] = {
                        "max_enrage": content["enrage"],
                        "count": 1,
                    }
                else:
                    output[name]["count"] += 1
        logger.info(f"Finished fetching page {page}")
        page += 1
        if done or data["last"]:
            break
    sorted_output = dict(
        sorted(
            output.items(), key=lambda x: (x[1]["count"]), reverse=True
        )
    )
    logger.info(f"Total Teams: {entries}")
    logger.info(f"Total Unique Players: {len(sorted_output)}")
    pt = PrettyTable(["Name", "Count", "Highest Enrage"])
    for k, v in sorted_output.items():
        pt.add_row([k, v["count"], v["max_enrage"]])
    print(pt)

    if args.o:
        output = json.dumps(sorted_output)
        with open(args.o, "w", encoding="utf-8") as fd:
            fd.write(output)


if __name__ == '__main__':
    main()
