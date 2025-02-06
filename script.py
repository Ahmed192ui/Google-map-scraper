from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import sys
import pandas as pd

# Configure default encoding for printing
sys.stdout.reconfigure(encoding='utf-8')

# Set up the browser
driver = webdriver.Chrome()  # Ensure chromedriver is installed and in PATH
driver.maximize_window()

# Navigate to Google Maps
driver.get("https://www.google.com/maps/search/library+in+London,+UK/@51.5148452,-0.2750944,10z/data=!4m2!2m1!6e2?hl=en")

# Wait for the page to load
time.sleep(3)

# Scroll multiple times to load more results
scroll_pause_time = 3
for _ in range(20):  # Adjust the range for more scrolling
    driver.execute_script("document.querySelector('div[role=\"feed\"]').scrollBy(0, 1000);")
    time.sleep(scroll_pause_time)

# Collect data
libraries = []
results = driver.find_elements(By.XPATH, '//a[contains(@href, "https://www.google.com/maps/place")]')

for result in results:
    try:
        # Scroll the element into view before clicking
        driver.execute_script("arguments[0].scrollIntoView();", result)
        
        # Wait until the element is clickable
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(result))
        
        # Click on the result
        ActionChains(driver).move_to_element(result).click().perform()
        time.sleep(5)

        # Extract data
        name = driver.find_element(By.CSS_SELECTOR, 'h1.DUwDvf.lfPIob').text
        address = driver.find_element(By.XPATH, '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]').text
        try:
            website = driver.find_element(By.XPATH, '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]').text
        except:
            website = "N/A"
        try:
            phone = driver.find_element(By.XPATH, '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]').text
        except:
            phone = "N/A"

        try:
            rating_count = driver.find_element(By.CSS_SELECTOR, 'div.LBgpqf > div > div.fontBodyMedium.dmRWX > div.F7nice > span:nth-child(2) > span > span').text
            rating_count = re.sub(r'\D', '', rating_count)
        except:
            rating_count = "N/A"
        
        try:
            rating = driver.find_element(By.CSS_SELECTOR, 'div.fontBodyMedium.dmRWX > div.F7nice > span:nth-child(1) > span:nth-child(1)').text
        except:
            rating = "N/A"

        # Store data
        libraries.append({
            "Name": name,
            "Address": address,
            "Website": website,
            "Phone": phone,
            "Rating": rating,
            "Rating Count": rating_count
        })

    except Exception as e:
        print(f"Error fetching details: {e}")

# Save data to CSV file
df = pd.DataFrame(libraries)
df.to_csv('libraries_data.csv', index=False, encoding='utf-8')

# Print data
for library in libraries:
    print(library)

# Close the browser
driver.quit()
