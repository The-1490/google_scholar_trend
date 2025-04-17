# Google Scholar Trend Scraper

This script, `Tool1.py`, scrapes Google Scholar to analyze trends in research publications for specified keywords over a range of years. It uses Selenium to automate browser actions, BeautifulSoup4 to parse HTML content, and Matplotlib to generate plots.

## Usage

To use the script, you need to have Python 3 installed, along with the required libraries.

### Running the Script

Open a command-line interpreter (e.g., Command Prompt or PowerShell on Windows, or Terminal on macOS/Linux) and navigate to the directory where `Tool1.py` is located.

Execute the script using the following command:

```bash
python Tool1.py <keywords> [options]
```

## Arguments for Tool1.py

*   `keywords` (required): Keywords to search for trends. This is a positional argument, meaning it must be provided when running the script.
*   `--since` (optional): Starting year for the search (default: 2020).
*   `--to` (optional): Ending year for the search (default: current year).
*   `--plot` (optional): If present, the script will generate a plot of the results.
*   `--csv` (optional): Filename for the CSV output (default: "Tungsten.csv").
*   `--output_dir` (optional): Directory to save output files (default: "*//:path*").
*   `--filter` (optional): Filter type for multiple keywords ("AND" or "OR") (default: "AND").
