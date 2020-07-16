import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from house import crafting
from utils import captcha_solver, constants, error_handler, vars


def sepikoda(driver, action, item, anvil_qty, max_errors=1000, token=None, remake=5000):
    driver.get(constants.BASE_URL + constants.ASUKOHT_MAJA + action)

    time.sleep(1)

    select_item = Select(driver.find_element_by_id('smithing_make_name'))
    select_item.select_by_value(vars.item_to_value_map_sepikoda[item])

    select_qty = Select(driver.find_element_by_id('smithing_make_quantity'))
    select_qty.select_by_value(anvil_qty)

    captchaContainer = driver.find_element_by_id('captcha_container')

    while True:
        try:
            while captchaContainer.value_of_css_property('display') == 'none' and not driver.find_elements_by_css_selector('div#ajaxmessage div#message-container p.message.error') and not vars.stop_thread:
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'nupuke420'))).click()
                time.sleep(0.1)

            if driver.find_elements_by_css_selector('div#ajaxmessage div#message-container p.message.error'):
                print('materjal otsas')
                crafting.kasitoo(driver, constants.TEGEVUS_AHI, vars.weapon_to_item_map_sepikoda[vars.item_to_value_map_sepikoda[item]], counter=remake, token=token)
                sepikoda(driver, action, item, anvil_qty, max_errors, token, remake)

            if vars.stop_thread:
                print('thread was signaled to stop')
                break

            else:
                captcha_solver.solveCaptcha(driver, captchaContainer, token)

        except Exception as error:
            error_handler.printError(driver, error, max_errors)
            continue
