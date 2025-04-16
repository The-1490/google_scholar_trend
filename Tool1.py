#!python3
import argparse
import datetime
import re
import sys
import time
import os

import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup  # Import BeautifulSoup


def parse_args():
    parser = argparse.ArgumentParser(description="Scrape Google Scholar results for keyword trends.")
    parser.add_argument("keywords", type=str, nargs="+", help="Keywords to search")
    parser.add_argument("--since", type=int, default=2020, help="Starting year")
    parser.add_argument("--to", type=int, default=datetime.datetime.now().year, help="Ending year")
    parser.add_argument("--plot", action="store_true", help="Plot the results")
    parser.add_argument("--csv", type=str, default="Tungsten.csv", metavar="filename", help="Filename for CSV output")
    parser.add_argument("--output_dir", type=str, default="D:\\Server\\Scholar trends", help="Directory to save output files")
    parser.add_argument("--filter", type=str, default="AND", choices=["AND", "OR"], help="Filter type for multiple keywords (AND or OR)")
    return parser.parse_args()


def fetch_scholar_results(driver, keywords, year):
    """Fetches and parses Google Scholar results for a given year using BeautifulSoup.
    Also extracts author and publication year.
    """
    base_url = f"https://scholar.google.ca/scholar?q={keywords}&as_ylo={year}&as_yhi={year}"
    try:
        driver.get(base_url)
        # Wait for the results to load (adjust timeout and element as needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "gs_top"))  # Or a more specific result element
        )
        page_content = driver.page_source
        soup = BeautifulSoup(page_content, 'html.parser')  # Create BeautifulSoup object

        # Find the element containing the results count
        result_div = soup.find('div', {'id': 'gs_ab_md'})  # Adjust based on Google Scholar's HTML structure
        total_results = 0  # Initialize total_results
        if result_div:
            result_text = result_div.text
            reg = re.compile(r".*About ([\d,]+) results.*")
            match = reg.match(result_text)

            if match:
                total_results = int(match.group(1).replace(",", ""))
                print(f"{year}: {total_results} total results")
            else:
                print(f"Error parsing total results for {year}", file=sys.stderr)

        else:
            print(f"Could not find total results div for {year}", file=sys.stderr)

        # Extract author and publication year for each result
        results_data = []
        result_blocks = soup.find_all('div', class_='gs_r')  # Each result is in a gs_r div
        for block in result_blocks:
            author_year = ""
            author_year_span = block.find('div', class_='gs_a')  # gs_a contains author and year
            if author_year_span:
                author_year = author_year_span.text
            results_data.append(author_year)

        return total_results, results_data  # Return both total results and extracted data

    except Exception as e:
        print(f"Error fetching results for {year}: {e}", file=sys.stderr)
        return 0, []  # Return 0 and empty list in case of error
    finally:
        time.sleep(1)  # Reduced to 1 second as requested


def save_results_to_csv(output_dir, filename, years, results):
    """Saves the results to a CSV file."""
    filepath = os.path.join(output_dir, filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:  # Added encoding
            f.write("year,totalResults,authorYear\n")  # Header row
            for year, (total_results, results_data) in zip(years, results):
                for author_year in results_data:
                    f.write(f"{year},{total_results},\"{author_year}\"\n")  # Quote author/year
        print(f"Results saved to {filepath}")
    except Exception as e:
        print(f"Error saving to CSV: {e}", file=sys.stderr)


def plot_results(output_dir, keywords, years, results):
    """Plots the results and saves the plot to a file."""
    # The plotting part remains the same, but now it only plots total results
    total_results = [r[0] for r in results]  # Extract total results for plotting

    plt.figure(figsize=(10, 5), dpi=80)
    plt.style.use("grayscale")
    plt.grid(True, alpha=0.5)
    plt.plot(years, total_results, "X-", label="Total Results")  # Combined marker and line
    plt.title(f'Google Scholar Results for "{ " ".join(keywords) }" ({years[0]}-{years[-1]})')
    plt.xlabel("Year")
    plt.ylabel("Number of Results")
    plt.legend()  # Show the label
    plt.savefig(os.path.join(output_dir, f"trend_{'_'.join(keywords)}.png"), bbox_inches="tight")  # Use underscore in filename
    plt.show()


def write_search_info(filename, keywords, filter_type):
    """Writes the search keywords and filter type to a file."""
    filepath = filename
    try:
        with open(filepath, "w") as f:
            f.write(f"Keywords: {', '.join(keywords)}\n")
            f.write(f"Filter Type: {filter_type}\n")
        print(f"Search information written to {filepath}")
    except Exception as e:
        print(f"Error writing search information to {filepath}: {e}", file=sys.stderr)


if __name__ == "__main__":
    args = parse_args()
    keywords = args.keywords  # Keep keywords as a list
    filter_type = args.filter

    # Construct the search query based on the filter type
    if filter_type == "AND":
        search_query = "+".join(keywords)  # "AND" is the default behavior in Google Scholar
    else:  # filter_type == "OR"
        search_query = " OR ".join(keywords)

    years = range(args.since, args.to + 1)

    # Selenium setup
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    # Fetch results
    all_results = [fetch_scholar_results(driver, search_query, year) for year in years]  # Collect all results

    # Clean up Selenium
    driver.quit()

    # Save and plot results
    if args.csv:
        save_results_to_csv(args.output_dir, args.csv, years, all_results)  # Pass all_results
    if args.plot:
        plot_results(args.output_dir, keywords, years, all_results)  # Pass original keywords for title
    # Write search information to Cmd.txt
    write_search_info("Cmd.txt", keywords, filter_type)
