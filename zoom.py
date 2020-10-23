'''

1. Takes in command for class name
2. Opens preset link for canvas
3. Clicks "Courses" tab in menu: can find by div ID
4. Click the class based on class name provided
5. Click on the zoom tab
6. Returns list of zoom links
7. Clicks on zoom link specified to open zoom call
8. Optional gives link to manually input

'''

from selenium import webdriver
import sys
import time
from selenium.webdriver.common.keys import Keys

link = "https://canvas.calpoly.edu/courses"
browserPath = "./geckodriver.exe"
defaultProfile = "./profile"

def valid_command(args):
    command = args[1]
    if command != 'open' or command != 'link':
        print("Error: python zoom.py (open/link) classname")
        return False
    return True

def open_link():
    profile = webdriver.FirefoxProfile(defaultProfile)
    driver = webdriver.Firefox(profile)
    driver.get(link)
    return driver

def login(driver):
    username = driver.find_element_by_id("username")
    userKey = input("Enter your username: ")
    username.send_keys(userKey)
    password = driver.find_element_by_id("password")
    userPass = input("Enter your password: ")
    password.send_keys(userPass)
    password.send_keys(Keys.ENTER)
    time.sleep(5)

def get_courses(driver):
    courseTable = driver.find_element_by_id("my_courses_table")
    tbody = courseTable.find_element_by_tag_name("tbody")
    tr = tbody.find_elements_by_tag_name("tr")
    d = {}
    for li in tr:
        td = li.find_element_by_class_name('course-list-course-title-column')
        className = td.find_elements_by_tag_name("a")
        if className:
            title = className[0].get_attribute('title')
            d[title] = className[0]

    print()
    for key in d.keys():
        print(key)
    return d

def choose_course(driver, d):
    while(True):
        choice = input("\nWhat class do you want to join? ")
        for key in d.keys():
            if choice.upper() in key:
                d[key].click()
                time.sleep(2)
                driver2 = open_zoom(driver)
                driver.quit()
                driver2.quit()
                exit()
        print("Class does not exist")
    
def open_zoom(driver):
    time.sleep(2)
    driver.find_element_by_link_text("Zoom").click()
    time.sleep(2)
    driver2 = driver
    driver.switch_to.frame("tool_content")
    driver.find_element_by_link_text("Join").click()
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(driver.current_url)
    time.sleep(5)
    return driver2

def main():
    driver = open_link()
    login(driver)
    classes = get_courses(driver)
    choose_course(driver, classes)

if __name__ == '__main__':
    main()

# handlers.json, key4.db




