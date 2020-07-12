import io
import time

import requests
from PIL import Image
from anticaptchaofficial.imagecaptcha import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


username = ''
password = ''
token = ''
base_url = 'https://valge.crime.ee/index.php?'

#### LOCATIONS ####
ASUKOHT_MAJA = 'asukoht=house'
ASUKOHT_KORTS = 'asukoht=tavern'
ASUKOHT_SOOKLA = 'asukoht=tavern&korrus=2'
ASUKOHT_TANAV = 'asukoht=tanav'
ASUKOHT_SLUMM_TURG_CRFT = 'asukoht=slumm&paik=4&lett=2'
#### END OF LOCATIONS ####


##### HOUSE ACTIONS #####

#crafting
TEGEVUS_KAPP = '&tegevus=materialsstorage'
TEGEVUS_TUGI = '&tegevus=chair'
TEGEVUS_PUIT = '&tegevus=desk'
TEGEVUS_AHI = '&tegevus=ovens'

#blacksmith
TEGEVUS_ALAS = '&tegevus=anvil'

#drug lab
TEGEVUS_RAVI = '&tegevus=ravipaki'

##### END OF HOUSE ACTIONS #####

error_cnt = 0
restock_cnt = 0
item_craft_cnt = 0
anvil_qty = '7'

item_to_material_map = {'10': ['10'], '12': ['5'], '16': ['11'], '22': ['7', '11'], '25': ['5', '11'], '26': ['5', '7'], '27': ['5', '7'],
                        '28': ['5', '7', '11'], '29': ['5', '10'], '30': ['5', '10'], '33': ['4', '5', '7'], '35': ['4', '5', '8'],
                        '37': ['7', '10'], '39': ['7', '9', '10'], '23': ['1', '3'], '31': ['3'], '32': ['3'], '36': ['1', '3', '10'],
                        '24': ['1', '2'], '34': ['2', '6'], '38': ['1', '2', '6'], '40': ['1', '2', '6'], '13': ['5']}

weapon_to_item_map = {'6': '16', '7': '22', '19': '13', '8': '22', '9': '16', '10': '16', '11': '25', '12': '22',
                      '13': '22', '14': '25', '15': '25', '16': '25', '17': '28', '18': '28'}


#### CAPTCHA SOLVING ####

def getPictureAnswer(link):
    page = requests.get(link)
    b = page.content
    file_bytes = io.BytesIO(b)
    image = Image.open(file_bytes)
    image.save('test.png')
    return sendAPIRequest('test.png')

def sendAPIRequest(image):
    global token
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_numeric(1)
    solver.set_key(token)

    captcha_text = solver.solve_and_return_solution(image)
    if captcha_text != 0:
        print('captcha answer is: ' + captcha_text)
        return captcha_text
    else:
        print("task finished with error " + solver.error_code)
        #send new request
        return sendAPIRequest(image)

def solveCaptcha(driver, captchaContainer):
    print('captcha time')
    guessed = False
    wrongAnswerCounter = 0
    while not guessed:
        if wrongAnswerCounter > 15:
            driver.close()
            exit()
        src_image = driver.find_element_by_id('captcha_img').get_attribute('src')
        answer = getPictureAnswer(src_image)
        driver.find_element_by_id('trivia_input').send_keys(answer)
        wrongAnswerCounter += 1
        time.sleep(1)
        if captchaContainer.value_of_css_property('display') == 'none':
            guessed = True

#### END OF CAPTCHA SOLVING ####


#### AUTOMATION TASKS ####

def restock(values):  #takes array of values to buy
    global restock_cnt
    wait_time = 0.2
    print(values)
    for value in values:
        while restock_cnt < 150: #it's a great, great number
            driver.get(base_url + ASUKOHT_SLUMM_TURG_CRFT + '&ese=' + value + '#x')
            time.sleep(wait_time)
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, 'purchcrafitem'))).click()
            time.sleep(wait_time)
            driver.get(base_url + ASUKOHT_MAJA + TEGEVUS_KAPP)
            time.sleep(wait_time)
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, 'ktookappi'))).click()
            time.sleep(wait_time)
            restock_cnt += 1

        restock_cnt = 0

def kasitoo(action, item_value, counter=0):
    global item_craft_cnt, error_cnt
    noCaptcha = True

    driver.get(base_url + ASUKOHT_MAJA + action)

    time.sleep(1)

    select = Select(driver.find_element_by_class_name('kast'))
    select.select_by_value(item_value)

    meisterdaButton = driver.find_element_by_class_name('nupuke420')
    captchaContainer = driver.find_element_by_id('captcha_container')


    while noCaptcha:
        try:
            if counter != 0:
                while captchaContainer.value_of_css_property('display') == 'none' and not driver.find_elements_by_css_selector('div#ajaxmessage div#message-container p.message.error') and item_craft_cnt < counter:
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'nupuke420'))).click()
                    item_craft_cnt += 1
                    time.sleep(0.1)

                if item_craft_cnt == counter:
                    item_craft_cnt = 0
                    return
            else:
                while captchaContainer.value_of_css_property('display') == 'none' and not driver.find_elements_by_css_selector('div#ajaxmessage div#message-container p.message.error'):
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'nupuke420'))).click()
                    time.sleep(0.1)
                #driver.close()

            if (driver.find_elements_by_css_selector('div#ajaxmessage div#message-container p.message.error')):
                print('materjal otsas')
                restock(item_to_material_map[item_value])
                kasitoo(action, item_value, counter)

            else:
                solveCaptcha(driver, captchaContainer)
                #noCaptcha = False
        except Exception as error:
            error_cnt += 1
            print('exception nr ' + str(error_cnt) + ':(')
            print(error)
            if error_cnt > 1000:
                driver.close()
                exit() #failsafe in case of infinite error
            continue

    #print(driver.find_element_by_id('captcha_img').get_attribute('src'))

def ravim(action):
    global error_cnt
    driver.get(base_url + ASUKOHT_MAJA + action)

    time.sleep(1)
    captchaContainer = driver.find_element_by_id('captcha_container')
    try:
        while captchaContainer.value_of_css_property('display') == 'none' and not driver.find_elements_by_css_selector('div#ajaxmessage div#message-container p.message.error'):
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'nupuke420'))).click()
            #meisterdaButton.click()
            time.sleep(0.1)

        solveCaptcha(driver, captchaContainer)
    except Exception as error:
        error_cnt += 1
        print('exception nr ' + str(error_cnt) + ':(')
        print(error)
        if error_cnt > 1000:
            driver.close()
            exit()  # failsafe in case of infinite error
    #driver.close()
    #print(driver.find_element_by_id('captcha_img').get_attribute('src'))

def sepikoda(action, item_value):
    global anvil_qty, error_cnt
    noCaptcha = True

    #item_value = 6 ( lvl 38 )
    driver.get(base_url + ASUKOHT_MAJA + action)

    time.sleep(1)

    select_item = Select(driver.find_element_by_id('smithing_make_name'))
    select_item.select_by_value(item_value)

    select_qty = Select(driver.find_element_by_id('smithing_make_quantity'))
    select_qty.select_by_value(anvil_qty)

    meisterdaButton = driver.find_element_by_class_name('nupuke420')
    captchaContainer = driver.find_element_by_id('captcha_container')


    while noCaptcha:
        try:
            while captchaContainer.value_of_css_property('display') == 'none' and not driver.find_elements_by_css_selector('div#ajaxmessage div#message-container p.message.error'):
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'nupuke420'))).click()
                time.sleep(0.1)
            # driver.close()

            if driver.find_elements_by_css_selector('div#ajaxmessage div#message-container p.message.error'):
                print('materjal otsas')
                kasitoo(TEGEVUS_AHI, weapon_to_item_map[item_value], counter=5000)
                sepikoda(action, item_value)

            else:
                solveCaptcha(driver, captchaContainer)

        except Exception as error:
            error_cnt += 1
            print('exception nr ' + str(error_cnt) + ':(')
            print(error)
            if error_cnt > 1000:
                driver.close()
                exit()  # failsafe in case of infinite error
            continue
                #noCaptcha = False


#### END OF AUTOMATION TASKS ####



with open('config.txt') as f:
    lines = f.readlines()
    username = lines[0].strip()
    password = lines[1].strip()
    token = lines[2].strip()

driver = webdriver.Chrome()
driver.get('https://www.crime.ee')
driver.find_element_by_id('white').click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'username5'))).send_keys(username)
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'password5'))).send_keys(password)
driver.find_element_by_id('password5').send_keys(Keys.RETURN)

time.sleep(1)

sepikoda(TEGEVUS_ALAS, '11')
#kasitoo(TEGEVUS_AHI, '25')
#restock(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'])
#restock(['5', '11'])
