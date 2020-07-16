import threading
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from multiprocessing import Process

from utils import constants, captcha_solver, error_handler, vars


def restock(driver, values, amount_of_restock=150, restock_cnt=0):  # takes array of values to buy
    wait_time = 0.2
    print(values)
    for value in values:
        while restock_cnt < amount_of_restock:
            driver.get(constants.BASE_URL + constants.ASUKOHT_SLUMM_TURG_CRFT + '&ese=' + vars.kapp_map[vars.ingredient_to_kapp_map[value]] + '#x')
            time.sleep(wait_time)
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, 'purchcrafitem'))).click()
            time.sleep(wait_time)
            driver.get(constants.BASE_URL + constants.ASUKOHT_MAJA + constants.TEGEVUS_KAPP)
            time.sleep(wait_time)
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, 'ktookappi'))).click()
            time.sleep(wait_time)
            restock_cnt += 1

        restock_cnt = 0


def kasitoo(driver, action, item, counter=0, item_craft_cnt=0, max_errors=1000, token=None):
    driver.get(constants.BASE_URL + constants.ASUKOHT_MAJA + action)

    time.sleep(1)

    select = Select(driver.find_element_by_class_name('kast'))
    select.select_by_value(vars.item_to_value_map_kasitoo[item])

    captchaContainer = driver.find_element_by_id('captcha_container')

    while True:
        try:
            if counter != 0:
                while captchaContainer.value_of_css_property('display') == 'none' and not driver.find_elements_by_css_selector('div#ajaxmessage div#message-container p.message.error') and item_craft_cnt < counter and not vars.stop_thread:
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'nupuke420'))).click()
                    item_craft_cnt += 1
                    time.sleep(0.1)

                if item_craft_cnt == counter:
                    item_craft_cnt = 0
                    return
            else:
                while captchaContainer.value_of_css_property('display') == 'none' and not driver.find_elements_by_css_selector('div#ajaxmessage div#message-container p.message.error') and not vars.stop_thread:
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'nupuke420'))).click()
                    time.sleep(0.1)

            if driver.find_elements_by_css_selector('div#ajaxmessage div#message-container p.message.error'):
                print('materjal otsas')
                restock(driver, vars.item_to_ingredients_map_kasitoo[item])  #restock(item_to_material_map[item_value])
                kasitoo(driver, action, item, counter, item_craft_cnt, token=token)

            if vars.stop_thread:
                print('thread is signaled to stop')
                break

            else:
                captcha_solver.solveCaptcha(driver, captchaContainer, token)
        except Exception as error:
            error_handler.printError(driver, error, max_errors)
            continue
