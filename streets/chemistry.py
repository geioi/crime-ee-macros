import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import captcha_solver, constants, error_handler, vars

def checkStolenItems(driver):
    driver.get(constants.BASE_URL + constants.ASUKOHT_VARASTATUD_ESEMED)
    time.sleep(0.5)

    driver.find_element_by_name('bitems_identify').click()
    time.sleep(0.15)

def stealPlants(driver, plants_value, steal_amount = 50, token = None, narc_to_buy = None):
    stolen_amount = 0
    while stolen_amount < steal_amount:
        driver.get(constants.BASE_URL + constants.ASUKOHT_BOTAANIKAAED)
        time.sleep(0.2)

        select_plant = Select(driver.find_element_by_name('varastataim'))
        select_plant.select_by_value(plants_value)

        driver.find_element_by_xpath("//input[@value='Varasta taimed']").click()

        hasCaptcha = captcha_solver.checkForCaptcha(driver, token)
        if hasCaptcha:
            select_plant = Select(driver.find_element_by_name('varastataim'))
            select_plant.select_by_value(plants_value)
            driver.find_element_by_xpath("//input[@value='Varasta taimed']").click()
            hasCaptcha = False

        time.sleep(0.2)

        driver.get(constants.BASE_URL + constants.ASUKOHT_MAJA + constants.TEGEVUS_LABORI_KAPP)

        time.sleep(0.2)

        driver.find_element_by_name('taimedkappi').click()

        time.sleep(0.2)

        hasCaptcha = captcha_solver.checkForCaptcha(driver, token)
        if hasCaptcha:
            driver.find_element_by_name('taimedkappi').click()
            time.sleep(0.2)
            hasCaptcha = False

        stolen_amount += 1

    driver.get(constants.BASE_URL + constants.ASUKOHT_MAJA + constants.TEGEVUS_MAHLAPRESS)

    time.sleep(0.3)

    driver.find_element_by_name('jsq_quantity').send_keys(str(1000))
    select_juice = Select(driver.find_element_by_name('jsq_plant'))
    select_juice.select_by_value(plants_value)

    time.sleep(0.3)
    for i in range(0, int((steal_amount * 100) / 1000), 1):
        driver.find_element_by_xpath("//input[@value='Valmista taimedest mahla']").click()
        time.sleep(0.2)
        hasCaptcha = captcha_solver.checkForCaptcha(driver, token)
        if hasCaptcha:
            driver.find_element_by_xpath("//input[@value='Valmista taimedest mahla']").click()
            time.sleep(0.2)
            hasCaptcha = False


    driver.get(constants.BASE_URL + constants.ASUKOHT_TANAV)

    time.sleep(0.2)

    driver.find_element_by_id('myy_narkot_' + narc_to_buy).click()
    driver.find_element_by_name('selldrugs').click()


def keemik(driver, item, backpack_size, max_errors=1000, token=None, autolevel=False):
    driver.get(constants.BASE_URL + constants.ASUKOHT_TANAV)

    time.sleep(1)
    captcha_solver.checkForCaptcha(driver, token)
    time.sleep(0.1)

    captchaContainer = driver.find_element_by_id('captcha_container')

    current_level = int(driver.find_element_by_id('s_chemistry').text)
    level_updated = int(driver.find_element_by_id('s_chemistry').text)

    #belt_notification_container = driver.find_element_by_class_name('bd_lastrow2')
    for i in range(1, 31, 1):
        if driver.find_elements_by_id('myy_narkot_' + str(i)):
            print(i)
            driver.find_element_by_id('myy_narkot_' + str(i)).click()
            driver.find_element_by_name('selldrugs').click()
            break

    narc_to_buy = vars.narc_to_value_map_chemistry[vars.item_to_narc_map_chemistry[item]]
    juice_to_use = vars.juice_to_value_map_chemistry[vars.item_to_juice_map_chemistry[item]]
    narc_to_sell = vars.item_to_ready_narc_value_map_chemistry[item]
    #print(narc_to_buy)

    while True:
        #print(driver.find_element_by_id('captcha_container').value_of_css_property('display') == 'none')
        #print(captchaContainer.value_of_css_property('display') == 'none')
        #print(driver.find_element_by_id('captcha_container'))
        try:
            while driver.find_element_by_id('captcha_container').value_of_css_property('display') == 'none' and not driver.find_elements_by_css_selector('div#ajaxmessage div#message-container p.message.error') and not vars.stop_thread:
                if autolevel:
                    if int(current_level) < int(level_updated):
                        # gained a level
                        print('Gained a level!!! Congrats!')
                        if str(level_updated) in vars.level_to_item_map_chemistry:
                            keemik(driver, vars.level_to_item_map_chemistry[str(level_updated)], backpack_size, max_errors, token, autolevel)
                        else:
                            current_level = int(driver.find_element_by_id('s_chemistry').text)

                #print('here')
                grams_field = driver.find_element_by_name('osnarsumma')
                #driver.find_element_by_id('osta_narkot_' + str(narc_to_buy))
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'osta_narkot_' + str(narc_to_buy)))).click()
                if not grams_field.get_attribute('value') or int(grams_field.get_attribute('value')) < int(backpack_size):
                    grams_field.clear()
                    grams_field.send_keys(str(backpack_size))

                driver.find_element_by_name('purcdrugs').click()
                time.sleep(0.1)
                hasCaptcha = captcha_solver.checkForCaptcha(driver, token)
                if hasCaptcha:
                    driver.find_element_by_name('purcdrugs').click()
                    hasCaptcha = False

                time.sleep(0.1)

                driver.get(constants.BASE_URL + constants.ASUKOHT_MAJA + constants.TEGEVUS_TOOLAUD)

                select_drug = Select(driver.find_element_by_name('chemistry_drug1'))
                select_drug.select_by_value(narc_to_buy)

                select_juice = Select(driver.find_element_by_name('chemistry_drug2'))
                opts = select_juice.options
                available_juices = []
                for opt in opts:
                    available_juices.append(opt.get_attribute('value'))

                if juice_to_use in available_juices:
                    select_juice.select_by_value(juice_to_use)
                else:
                    print('could not find the required juice')
                    time.sleep(0.1)
                    stealPlants(driver, juice_to_use, 100, token, narc_to_buy=narc_to_buy)
                    continue
                    #return
                #return

                time.sleep(0.1)

                driver.find_element_by_class_name('nupuke420').click()
                time.sleep(0.1)
                hasCaptcha = captcha_solver.checkForCaptcha(driver, token)
                if hasCaptcha:
                    driver.find_element_by_class_name('nupuke420').click()
                    hasCaptcha = False
                time.sleep(0.1)
                if driver.find_elements_by_css_selector('div#ajaxmessage div#message-container p.message.error'):
                    print('not enough juice')
                    time.sleep(0.1)
                    stealPlants(driver, juice_to_use, 100, token, narc_to_buy=narc_to_buy)
                    continue
                    #return

                driver.get(constants.BASE_URL + constants.ASUKOHT_TANAV)

                driver.find_element_by_id('myy_narkot_' + narc_to_sell).click()
                driver.find_element_by_name('selldrugs').click()

                time.sleep(0.1)
                hasCaptcha = captcha_solver.checkForCaptcha(driver, token)
                if hasCaptcha:
                    driver.find_element_by_name('selldrugs').click()
                    hasCaptcha = False

                try:
                    level_updated = int(driver.find_element_by_id('s_chemistry').text)
                except:
                    print('ei leidnud uut levelit')
                    pass

            if vars.stop_thread:
                print('thread was signaled to stop')
                break

            else:
                captcha_solver.solveCaptcha(driver, captchaContainer, token)
        except Exception as error:
            error_handler.printError(driver, error, max_errors)
            continue



