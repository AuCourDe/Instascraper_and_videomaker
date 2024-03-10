#Import dependencies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from random import randint   
import requests
from bs4 import BeautifulSoup
import re
import config
import json
import os
from urllib.parse import urlparse
import pyautogui
import csv


instascraper_folder = "C:/Projects/Instascraper/"
path_to_folder = os.path.join(instascraper_folder, "cookies.png")
print(path_to_folder)


#set language to english
option = webdriver.ChromeOptions()
option.add_argument("--accept-lang=en")
# option.add_argument("--start-maximized")
option.add_argument('disable_infobars')

#specify the path to chromedriver.exe (download and save on your computer)
driver = webdriver.Chrome(options=option)

#open the webpage
driver.get("https://www.instagram.com/")
time.sleep(randint(2,4))
accept_cookies= driver.find_element(By.CSS_SELECTOR, "button._a9--._ap36._a9_0").click()
time.sleep(randint(2,4))
#target username
username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
#enter username and password
username.clear()
username.send_keys(config.username)
time.sleep(randint(2,4))
password.clear()
password.send_keys(config.password)
time.sleep(randint(2,4))
#target the login button and click it
button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

# Wait up to 10 seconds for the search button to be clickable on the web page
search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg[aria-label="Search"]')))
time.sleep(randint(2,4))
# Click the search button once it becomes clickable
search_button.click()
time.sleep(randint(1,3))
#target the search input field
searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
searchbox.clear()
time.sleep(randint(1,3))
#search for the @handle or keyword
keyword = config.keyword
searchbox.send_keys(keyword)
time.sleep(randint(1,3))
# Check if the keyword starts with "@"
if keyword.startswith("@"):
    # Remove the "@" symbol
    keyword = keyword[1:]

# Find the first element with the specified XPath that matches the keyword    
first_result = driver.find_element(By.XPATH, f'//span[text()="{keyword}"]')

# Click on the found element (assuming it represents the desired search result)
first_result.click()
time.sleep(randint(3,5))

triger = "reels"
content_type_choose = config.content_type
if content_type_choose == triger :
    reels = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div[2]/a[2]/div/span')
    reels.click()
    time.sleep(5)


# Get the initial page height
initial_height = driver.execute_script("return document.documentElement.scrollHeight")

# Create a list to store htmls
soups = []
scroll_counter = 0
max_scroll_counter = config.max_scroll_counter

while True:
    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    driver.execute_script("return document.documentElement.scrollHeight")
   

    # Wait for a moment to allow new content to load (adjust as needed)
    time.sleep(randint(2,5))
    
    # Parse the HTML
    html = driver.page_source
    
    # Create a BeautifulSoup object from the scraped HTML
    soups.append(BeautifulSoup(html, 'html.parser'))

    # Get the current page height
    current_height = driver.execute_script("return document.documentElement.scrollHeight")
    pyautogui.moveTo(randint(15,1600),randint(15, 1000), randint(1,2))
    time.sleep(randint(2,5))

    if initial_height - current_height != 0:
            initial_height = current_height
    else:
        break  # Exit the loop when you can't scroll further

    if scroll_counter <= max_scroll_counter:
        scroll_counter += 1
        print(f"current scroll count is {scroll_counter} from {max_scroll_counter}")
    else:
        break  # Exit the loop when you can't scroll further


# List to store the post image URLs
post_urls = []

for soup in soups:
    # Find all image elements that match the specific class in the current soup
    elements = soup.find_all('a', class_='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd')

    # Extract the href attributes and filter URLs that start with "/p/" or "/reel/"
    post_urls.extend([element['href'] for element in elements if element['href'].startswith(("/p/", "/reel/"))])
    
# Convert the list to a set to remove duplicates
unique_post_urls = list(set(post_urls))

print(f"post before: {len(post_urls)},posts after:{len(unique_post_urls)}")

json_list = []

# Define the query parameters to add
query_parameters = "__a=1&__d=dis"
url_counter = 0
# go through all urls
for url in unique_post_urls:
    try:
        url_counter += 1
        print(f"procesing link: {url_counter} from total: {len(unique_post_urls)}")
        # Get the current URL of the page
        current_url = driver.current_url

        # Append the query parameters to the current URL
        modified_url = "https://www.instagram.com/" + url + "?" + query_parameters

        # Get URL
        driver.get(modified_url)

        # Wait for a moment to allow new content to load (adjust as needed)
        time.sleep(randint(2,5))

        # Find the <pre> tag containing the JSON data
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//pre'))
        )
        pre_tag = driver.find_element(By.XPATH, '//pre')

        # Extract the JSON data from the <pre> tag
        json_script = pre_tag.text

        # Parse the JSON data
        json_parsed = json.loads(json_script)

        # Add json to the list
        json_list.append(json_parsed)
    except (NoSuchElementException, TimeoutException, json.JSONDecodeError) as e:
        print(f"Error processing URL {url}: {e}")


# Lists to store URLs and corresponding dates
all_urls = []
all_dates = []

# Iterate through each JSON data in the list
for json_data in json_list:
    
    # Extract the list from the 'items' key
    item_list = json_data.get('items', [])
    
    # Iterate through each item in the 'items' list
    for item in item_list:
        
        # Extract the date the item was taken
        date_taken = item.get('taken_at')  # Move this line inside the loop

        # Check if 'carousel_media' is present
        carousel_media = item.get('carousel_media', [])
        
        # Iterate through each media in the 'carousel_media' list
        for media in carousel_media:
            
            # Extract the image URL from the media
            image_url = media.get('image_versions2', {}).get('candidates', [{}])[0].get('url')
            
            if image_url:
                # Add the image URL and corresponding date to the lists
                all_urls.append(image_url)
                all_dates.append(date_taken)
                print(f"carousel image added: {len(all_urls)}")
                # time.sleep(randint(1,3))
                
            # Extract the video URL from the media
            video_versions = media.get('video_versions', [])
            if video_versions:
                video_url = video_versions[0].get('url')
                if video_url:
                    
                    # Add the video URL and corresponding date to the lists
                    all_urls.append(video_url)
                    all_dates.append(date_taken)
                    print(f"carousel video added: {len(all_urls)}")
                    # time.sleep(randint(1,3))

        # Handle cases of unique image, instead of carousel
        image_url = item.get('image_versions2', {}).get('candidates', [{}])[0].get('url')
        if image_url:
            
            # Add the image URL and corresponding date to the lists
            all_urls.append(image_url)
            all_dates.append(date_taken)
            print(f"single image added: {len(all_urls)}")
            # time.sleep(randint(1,3))

        # Check if 'video_versions' key exists
        video_versions = item.get('video_versions', [])
        if video_versions:
            video_url = video_versions[0].get('url')
            if video_url:
                all_urls.append(video_url)
                all_dates.append(date_taken)
                print(f"video added: {len(all_urls)}")
                # time.sleep(randint(1,3))
                
# Print or use all collected URLs as needed
print(len(all_urls))
                

# Create a directory to store downloaded files
download_dir = keyword
os.makedirs(download_dir, exist_ok=True)

# Create subfolders for images and videos
image_dir = os.path.join("C://Projects//Instascraper", download_dir, "images")
video_dir = os.path.join("C://Projects//Instascraper",download_dir, "videos")
os.makedirs(image_dir, exist_ok=True)
os.makedirs(video_dir, exist_ok=True)

# Initialize counters for images and videos
image_counter = 1
video_counter = 1

# Iterate through URLs in the all_urls list and download media
for index, url in enumerate(all_urls, 0):
    response = requests.get(url, stream=True)

    # Extract file extension from the URL
    url_path = urlparse(url).path
    file_extension = os.path.splitext(url_path)[1]

    # Determine the file name based on the URL
    if file_extension.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.heic'}:
        file_name = f"{all_dates[index]}-img-{image_counter}.png"
        destination_folder = image_dir
        image_counter += 1
    elif file_extension.lower() in {'.mp4', '.avi', '.mkv', '.mov'}:
        file_name = f"{all_dates[index]}-vid-{video_counter}.mp4"
        destination_folder = video_dir
        video_counter += 1
    else:
        # Default to the main download directory for other file types
        file_name = f"{all_dates[index]}{file_extension}"
        destination_folder = download_dir

    # Save the file to the appropriate folder
    file_path = os.path.join(destination_folder, file_name)
    
    # Write the content of the response to the file
    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

    print(f"Downloaded: {file_path}")

# Print a message indicating the number of downloaded files and the download directory
print(f"Downloaded {len(all_urls)} files to {download_dir}")

