from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import json


with open("./settings.json", "r") as f:
    settings = json.loads(f.read())
    username = settings["username"]
    password = settings["password"]
    term = settings["term"]
    headless = settings["headless"]
    course_codes_to_register_for = settings["course_codes_to_register_for"]


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
if headless:
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options)


# Go to GriffinGate
griffingate_url = "https://griffingate.setonhill.edu"
driver.get(griffingate_url)
print(f'went to griffin gate at {griffingate_url}')

username_input = driver.find_element(By.ID, "userName")
print(f'found the user name input box')
username_input.clear()
username_input.send_keys(username)
print(f'typed in username "{username}"')

continue_button = driver.find_element(By.ID, "siteNavBar_welcomeBackBarLoggedOut_JicsLoginRedirectContinue")
print(f'found the continue button')
continue_button.click()
print(f'clicked the continue button, expected to be redirected to SSO')



# Login in to SSO
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "username"))
)
username_input = driver.find_element(By.ID, "username")
print(f'found the username input')
username_input.clear()
username_input.send_keys(username)
print(f'typed in username "{username}"')

password_input = driver.find_element(By.ID, "password")
print(f'found the password input')
password_input.clear()
password_input.send_keys(password)
print(f'typed in password')

login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
print(f'found the login button')
login_button.click()
print('clicked login button')



# click the student link
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/ICS/Student/']"))
)
student_button = driver.find_element(By.CSS_SELECTOR, "a[href='/ICS/Student/']")
print(f'found student button')
student_button.click()
print(f'clicked student button')


# click the course registration and advising link
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/ICS/Student/Course_Registration_and_Advising.jnz']"))
)
course_registration_and_advising_link = driver.find_element(By.CSS_SELECTOR, "a[href='/ICS/Student/Course_Registration_and_Advising.jnz']")
print(f'found the course registration and advising link')
course_registration_and_advising_link.click()
print(f'clicked the course registration and advising link')


# click the add drop courses link
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/ICS/Student/Course_Registration_and_Advising.jnz?portlet=Course_Schedules&screen=Add+Drop+Courses&screenType=next']"))
)
add_drop_courses_link = driver.find_element(By.CSS_SELECTOR, "a[href='/ICS/Student/Course_Registration_and_Advising.jnz?portlet=Course_Schedules&screen=Add+Drop+Courses&screenType=next']")
print(f'found the add drop courses link')
add_drop_courses_link.click()
print(f'clicked the add drop courses link')


# select the right term, the term we pick will be populated throughout the session, so we are only selecting it once here.
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "pg0_V_ddlTerm"))
)
term_dropdown = driver.find_element(By.ID, "pg0_V_ddlTerm")
print(f'found the term dropdown')
term_dropdown_select = Select(term_dropdown)
term_dropdown_select.select_by_visible_text(term)
print(f'selected "{term}" in the term dropdown')
print(f'waiting for the page to reload')
WebDriverWait(driver, 60).until(EC.staleness_of(term_dropdown))

# capture the url
course_search_url = driver.current_url

for course_code in course_codes_to_register_for:

    # select "Exact Match" on the course search
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "pg0_V_tabSearch_ddlCourseRestrictor"))
    )
    course_code_search_type_dropdown = driver.find_element(By.ID, "pg0_V_tabSearch_ddlCourseRestrictor")
    print(f'found the course code search type dropdown')
    course_code_search_type_dropdown_select = Select(course_code_search_type_dropdown)
    course_code_search_type_dropdown_select.select_by_visible_text('Exact Match')
    print(f'selected "Exact Match" in the course code search type dropdown')

    # enter the course code
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "pg0_V_tabSearch_txtCourseRestrictor"))
    )
    course_code_input = driver.find_element(By.ID, "pg0_V_tabSearch_txtCourseRestrictor")
    print(f'found the course code input')
    course_code_input.clear()
    course_code_input.send_keys(course_code)
    print(f'entered "{course_code}" in the course code input')

    # click the search button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "pg0_V_tabSearch_btnSearch"))
    )
    search_button = driver.find_element(By.ID, "pg0_V_tabSearch_btnSearch")
    print(f'found the search button')
    search_button.click()
    print(f'clicked the search button')

    # click the desired courses' link
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, course_code))
    )
    course_link = driver.find_element(By.PARTIAL_LINK_TEXT, course_code)
    print(f'found link for "{course_code}"')
    course_link.click()
    print(f'clicked link for "{course_code}"')

    # # click the desired courses' link
    # WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.ID, "pg0_V_lnkAddCourse"))
    # )
    # add_course_link = driver.find_element(By.ID, "pg0_V_lnkAddCourse")
    # print(f'found the add course link')
    # add_course_link.click()
    # print(f'clicked the add course link')

    driver.get(course_search_url)
    print(f'going back to course search')








# WebDriverWait(driver, 10000000000000).until(
#     EC.element_to_be_clickable((By.ID, "thing-that-does-not-exist"))
# )