import pkg_resources
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def check_google_scholar_access():
    """
    Checks if Google Scholar is accessible via Selenium.
    """
    try:
        # Set up Chrome options for headless browsing
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (recommended for headless)

        # Initialize the Chrome driver
        driver = webdriver.Chrome(options=chrome_options)

        # Navigate to Google Scholar
        driver.get("https://scholar.google.com/")

        # Wait for the page to load (e.g., check for the search input element)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "gs_hdr_tsi"))  # Google Scholar search input element
        )

        print("Google Scholar is accessible via Selenium.")

    except Exception as e:
        print(f"Google Scholar is not accessible via Selenium. Error: {e}")

    finally:
        # Close the browser
        if 'driver' in locals():
            driver.quit()

def check_scholar_parsing(keyword="Tungsten"):
    """
    Checks if Google Scholar titles can be parsed using Selenium and BeautifulSoup.
    """
    try:
        # Set up Chrome options for headless browsing
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (recommended for headless)

        # Initialize the Chrome driver
        driver = webdriver.Chrome(options=chrome_options)

        # Navigate to Google Scholar with the keyword
        search_url = f"https://scholar.google.com/scholar?q={keyword}"
        driver.get(search_url)

        # Wait for the page to load and the results to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "gs_res_ccl_mid"))  # Common container for search results
        )

        # Get the page source and create a BeautifulSoup object
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Find all title elements (gs_rt)
        title_elements = soup.find_all('h3', class_='gs_rt')

        if title_elements:
            print(f"Found {len(title_elements)} title elements.")
            for i, title_element in enumerate(title_elements):
                title_text = title_element.get_text()
                print(f"Title {i+1}: {title_text}")
        else:
            print("No title elements found with class 'gs_rt'.")

        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        # Close the browser
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    check_scholar_parsing()