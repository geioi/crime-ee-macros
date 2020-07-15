import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from house import crafting
from utils import captcha_solver
from utils import constants


weapon_to_item_map = {'6': '16', '7': '22', '19': '13', '8': '22', '9': '16', '10': '16', '11': '25', '12': '22',
                      '13': '22', '14': '25', '15': '25', '16': '25', '17': '28', '18': '28'}


def sepikoda(driver, action, item_value):
    global anvil_qty, error_cnt

    driver.get(constants.BASE_URL + constants.ASUKOHT_MAJA + action)

    time.sleep(1)

    select_item = Select(driver.find_element_by_id('smithing_make_name'))
    select_item.select_by_value(item_value)

    select_qty = Select(driver.find_element_by_id('smithing_make_quantity'))
    select_qty.select_by_value(anvil_qty)

    meisterdaButton = driver.find_element_by_class_name('nupuke420')
    captchaContainer = driver.find_element_by_id('captcha_container')

    while True:
        try:
            while captchaContainer.value_of_css_property('display') == 'none' and not driver.find_elements_by_css_selector('div#ajaxmessage div#message-container p.message.error'):
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'nupuke420'))).click()
                time.sleep(0.1)

            if driver.find_elements_by_css_selector('div#ajaxmessage div#message-container p.message.error'):
                print('materjal otsas')
                crafting.kasitoo(constants.TEGEVUS_AHI, weapon_to_item_map[item_value], counter=9000)
                sepikoda(action, item_value)

            else:
                captcha_solver.solveCaptcha(driver, captchaContainer)

        except Exception as error:
            error_cnt += 1
            print('exception nr ' + str(error_cnt) + ':(')
            print(error)
            if error_cnt > 1000:
                driver.close()
                exit()  # failsafe in case of infinite error
            continue
