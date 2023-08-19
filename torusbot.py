import os
import sys
from page_definition import Page_definition
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.chrome.options import Options


TORUS_BOT_DELAY = 0.5
page_has_been_created = False


def wait_for_element(driver, locator, timeout=20):
    element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
    sleep(TORUS_BOT_DELAY)
    return element


def wait_for_elements(driver, locator, count, timeout=20):
    WebDriverWait(driver, timeout).until(lambda d: len(d.find_elements(*locator)) >= count)
    sleep(TORUS_BOT_DELAY)
    return driver.find_elements(*locator)


def wait_for_clickable_element(driver, locator, timeout=20):
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
    sleep(TORUS_BOT_DELAY)
    return element


def click_element(driver, locator, attempts=1, timeout=20):
    for _ in range(attempts):
        try:
            wait_for_clickable_element(driver, locator, timeout).click()
            break
        except StaleElementReferenceException or ElementClickInterceptedException:
            sleep(TORUS_BOT_DELAY)


def login(driver, email, password):
    email_element_locator = (By.ID, "user_email")
    password_element_locator = (By.ID, "user_password")
    submit_btn_locator = (By.CSS_SELECTOR, ".btn.btn-md.btn-primary.btn-block")

    wait_for_element(driver, email_element_locator).send_keys(email)
    wait_for_element(driver, password_element_locator).send_keys(password)
    click_element(driver, submit_btn_locator)


def close_cookie_banner(driver):
    cookie_consent_display_locator = (By.ID, "cookie_consent_display")
    close_cookies_btn_locator = (By.CSS_SELECTOR, 'button[aria-label="Close"]')
    click_element(wait_for_element(driver, cookie_consent_display_locator), close_cookies_btn_locator)


def open_unit(driver, unit_name):
    unit_locator = (By.PARTIAL_LINK_TEXT, unit_name)
    try:
        click_element(driver, unit_locator, 5)
    except TimeoutException:
        create_unit(driver, unit_name)
        click_element(driver, unit_locator, 5)


def create_unit(driver, unit_name):
    create_new_unit_locator = (By.CSS_SELECTOR, 'button[phx-value-type="Container"]')
    unit_drop_down_menu_locator = (By.CSS_SELECTOR, ".btn.dropdown-toggle")
    options_svg_locator = (By.CSS_SELECTOR, 'svg[data-icon="sliders"]')
    edit_title_locator = (By.ID, "revision-settings-form_title")
    unit_edit_form_locator = (By.ID, "revision-settings-form")
    save_btn_locator = (By.CSS_SELECTOR, ".btn.btn-primary")

    prev_num_units = len(driver.find_elements(*unit_drop_down_menu_locator))
    click_element(driver, create_new_unit_locator, 5)
    wait_for_elements(driver, unit_drop_down_menu_locator, prev_num_units + 1)
    driver.find_elements(*unit_drop_down_menu_locator)[-1].click()
    driver.find_elements(*options_svg_locator)[-1].find_element(By.XPATH, "..").click()
    wait_for_element(driver, edit_title_locator).send_keys(Keys.BACKSPACE * 8 + unit_name)
    driver.find_element(*unit_edit_form_locator).find_element(*save_btn_locator).click()


def create_page(driver, page_name):
    new_page_btn_locator = (By.CSS_SELECTOR, 'button[phx-value-type="Unscored"]')
    edit_page_btns_locator = (By.LINK_TEXT, "Edit Page")

    prev_num_pages = len(driver.find_elements(*edit_page_btns_locator))
    click_element(driver, new_page_btn_locator, 5)
    wait_for_elements(driver, edit_page_btns_locator, prev_num_pages + 1)
    driver.find_elements(*edit_page_btns_locator)[-1].click()
    rename_page(driver, page_name)


def rename_page(driver, page_name):
    edit_btn_locator = (By.CSS_SELECTOR, ".btn.btn-link.btn-sm")
    title_input_locator = (By.CSS_SELECTOR, 'input[value="New Page"]')
    save_btn_locator = (By.CSS_SELECTOR, ".btn.btn-primary.btn-sm.my-2.ml-2")

    click_element(driver, edit_btn_locator, 5)
    wait_for_element(driver, title_input_locator).send_keys(Keys.BACKSPACE * 8 + page_name)
    click_element(driver, save_btn_locator)
    # Refresh is needed because otherwise add_multiple_choice_question will be interrupted when
    # the page refreshes some time after the save btn has been clicked
    driver.refresh()


def add_multiple_choice_question(driver, question):
    resource_block_locator = (By.CSS_SELECTOR, ".resource-block-editor")
    prev_num_resource_blocks = len(driver.find_elements(*resource_block_locator))
    add_new_multiple_choice_question(driver)
    wait_for_elements(driver, resource_block_locator, prev_num_resource_blocks + 1)
    question_block = driver.find_elements(*resource_block_locator)[-1]
    fill_in_question(question_block, question)
    fill_in_answer_options(question_block, question)
    driver.execute_script("arguments[0].scrollIntoView();", question_block) # make sure ANSWER KEY btn is visible
    click_element(question_block, (By.LINK_TEXT, "ANSWER KEY"))
    fill_in_feedback(question_block, question)


def add_new_multiple_choice_question(driver):
    add_element_menu_btns_locator = (By.CSS_SELECTOR, ".addResourceContent_W\\+36phqP")
    wait_for_elements(driver, add_element_menu_btns_locator, 2)
    add_element_menu_btns = driver.find_elements(*add_element_menu_btns_locator)
    add_element_menu_btns[-1].click()
    options_bounding_box = wait_for_element(driver, (By.CSS_SELECTOR, ".activities"))
    add_MCQ_btn = options_bounding_box.find_elements(By.CSS_SELECTOR, ".resource-choice")[1]
    add_MCQ_btn.click()


def fill_in_question(question_block, question):
    question_block.find_elements(By.CSS_SELECTOR, ".slate-editor")[0].send_keys(question.question_text.replace("```", "")) # replace due to OLI otherwise creating hard to manage text blocks


def fill_in_answer_options(question_block, question):
    add_new_answer_option_div_locator = (By.CSS_SELECTOR, ".addChoiceContainer_nMRQoZI6")
    wait_for_element(question_block, add_new_answer_option_div_locator).find_element(By.CSS_SELECTOR, "button").click()
    answer_option_slate_editors = question_block.find_elements(By.CSS_SELECTOR, ".slate-editor")[1:4]
    for i in range(3):
        answer_option_slate_editors[i].send_keys(Keys.BACKSPACE * 8 + question.answer_options[i])


def fill_in_feedback(question_block, question):
    mark_correct_answer_radio_btns = question_block.find_elements(By.CSS_SELECTOR, ".oli-radio.flex-shrink-0")[3:6] # first three are on the question page
    mark_correct_answer_radio_btns[question.correct_option].click()
    correct_ans_feedback = question_block.find_element(By.CSS_SELECTOR, ".card").find_element(By.CSS_SELECTOR, ".slate-editor")
    correct_ans_feedback.send_keys(Keys.BACKSPACE * 8 + question.feedback[question.correct_option])

    add_targeted_feedback_btn = question_block.find_elements(By.CSS_SELECTOR, ".btn.btn-link.pl-0")[-1]
    add_targeted_feedback_btn.click()
    add_targeted_feedback_btn.click()
    targeted_feedback_cards = question_block.find_elements(By.CSS_SELECTOR, ".card")[2:4]

    non_correct_options = [i for i in range(3) if i != question.correct_option]
    for option_index, targeted_feedback_card in zip(non_correct_options, targeted_feedback_cards):
        select_corresponding_answer_btns = targeted_feedback_card.find_elements(By.CSS_SELECTOR, ".oli-radio.flex-shrink-0")
        select_corresponding_answer_btns[option_index].click()
        targeted_feedback_card.find_element(By.CSS_SELECTOR, ".slate-editor").send_keys(question.feedback[option_index])


def main(is_retry=False):
    
    page_definition = Page_definition.from_file(sys.argv[1])

    chrome_options = Options()
    # chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(os.getenv('CURRICULUM_URL'))

    close_cookie_banner(driver)
    login(driver, os.getenv('USER_EMAIL'), os.getenv('USER_PASSWORD'))
    
    open_unit(driver, page_definition.unit)

    create_page(driver, page_definition.page)

    global page_has_been_created
    page_has_been_created = True

    for question in page_definition.questions:
        add_multiple_choice_question(driver, question)

    sleep(3)

    print("Deployment successful!")
    print(f"Edit URL: {driver.current_url}")
    print(f"Preview URL: {driver.current_url.replace('/resource/', '/preview/')}")
    if is_retry and page_has_been_created:
        print("Due to retry of the deployment an artefact page was created. Name of the artefact is the same as created page. Please remove it manually.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if type(e) == KeyboardInterrupt:
            exit(0)
        print(e)
        TORUS_BOT_DELAY = 2
        main(is_retry=True)
