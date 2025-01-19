import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementNotInteractableException, NoSuchElementException, TimeoutException, ElementClickInterceptedException
)

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get("https://www.redbus.in/online-booking/apsrtc/?utm_source=rtchometile")
driver.maximize_window()
time.sleep(3)

# Initialize lists to store routes and links
routes = []
links = []

# WebDriverWait instance
wait = WebDriverWait(driver, 10)

# Retrieve route links and texts across multiple pages
while True:
    # Scrape data from the current page
    elements = driver.find_elements(By.XPATH, "//a[@class='route']")
    links.extend([element.get_attribute("href") for element in elements if element.get_attribute("href")])
    routes.extend([element.text for element in elements if element.text])

    # Handle pagination
    try:
        # Get the active page number
        active_page_element = driver.find_element(By.XPATH, "//div[@class='DC_117_pageTabs DC_117_pageActive']")
        active_page_number = int(active_page_element.text)
        next_page_number = str(active_page_number + 1)

        # Locate the next page button
        next_page_button_xpath = f"//div[@class='DC_117_paginationTable']//div[text()='{next_page_number}']"
        next_page_button = wait.until(EC.presence_of_element_located((By.XPATH, next_page_button_xpath)))

        # Scroll into view and click the next page button
        driver.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
        time.sleep(1)  # Short delay for scroll action

        try:
            next_page_button.click()
        except ElementNotInteractableException:
            driver.execute_script("arguments[0].click();", next_page_button)

        print(f"Navigating to page {next_page_number}...")
        time.sleep(5)  # Wait for the next page content to load
    except (NoSuchElementException, TimeoutException):
        print("No more pages to paginate or pagination element not found.")
        break

# Now scrape data for each route link
all_bus_data = []  # List to store data for all routes

for route, link in zip(routes, links):
    try:
        # Navigate to the route link
        driver.get(link)
        print(f"Scraping buses for route: {route} | Link: {link}")

        try:
            # Locate the "View Buses" button for RSRTC
            view_buses_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'button') and contains(text(), 'View Buses')]"))
            )

            # Check if the button is visible
            if view_buses_button.is_displayed():
                # Scroll the button into view if necessary
                driver.execute_script("arguments[0].scrollIntoView(true);", view_buses_button)
                time.sleep(1)  # Allow time for scrolling
                try:

                    view_buses_button.click()
                except ElementClickInterceptedException:

                    driver.execute_script("arguments[0].click();", view_buses_button)
                time.sleep(3)  # Allow time for buses to load
                print(f"'View Buses' clicked for government buses on route: {route}")
            else:
                print(f"'View Buses' button found but not visible for route: {route}")
        except TimeoutException:
            print(f"No 'View Buses' button found for route: {route}")
        except Exception as e:
            print(f"Error interacting with 'View Buses' button: {e}")

        # Scroll to load all buses
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for more buses to load


            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Scrape bus data
        bus_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'bus-item')]")
        for bus_element in bus_elements:
            bus_name = bus_element.find_element(By.XPATH, ".//div[contains(@class, 'travels lh-24 f-bold d-color')]").text
            departure_time = bus_element.find_element(By.XPATH, ".//div[contains(@class, 'dp-time f-19 d-color f-bold')]").text
            price = bus_element.find_element(By.XPATH, ".//div[contains(@class, 'fare d-block')]").text
            duration = bus_element.find_element(By.XPATH, ".//div[contains(@class, 'dur l-color lh-24')]").text
            reaching_time = bus_element.find_element(By.XPATH, ".//div[contains(@class, 'bp-time f-19 d-color disp-Inline')]").text
            bus_type = bus_element.find_element(By.XPATH, ".//div[contains(@class, 'bus-type f-12 m-top-16 l-color evBus')]").text
            try:
                star_rating = bus_element.find_element(By.XPATH, ".//div[contains(@class, 'rating-sec lh-24')]").text
            except NoSuchElementException:
                print(f"Star rating not found for route: {route}")
                star_rating = "N/A"
            seat_avail = bus_element.find_element(By.XPATH, ".//div[contains(@class, 'column-eight w-15 fl')]").text
            # Save data
            all_bus_data.append({
                "Bus_Routes_Name": route,
                "Bus_Routes_links": link,
                "Bus_name": bus_name,
                "Bus_type": bus_type,
                "Departing_time": departure_time,
                "Duration": duration,
                "Reaching_time": reaching_time,
                "Star_rating": star_rating,
                "Price": price,
                "Seat_availability": seat_avail
            })

        # Go back to the main page (if needed, reload the main page URL)
        driver.back()
        time.sleep(5)  # Wait for the main page to load
    except Exception as e:
        print(f"Error scraping route {route}: {e}")

# Close the WebDriver
driver.quit()

# Convert the list of scraped data to a Pandas DataFrame
df = pd.DataFrame(all_bus_data)

# Save the DataFrame to a CSV file
csv_file = "AndhraPradesh_scraped_data.csv"
try:
    df.to_csv(csv_file, index=False, encoding="utf-8")
    print(f"Scraped data saved to {csv_file}")
except Exception as e:
    print(f"Error writing to CSV file: {e}")
