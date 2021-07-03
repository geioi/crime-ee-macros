import io
import time

import requests
from PIL import Image
from anticaptchaofficial.imagecaptcha import imagecaptcha


def getPictureAnswer(link, token=None):
    page = requests.get(link, timeout=0.1)
    b = page.content
    file_bytes = io.BytesIO(b)
    image = Image.open(file_bytes)
    image.save('captcha.png')
    return sendAPIRequest('captcha.png', token)


def sendAPIRequest(image, token=None):
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_numeric(1)
    solver.set_key(token)

    try:
        captcha_text = solver.solve_and_return_solution(image)
    except Exception as err:
        print('Probably 500 error, trying again in 5 seconds')
        time.sleep(5)
        return sendAPIRequest(image, token=token)
    print(captcha_text)
    if captcha_text != 0:
        print('captcha answer is: ' + captcha_text)
        return captcha_text
    else:
        print("task finished with error " + solver.error_code)
        #send new request
        return sendAPIRequest(image, token)


def solveCaptcha(driver, captchaContainer, token=None):
    print('captcha time')
    guessed = False
    wrongAnswerCounter = 0
    while not guessed:
        if wrongAnswerCounter > 15:
            driver.close()
            exit()
        src_image = driver.find_element_by_id('captcha_img').get_attribute('src')
        answer = getPictureAnswer(src_image, token)
        driver.find_element_by_id('trivia_input').send_keys(answer)
        wrongAnswerCounter += 1
        time.sleep(1)
        if captchaContainer.value_of_css_property('display') == 'none':
            guessed = True

def checkForCaptcha(driver, token=None):
    if driver.find_elements_by_id('captcha_container'):
        if not driver.find_element_by_id('captcha_container').value_of_css_property('display') == 'none':
            solveCaptcha(driver, driver.find_element_by_id('captcha_container'), token)
            return True
