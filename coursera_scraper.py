
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv

def scrape_courses_by_keyword(keyword):
    """Scrapes Coursera courses for a given keyword using Selenium.

    Args:
        keyword (str): The keyword to search for.

    Returns:
        list: A list of dictionaries containing course data.
    """

    course_data = []
    url = f"https://www.coursera.org/search?query={keyword}"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Optional: run Chrome in headless mode
    driver = webdriver.Chrome(options=options, executable_path="/path/to/chromedriver")  # Adjust path

    driver.get(url)

    while True:
        try:
            # Click "See More" button using Selenium
            see_more_button = driver.find_element(By.CSS_SELECTOR, ".see-more-button")  # Adjust selector as needed
            see_more_button.click()
            time.sleep(2)  # Adjust wait time as needed
        except:
            # Button likely not found, break the loop
            break

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    all_course_data = []


    # Extract data from the initial page (adjust selectors based on Coursera's structure)
    courses = soup.find_all("div", class_="cds-ProductCard-content")
    for course in courses:
        title = course.find("h3", class_="cds-CommonCard-title").text.strip()
        link = "https://www.coursera.org" + course.find("a", class_="cds-119 cds-113 cds-115 cds-CommonCard-titleLink css-si869u cds-142")["href"]
        # ... extract other course information ...

        course_dict = {
            "title": title,
            "link": link,
            # Add additional key-value pairs for extracted course data
        }
        all_course_data.append(course_dict)

    driver.quit()  # Close the WebDriver after scraping

    return all_course_data

# Example usage
keyword = input("Enter a keyword to search for Coursera courses: ")
courses_data = scrape_courses_by_keyword(keyword)

# Process and store the scraped data (e.g., print or save to CSV)
# ... your code for processing data ...
print(f"Scraped {len(courses_data)} courses with keyword '{keyword}':")
for course in courses_data:
    print(f"\nTitle: {course['title']}")    
    print(f"Link: {course['link']}")
    

# Save all data to a CSV file
csv_file_path = f"coursera_courses_{keyword}.csv"

# Specify the CSV file headers based on the keys in the course_dict
csv_headers = ["title", "link"]

with open(csv_file_path, mode="w", encoding="utf-8", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)

    # Write headers to the CSV file
    writer.writeheader()

    # Write all course data to the CSV file
    writer.writerows(courses_data)

print(f"\nData saved to {csv_file_path} Scraped {len(courses_data)} courses with keyword '{keyword}'.")
