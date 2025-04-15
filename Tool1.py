#!python3
import argparse
import datetime
import re
import sys
import time
import random
import os

import matplotlib.pyplot as plt
import requests


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("keywords", type=str, help="Keywords to search", nargs="+")
    parser.add_argument("--since", type=int, help="Starting year", default=2020)
    parser.add_argument("--to", type=int, help="Ending year", default=datetime.datetime.now().year)
    parser.add_argument("--plot", help="Plot the result", action="store_true")
    parser.add_argument("--csv", type=str, help="Filename of CSV output result", metavar="filename", default="Tungsten.csv")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    keywords = "+".join(args.keywords)

    # Prepare http requests
    years = range(args.since, args.to + 1)
    base_url = "https://scholar.google.ca/scholar?q=%s&as_ylo=%i&as_yhi=%i"
    urls = [base_url % (keywords, i, i + 1) for i in years]
    headers = requests.utils.default_headers()
    headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        }
    )

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    ]
    headers.update({"User-Agent": random.choice(user_agents)})

    # Download webpages and parse html
    reg = re.compile(r".*About ([\d,]+) results.*")
    result_nbs = []
    for i, url in enumerate(urls):
        page = requests.get(url, headers=headers)
        page_content = page.text  # Get the content as text
        m = reg.match(page_content)
        if m is None:
            print(f"Error while parsing results for year {years[i]}", file=sys.stderr)
            if "Our systems have detected unusual traffic" in page_content:
                print("Google is throttling your IP, consider using a proxy/VPN", file=sys.stderr)
            result_nbs.append(0)  # Append 0 to continue the process
            continue
        r = int(m.group(1).replace(",", ""))
        print("%i: %i" % (years[i], r))
        result_nbs.append(r)
        time.sleep(random.uniform(0.5, 2))

    # Save results
    if args.csv is not None:
        output_path = os.path.join("D:\\Server\\Scholar trends", args.csv)  # saves to the specified directory
        with open(output_path, "w") as f:
            print("year,numberOfResults", file=f)
            for i, r in enumerate(result_nbs):
                print("%i,%i" % (years[i], r), file=f)

    # Plot results
    if args.plot:
        fig = plt.figure(figsize=(10, 5), dpi=80)
        plt.style.use("grayscale")
        ax = fig.subplots()
        ax.grid(True, alpha=0.5)
        ax.plot(years, result_nbs, "X", years, result_nbs)
        ax.set_title('Number of results with keywords "%s" using Google Scholar' % " ".join(args.keywords))
        # plt.xticks(years)
        plt.savefig(f"trend_{keywords}.png", bbox_inches="tight")
        plt.show()
