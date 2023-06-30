from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from env import USER_EMAIL, USER_PASSWORD
from time import sleep


driver = webdriver.Chrome()
driver.get("https://qbl.sys.kth.se/authoring/project/dd1396__parallel_and_concurren/curriculum/unit_zmuf3")

# close the cookie banner
close_cookies_btn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/div/div[1]/button"))
)
close_cookies_btn.click() 

# # login
email_element = driver.find_element(By.XPATH, "/html/body/div[2]/main/div[2]/form/div[1]/input")
email_element.send_keys(USER_EMAIL)

password_element = driver.find_element(By.XPATH, "/html/body/div[2]/main/div[2]/form/div[2]/input")
password_element.send_keys(USER_PASSWORD)

submit_btn = driver.find_element(By.XPATH, "/html/body/div[2]/main/div[2]/form/button")
submit_btn.click()

sleep(2)

# edit page
wait = WebDriverWait(driver, 10)

edit_btn = wait.until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Edit Page"))
)
edit_btn.click()

# add multiple choice question
sleep(5)

add_element_menu_btns = driver.find_elements(By.CSS_SELECTOR, ".addResourceContent_W\\+36phqP")
add_element_menu_btns[-1].click()

sleep(1)

options_bounding_box = wait.until(
    EC.visibility_of_element_located((By.CLASS_NAME, 'activities'))
)
add_MCQ_btn = options_bounding_box.find_elements(By.CLASS_NAME, 'resource-choice')[1]
add_MCQ_btn.click()

sleep(1)

# fill in question

sleep(1)

question_block = driver.find_elements(By.CSS_SELECTOR, ".resource-block-editor")[-1]

# add third answer option
question_block.find_element(By.CSS_SELECTOR, ".addChoiceContainer_nMRQoZI6").find_element(By.CSS_SELECTOR, "button").click()

slate_editors = question_block.find_elements(By.CSS_SELECTOR, ".slate-editor")
question_input = slate_editors[0]
alt1_input = slate_editors[1]
alt2_input = slate_editors[2]
alt3_input = slate_editors[3]

question_input.clear()
alt1_input.clear()
alt2_input.clear()
alt3_input.clear()

question_input.send_keys("What is the answer to life, the universe and everything?")
alt1_input.send_keys("42")
alt2_input.send_keys("43")
alt3_input.send_keys("44")





sleep(8)

# new_page = driver.find_element(By.CSS_SELECTOR, "button:contains('Practice Page')")
# print(new_page.text)

# new_page.click()


