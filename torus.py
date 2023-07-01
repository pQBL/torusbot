from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from env import USER_EMAIL, USER_PASSWORD, CURRICULUM_URL
from page_definition import Page_definition
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException


def wait_for_element(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))


def wait_for_elements(driver, by, value, count, timeout=10):
    return WebDriverWait(driver, timeout).until(lambda d: len(d.find_elements(by, value)) >= count)


def wait_for_clickable_element(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))


def click_element(driver, locator, attempts=1):
    for _ in range(attempts):
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator)).click()
            break
        except StaleElementReferenceException or ElementClickInterceptedException:
            continue


def login(driver, email, password):
    email_element_locator = (By.XPATH, "/html/body/div[2]/main/div[2]/form/div[1]/input")
    password_element_locator = (By.XPATH, "/html/body/div[2]/main/div[2]/form/div[2]/input")
    submit_btn_locator = (By.XPATH, "/html/body/div[2]/main/div[2]/form/button")

    wait_for_element(driver, email_element_locator).send_keys(email)
    wait_for_element(driver, password_element_locator).send_keys(password)
    click_element(driver, submit_btn_locator)


def close_cookie_banner(driver):
    close_cookies_btn_locator = (By.XPATH, "/html/body/div[4]/div/div/div/div[1]/button")
    click_element(driver, close_cookies_btn_locator)


def open_unit(driver, unit_name):
    unit_locator = (By.PARTIAL_LINK_TEXT, unit_name)
    click_element(driver, unit_locator, 3)


def open_page(driver):
    edit_btn_locator = (By.LINK_TEXT, "Edit Page")
    click_element(driver, edit_btn_locator, 3)


def add_multiple_choice_question(driver, question):
    prev_num_resource_blocks = len(driver.find_elements(By.CLASS_NAME, "resource-block-editor"))
    add_new_multiple_choice_question(driver)
    wait_for_elements(driver, By.CLASS_NAME, "resource-block-editor", prev_num_resource_blocks + 1)
    question_block = driver.find_elements(By.CLASS_NAME, "resource-block-editor")[-1]
    fill_in_question(question_block, question)
    fill_in_answer_options(driver, question_block, question)
    question_block.find_element(By.LINK_TEXT, "ANSWER KEY").click()
    fill_in_feedback(question_block, question)


def add_new_multiple_choice_question(driver):
    wait_for_elements(driver, By.CLASS_NAME, "addResourceContent_W\\+36phqP", 2)
    add_element_menu_btns = driver.find_elements(By.CSS_SELECTOR, ".addResourceContent_W\\+36phqP")
    add_element_menu_btns[-1].click()
    options_bounding_box = wait_for_element(driver, (By.CLASS_NAME, 'activities'))
    add_MCQ_btn = options_bounding_box.find_elements(By.CLASS_NAME, 'resource-choice')[1]
    add_MCQ_btn.click()


def fill_in_question(question_block, question):
    question_block.find_elements(By.CLASS_NAME, "slate-editor")[0].send_keys(question.question_text)


def fill_in_answer_options(driver, question_block, question):
    # add third answer option
    wait_for_element(driver, (By.CSS_SELECTOR, ".addChoiceContainer_nMRQoZI6"))
    question_block.find_element(By.CSS_SELECTOR, ".addChoiceContainer_nMRQoZI6").find_element(By.CSS_SELECTOR, "button").click()
    answer_option_slate_editors = question_block.find_elements(By.CLASS_NAME, "slate-editor")[1:4]
    for i in range(3):
        answer_option_slate_editors[i].send_keys(Keys.BACKSPACE * 8 + question.answer_options[i])


def fill_in_feedback(question_block, question):
    mark_correct_answer_radio_btns = question_block.find_elements(By.CSS_SELECTOR, ".oli-radio.flex-shrink-0")[3:6] # first three are on the question page
    mark_correct_answer_radio_btns[question.correct_option].click()
    correct_ans_feedback = question_block.find_element(By.CLASS_NAME, "card").find_element(By.CLASS_NAME, "slate-editor")
    correct_ans_feedback.send_keys(Keys.BACKSPACE * 8 + question.feedback[question.correct_option])

    add_targeted_feedback_btn = question_block.find_elements(By.CSS_SELECTOR, ".btn.btn-link.pl-0")[-1]
    add_targeted_feedback_btn.click()
    add_targeted_feedback_btn.click()
    targeted_feedback_cards = question_block.find_elements(By.CLASS_NAME, "card")[2:4]

    non_correct_options = [i for i in range(3) if i != question.correct_option]
    for option_index, targeted_feedback_card in zip(non_correct_options, targeted_feedback_cards):
        select_corresponding_answer_btns = targeted_feedback_card.find_elements(By.CSS_SELECTOR, ".oli-radio.flex-shrink-0")
        select_corresponding_answer_btns[option_index].click()
        targeted_feedback_card.find_element(By.CLASS_NAME, "slate-editor").send_keys(question.feedback[option_index])


def main():
    page_definition = Page_definition.from_file('input.txt')

    driver = webdriver.Chrome()
    driver.get(CURRICULUM_URL)

    close_cookie_banner(driver)
    login(driver, USER_EMAIL, USER_PASSWORD)
    
    open_unit(driver, page_definition.unit)

    open_page(driver)

    for question in page_definition.questions[:2]:
        add_multiple_choice_question(driver, question)

    sleep(200)


if __name__ == "__main__":
    main()
