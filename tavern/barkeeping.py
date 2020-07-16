import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import captcha_solver, constants, error_handler, vars


def joogimeister(driver, action, item, max_errors=1000, token=None):
    driver.get(constants.BASE_URL + constants.ASUKOHT_KORTS + action)

    time.sleep(1)

    select_item = Select(driver.find_element_by_id('drinks_list'))
    select_item.select_by_value(vars.item_to_value_map_jook[item])

    captchaContainer = driver.find_element_by_id('captcha_container')

    while True:
        try:
            while captchaContainer.value_of_css_property('display') == 'none' and not driver.find_elements_by_css_selector('div#ajaxmessage div#message-container p.message.error') and not vars.stop_thread:
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'nupuke420'))).click()
                time.sleep(0.1)

            if driver.find_elements_by_css_selector('div#ajaxmessage div#message-container p.message.error'):
                print('materjal otsas')
                print('exiting')
                break
                #joogimeister(driver, action, item, max_errors, token)

            if vars.stop_thread:
                print('thread was signaled to stop')
                break

            else:
                captcha_solver.solveCaptcha(driver, captchaContainer, token)

        except Exception as error:
            error_handler.printError(driver, error, max_errors)
            continue
