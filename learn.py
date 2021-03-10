#Copyright (c) 2021, Advait Jayadevan Nair
#All rights reserved.
#
#This source code is licensed under the BSD-style license found in the
#LICENSE file in the root directory of this source tree. 

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import re

def check_exists(selector):
    return len(driver.find_elements_by_css_selector(selector)) > 0
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

# define
termSelector = '.SetPageTerm-wordText'
defintionSelector = '.SetPageTerm-definitionText'
loginBtnSelector = 'div.SiteNavLoginSection > button'
usernameInputSelector = '#username'
passwordInputSelector = '#password'
submitBtnSelector = 'div.UIModalBody > form > button'
isSuccesfulSelector = 'div.UIInput-labelRowLeft'
learnStartBtn = 'div.OnboardingView-gotItButton > button'

isMultipleChoice = '.MultipleChoiceQuestionPrompt'
MultipleChoiceQuestion = 'div.MultipleChoiceQuestionPrompt-promptArea > div > div > div > div > div'
multipleChoice1 = 'div.MultipleChoiceQuestionPrompt-termOptions > div:nth-child(1)'
multipleChoice2 = 'div.MultipleChoiceQuestionPrompt-termOptions > div:nth-child(2)'
multipleChoice3 = 'div.MultipleChoiceQuestionPrompt-termOptions > div:nth-child(3)'
multipleChoice4 = 'div.MultipleChoiceQuestionPrompt-termOptions > div:nth-child(4)'

isQuestion = 'div.FormattedText > div'
questionInput = 'div.AutoExpandTextarea-wrapper > textarea'

isFlashcard = '.FlippableFlashcard'
continueBtn = 'div.FlashcardQuestionView-action:nth-child(1) > div > button'

isCheckpoint = 'div.FixedActionLayout-action > div > button'

isEnd = '.EndView'

chromedriver = 'chromedriver'
quizletId = input("quizletId(For https://quizlet.com/321434504/ id is 321434504):")
username = input("username:")
password = input("password:")
driver = webdriver.Chrome(chromedriver)

# get data
driver.get('https://quizlet.com/'+quizletId)
time.sleep(1)
terms = driver.find_elements_by_css_selector(termSelector)
defintions = driver.find_elements_by_css_selector(defintionSelector)
data = {}
for i in range(len(terms)):
  data[cleanhtml(terms[i].get_attribute('innerHTML'))] = cleanhtml(defintions[i].get_attribute('innerHTML'))
del terms
del defintions
print(data)

# login
driver.find_element_by_css_selector(loginBtnSelector).click()
driver.find_element_by_css_selector(usernameInputSelector).send_keys(username)
driver.find_element_by_css_selector(passwordInputSelector).send_keys(password)
driver.find_element_by_css_selector(submitBtnSelector).click()
time.sleep(3)
if len(driver.find_elements_by_css_selector(isSuccesfulSelector)) == 0:
    print('Logged In!')
else:
    print('Credentials not valid!')
    raise SystemExit(1)

# Go to learn
driver.get('https://quizlet.com/'+quizletId+'/learn')
time.sleep(3)

# Start learn
driver.find_element_by_css_selector(learnStartBtn).click()
print('Doing learn!')
while True:
    time.sleep(1.5)
    if check_exists(isMultipleChoice) :
        print('Multiple Choice')
        ques = driver.find_element_by_css_selector(MultipleChoiceQuestion).get_attribute('innerHTML')
        opt1 = driver.find_element_by_css_selector(multipleChoice1)
        opt2 = driver.find_element_by_css_selector(multipleChoice2)
        opt3 = driver.find_element_by_css_selector(multipleChoice3)
        opt4 = driver.find_element_by_css_selector(multipleChoice4)
        if data[cleanhtml(opt1.get_attribute('innerHTML'))[1:]] == ques :
            opt1.click()
        elif data[cleanhtml(opt2.get_attribute('innerHTML'))[1:]] == ques :
            opt2.click()
        elif data[cleanhtml(opt3.get_attribute('innerHTML'))[1:]] == ques :
            opt3.click()
        else: 
            opt4.click()
    elif check_exists(isQuestion) :
        print('Question')
        ques = driver.find_element_by_css_selector(isQuestion).get_attribute('innerHTML')
        for key in data:
            if ques == data[key]:
                inputElem = driver.find_element_by_css_selector(questionInput)
                inputElem.send_keys(key)
                inputElem.submit()
                break
    elif check_exists(isFlashcard):
        driver.find_element_by_css_selector(isFlashcard).click()
        driver.find_element_by_css_selector(continueBtn).click()
    elif check_exists(isCheckpoint):
        print('Checkpoint')
        driver.find_element_by_css_selector(isCheckpoint).click()
    elif check_exists(isEnd):
        print('Finished')
        driver.quit()
        raise SystemExit(0)
    else:
        print('Unknown')
