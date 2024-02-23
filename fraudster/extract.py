from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import time

def scrape_reviews(platform_url, product_name):
    # Set up headless browser options for Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Initialize the WebDriver (Ensure ChromeDriver is installed and in your PATH)
    driver = webdriver.Chrome(options=chrome_options)

    # Connect to or create a database
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    
    # Create a table for storing reviews if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS reviews
                      (product TEXT, review TEXT, rating TEXT, date TEXT)''')

    # Open the webpage
    driver.get(platform_url)

    # Wait for the reviews to load (adjust the timeout as necessary)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'review')) # Adjust the class name based on the actual website
    )

    # Logic to scrape reviews - this will vary depending on the website's structure
    # The findings may also be gibberish, still a wip..
    while True:
        # Find review elements
        review_elements = driver.find_elements(By.CLASS_NAME, 'review')

        for element in review_elements:
            # Extract review data
            review_text = element.find_element(By.CLASS_NAME, 'review-text').text
            review_rating = element.find_element(By.CLASS_NAME, 'rating').text
            review_date = element.find_element(By.CLASS_NAME, 'date').text

            # Insert the review into the database
            cursor.execute("INSERT INTO reviews VALUES (?, ?, ?, ?)",
                           (product_name, review_text, review_rating, review_date))

        # Check for and click the 'Next' or 'Load More' button, if it exists
        # This is also probably in need of debug.
        try:
            next_button = driver.find_element(By.CLASS_NAME, 'next-button') # Example
            next_button.click()
            time.sleep(2) # Wait for new content to load
        except Exception as e:
            print("No more pages or error encountered:", e)
            break

    # Commit changes and close the database connection
    conn.commit()
    conn.close()

    # Close the browser
    driver.quit()

# Example usage
scrape_reviews('https://example.com/product-reviews', 'ProductXYZ')

