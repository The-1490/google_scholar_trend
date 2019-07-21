#!python3
import argparse
import datetime
import re
import sys

import matplotlib.pyplot as plt
import requests


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("keywords", type=str, help="Keywords to search", nargs="+")
    parser.add_argument("--since", type=int, help="Starting year", default=2000)
    parser.add_argument("--to", type=int, help="Ending year", default=datetime.datetime.now().year)
    parser.add_argument("--plot", help="Plot the result", action="store_true")
    parser.add_argument("--csv", type=str, help="Filename of CSV output result", metavar="filename", default=None)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    keywords = '+'.join(args.keywords)
    
    # Download results
    years = range(args.since, args.to+1)
    base_url = "https://scholar.google.ca/scholar?q=%s&as_ylo=%i&as_yhi=%i"
    pages = [requests.get(base_url % (keywords, i, i+1)) for i in years]
    
    # Parse html
    reg = re.compile(".*About ((?:\d|,)+) results.*")
    result_nbs = []
    for i, page in enumerate(pages):
        m = reg.match(str(page.content))
        if m is None:
            print("Error while parsing results", file=sys.stderr)
            if "Our systems have detected unusual traffic" in str(page.content):
                print("Google is throttling your IP, consider using a proxy/VPN", file=sys.stderr)
            exit(1)
        r = int(m.group(1).replace(',', ''))
        print("%i: %i" % (years[i], r))
        result_nbs.append(r)

    # Save results
    if args.csv is not None:
        with open(args.csv, "w") as f:
            print("year,numberOfResults", file=f)
            for i, r in enumerate(result_nbs):
                print("%i,%i" % (years[i], r), file=f)

    # Plot results
    if args.plot:
        fig = plt.figure(figsize=(10, 5), dpi=80)
        plt.style.use('grayscale')
        ax = fig.subplots()
        ax.grid(True, alpha=0.5)
        ax.plot(years, result_nbs, 'X', years, result_nbs)
        ax.set_title('Number of results with keywords "%s" using Google Scholar' % ' '.join(args.keywords))
        plt.xticks(years)
        plt.show()
