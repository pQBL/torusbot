from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from env import USER_EMAIL, USER_PASSWORD
from time import sleep
from question import Question


example_question = """When is it more advantageous to use pointer receivers over value receivers in Go?

    A) When the method needs to modify the receiver value or when the receiver is a large struct.
    - Correct! Using pointer receivers can be more efficient when the receiver is a large struct because it avoids copying the value. Also, if the method needs to modify the receiver value, a pointer receiver is required.

    B) It is always better to use value receivers in Go.
    - Incorrect! This is a misconception. While value receivers can be easier to understand and use, there are situations where pointer receivers are more efficient or necessary, such as when the method needs to modify the receiver value or when the receiver is a large struct.

    C) It is always better to use pointer receivers in Go.
    - Incorrect! This is a misconception. The choice between value receivers and pointer receivers depends on the specific requirements and constraints of the situation. For example, value receivers are typically used when the method does not need to modify the receiver and the receiver is a small struct.
"""
question = Question.from_string(example_question)


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

# fill in question

sleep(1)

question_block = driver.find_elements(By.CSS_SELECTOR, ".resource-block-editor")[-1]

# add third answer option
question_block.find_element(By.CSS_SELECTOR, ".addChoiceContainer_nMRQoZI6").find_element(By.CSS_SELECTOR, "button").click()

slate_editors = question_block.find_elements(By.CLASS_NAME, "slate-editor")
question_input = slate_editors[0]
alt1_input = slate_editors[1]
alt2_input = slate_editors[2]
alt3_input = slate_editors[3]

question_input.send_keys(question.question_text)
alt1_input.send_keys(Keys.BACKSPACE * 8 + question.answer_options[0])
alt2_input.send_keys(Keys.BACKSPACE * 8 + question.answer_options[1])
alt3_input.send_keys(question.answer_options[2])

sleep(3)

# add answer feedback

question_block.find_element(By.LINK_TEXT, "ANSWER KEY").click()

sleep(5)

# click on add targeted feedback twice

question_block.find_elements(By.CSS_SELECTOR, ".btn.btn-link.pl-0")[-1].click()
question_block.find_elements(By.CSS_SELECTOR, ".btn.btn-link.pl-0")[-1].click()

# select correct answer
driver.execute_script("arguments[0].scrollIntoView();", question_block)
correct_ans_radio_btns = question_block.find_elements(By.CSS_SELECTOR, ".oli-radio.flex-shrink-0")[3:6] # first three are on the question page
correct_ans_radio_btns[question.correct_option].click()
sleep(1)

div_cards = question_block.find_elements(By.CLASS_NAME, "card")
# ignore div_cards[1] (wrong answer feedback) because it's not visible when using the targeted feedback
correct_ans_feedback_div = div_cards[0]
targeted_feedback_1_div = div_cards[2]
targeted_feedback_2_div = div_cards[3]

correct_ans_feedback_div.find_element(By.CLASS_NAME, "slate-editor").send_keys(
    Keys.BACKSPACE * 8 + question.feedback[question.correct_option]
)

non_correct_options = [i for i in range(3) if i != question.correct_option]
select_corresponding_answer_btns = targeted_feedback_1_div.find_elements(By.CSS_SELECTOR, ".oli-radio.flex-shrink-0")
select_corresponding_answer_btns[non_correct_options[0]].click()
targeted_feedback_1_div.find_element(By.CLASS_NAME, "slate-editor").send_keys(question.feedback[non_correct_options[0]])

select_corresponding_answer_btns = targeted_feedback_2_div.find_elements(By.CSS_SELECTOR, ".oli-radio.flex-shrink-0")
select_corresponding_answer_btns[non_correct_options[1]].click()
targeted_feedback_2_div.find_element(By.CLASS_NAME, "slate-editor").send_keys(question.feedback[non_correct_options[1]])

sleep(200)

# new_page = driver.find_element(By.CSS_SELECTOR, "button:contains('Practice Page')")
# print(new_page.text)

# new_page.click()


