import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from house import crafting
from utils import captcha_solver, constants, error_handler, vars

from datetime import datetime


def sepikoda(driver, action, item, anvil_qty, max_errors=1000, token=None, remake=5000, autolevel=False):
    driver.get(constants.BASE_URL + constants.ASUKOHT_MAJA + action)

    time.sleep(1)

    select_item = Select(driver.find_element_by_id('smithing_make_name'))
    select_item.select_by_value(vars.item_to_value_map_sepikoda[item])

    select_qty = Select(driver.find_element_by_id('smithing_make_quantity'))
    select_qty.select_by_value(anvil_qty)

    captchaContainer = driver.find_element_by_id('captcha_container')
    expBefore = None
    expAfter = None

    while True:
        try:
            while captchaContainer.value_of_css_property('display') == 'none' and not driver.find_elements_by_css_selector('div#ajaxmessage div#message-container p.message.error') and not vars.stop_thread:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                if (current_time > '02:28:00' and current_time < '02:30:00') or (current_time > '03:28:00' and current_time < '03:30:00'):
                    print(current_time)
                    print('Crime Factory server is about to restart, continuing in 5 minutes')
                    time.sleep(600)
                    driver.execute_script("location.reload(true);")
                    time.sleep(5)
                    sepikoda(driver, action, item, anvil_qty, max_errors, token, remake, autolevel)
                if autolevel and expBefore and expAfter:
                    if expBefore < expAfter:
                        # gained a level
                        print('Gained a level!!! Congrats!')
                        new_level = driver.find_element_by_id('s_smithing').text
                        if new_level in vars.level_to_item_map_sepikoda:
                            sepikoda(driver, action, vars.level_to_item_map_sepikoda[new_level], anvil_qty, max_errors, token, remake, autolevel)

                try:
                    expBefore = int(driver.find_element_by_id('exp_needed').text.replace(' ', ''))
                except:
                    pass

                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'nupuke420'))).click()
                time.sleep(0.11)
                try:
                    expAfter = int(driver.find_element_by_id('exp_needed').text.replace(' ', ''))
                except:
                    pass

            if driver.find_elements_by_css_selector('div#ajaxmessage div#message-container p.message.error'):
                print('materjal otsas')
                crafting.kasitoo(driver, constants.TEGEVUS_AHI, vars.weapon_to_item_map_sepikoda[vars.item_to_value_map_sepikoda[item]], counter=remake, token=token)
                driver.get(constants.BASE_URL + constants.ASUKOHT_MAJA + action)
                time.sleep(1)
                captchaContainer = driver.find_element_by_id('captcha_container')
                continue  # sepikoda(driver, action, item, anvil_qty, max_errors, token, remake)

            if vars.stop_thread:
                print('thread was signaled to stop')
                break

            else:
                captcha_solver.solveCaptcha(driver, captchaContainer, token)

        except Exception as error:
            error_handler.printError(driver, error, max_errors)
            continue
