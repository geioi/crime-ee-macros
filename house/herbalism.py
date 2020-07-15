import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import constants
from utils import captcha_solver


def ravim(driver, action):
    global error_cnt
    driver.get(constants.BASE_URL + constants.ASUKOHT_MAJA + action)

    time.sleep(1)
    captchaContainer = driver.find_element_by_id('captcha_container')
    try:
        while captchaContainer.value_of_css_property('display') == 'none' and not driver.find_elements_by_css_selector('div#ajaxmessage div#message-container p.message.error'):
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'nupuke420'))).click()
            time.sleep(0.1)

        captcha_solver.solveCaptcha(driver, captchaContainer)
    except Exception as error:
        error_cnt += 1
        print('exception nr ' + str(error_cnt) + ' :(')
        print(error)
        if error_cnt > 1000:
            driver.close()
            exit()  # failsafe in case of infinite error
