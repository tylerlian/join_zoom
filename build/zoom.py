from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from sql import *
import sys
import time

# global variables
CANVAS_LINK = "https://canvas.calpoly.edu/courses"
BROWSER_PATH = "./geckodriver.exe"
DEFAULT_PROFILE = "./profile"
COMMANDS = ["python zoom.py -n/navi",
            "python zoom.py -h/help",
            "python zoom.py -i/id",
            "python zoom.py -j/join [classname/zoom_id]"
            "python zoom.py -g/get [classname/zoom_id]",
            "python zoom.py -a/add [classname] [zoom_id] [zoom_link]"
            "python zoom.py -d/del [classname/zoom_id]"
            "python zoom.py -s/show"]

# opens headless window with link provided
def open_link(link):
    options = webdriver.FirefoxOptions()
    options.headless = True
    profile = webdriver.FirefoxProfile(DEFAULT_PROFILE)
    driver = webdriver.Firefox(firefox_profile=profile, options=options)
    driver.get(link)
    return driver

# logins to the website by referencing the element id's: username & password
def login(driver):
    username = driver.find_element_by_id("username")
    userKey = input("Enter your username: ")
    username.clear()
    username.send_keys(userKey)
    password = driver.find_element_by_id("password")
    userPass = input("Enter your password: ")
    password.send_keys(userPass)
    password.send_keys(Keys.ENTER)
    time.sleep(4)

# returns the courses from the canvas course table
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
    for key in d.keys(): print(key)
    return d

# Goes to the Canvas course page and selects
def choose_course(driver, d):
    while(True):
        choice = input("\nWhat class do you want to join? ")
        for key in d.keys():
            if choice.upper() in key.upper():
                d[key].click()
                time.sleep(2)
                open_zoom(driver)
                driver.quit()
                sys.exit()
        print("Class does not exist.")
    
# Clicks the zoom tab on Canvas and joins the most recent link
def open_zoom(driver):
    time.sleep(2)
    driver.find_element_by_link_text("Zoom").click()
    time.sleep(2)
    driver.switch_to.frame("tool_content")
    try: driver.find_element_by_link_text("Join").click()
    except: print("No zoom link exists.")
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(driver.current_url)
    time.sleep(2)

# checks what kind of zoom link it is
def check_link(link):
    if link[1] == "j":
        link = "https://calpoly.zoom.us" + link
    elif link[1] == "l":
        link = "https://applications.zoom.us" + link
    return link

# joins the zoom link provided
def join_link(link):
    link = check_link(link)
    driver = open_link(link)
    driver.refresh()
    driver.quit()

def get_id(num):
    if num == 0: print("No classes available.")
    id = int(input("Input the SQL ID you want to join: "))
    while(1 > id or num-1 < id):
        print("That is an invalid ID.")
        id = int(input("Input the SQL ID you want to join: "))
    return str(id)

def prompt_login(driver):
    login(driver)
    while True:
        try:
            driver.find_element_by_id("username")
            login(driver)
        except: 
            input("\nPlease do your dual verification then press 'enter'.\n")
            break

def option_navigate():
    driver = open_link(CANVAS_LINK)
    prompt_login(driver)
    classes = get_courses(driver)
    choose_course(driver, classes)

def option_help():
    print("List of commands: ")
    for command in COMMANDS: print(command)

def option_id(cursor):
    num = show_table(cursor, 2)
    id = get_id(num)
    link = join_id(cursor, id)
    join_link(link)

def option_join(cursor):
    if sys.argv[2].isdigit():
        link = join_meeting(cursor, "'%" + sys.argv[2] + "%'")
        join_link(link) if link != None else print("Invalid meeting id.")
    else:
        link = join_classname(cursor, "'%" + sys.argv[2] + "%'")
        join_link(link) if link != None else print("Invalid classname.")

def option_get(cursor):
    if sys.argv[2].isdigit():
        classname = get_classname(cursor, "'%" + sys.argv[2] + "%'")
        print("Class name: " + classname) if classname != None else print("Invalid meeting id.")
    else:
        id = get_meetingid(cursor, "'%" + sys.argv[2] + "%'")
        print("Meeting ID: " + id) if id != None else print("Invalid class name.")

def no_access_sql():
    if len(sys.argv) == 1:
        print("Show all commands with 'python zoom.py -h/help'")
        exit()
    if sys.argv[1] in ["-n", "navi"]: # connects through navigating Canvas
        option_navigate()
        exit()
    elif sys.argv[1] in ["-h", "help"]: # the help command: gives users all usable commands.
        option_help()
        exit()

def access_sql(connection, cursor):
    if sys.argv[1] in ["-s", "show"]: # shows all data inside the sql table
        show_table(cursor, 4)
    elif sys.argv[1] in ["-a", "add"] and len(sys.argv) == 5: # inserts row into the sql table
        add_row(connection, cursor, sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] in ["-d", "del"] and len(sys.argv) == 3: # deletes a row in the sql table
        del_row(connection, cursor, sys.argv[2])
    elif sys.argv[1] in ["-i", "id"] and len(sys.argv) == 2: # connects to zoom call through id in sql table
        option_id(cursor)
    elif sys.argv[1] in ["-j", "join"] and len(sys.argv) == 3: # connects to zoom call through meeting id
        option_join(cursor)
    elif sys.argv[1] in ["-g", "get"] and len(sys.argv) == 3: # get meeting id or class name by reverse option
        option_get(cursor)
    else: # incorrect command from user
        print("Show all commands with 'python zoom.py -h/help'")

# decides what command to run check documentation to figure out what command does what
def main():
    no_access_sql() # commands that don't need sql table
    connection, cursor = open_connection() # opens connection to sql table
    access_sql(connection, cursor) # commands that do need the sql table
    close_connection(connection, cursor) # close connection to sql table

if __name__ == '__main__':
    main()

# handlers.json, key4.db