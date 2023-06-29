from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()

driver.get("https://www.selenium.dev/selenium/web/web-form.html")

title = driver.title
print(title)

driver.implicitly_wait(0.5)

text_box = driver.find_element(by=By.NAME, value="my-text")
password_box = driver.find_element(By.NAME, value="my-password")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
radio2 = driver.find_element(By.CSS_SELECTOR, "input#my-radio-2")

radio2.click()
text_box.send_keys("Selenium")
password_box.send_keys("password")
submit_button.click()

message = driver.find_element(by=By.ID, value="message")
value = message.text
print(value)

from time import sleep
sleep(2)

