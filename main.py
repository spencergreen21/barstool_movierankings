from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from bs4 import BeautifulSoup


# function to scroll down the page
def scroll_down(driver):
    last_height = driver.execute_script("return window.scrollY")

    # Scroll down to the bottom of the page
    while True:
        actions = ActionChains(driver)
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(1)

        current_height = driver.execute_script("return window.scrollY")

        if current_height == last_height:
            break

        last_height = current_height

movies = []

# Initialize the WebDriver
driver = webdriver.Edge()

# Navigate to the website
driver.get("https://www.movierankings.net/")

top_100_button = driver.find_element(By.XPATH, '/html/body/div/div/div[9]/div[1]/h3[2]')
time.sleep(2)
top_100_button.click()

time.sleep(5)

# Initial scroll to load more content
scroll_down(driver)

# Keep scrolling until there is no more content to load
while True:
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Scroll down
    scroll_down(driver)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break

soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find all elements with the class 'movie-title'
movie_titles = soup.find_all(class_='movie-title')

for title in movie_titles:
    movie_name = title.text
    movies.append(movie_name)
    print(movie_name)

for _ in range(5):
    # Keep scrolling until there is no more content to load
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")

        # Scroll down
        scroll_down(driver)

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Find all elements with the class 'movie-title'
            movie_titles = soup.find_all(class_='movie-title')

            # Iterate over each movie title element and extract the movie name
            for title in movie_titles:
                movie_name = title.text
                movies.append(movie_name)
                print(movie_name)

            # Break out of the scrolling loop
            break

    try:
        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Next"]')))
        next_button.click()
        time.sleep(5)
    except NoSuchElementException:
        print("Next button not found.")
        break

print(movies)

# Close the webdriver
driver.quit()




