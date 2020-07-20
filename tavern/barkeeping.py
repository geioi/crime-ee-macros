import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import captcha_solver, constants, error_handler, vars


def emptyWares(driver, ingredient_list):
    for ingredient in ingredient_list:
        if ingredient in vars.phone_map_jook:
            driver.get(constants.BASE_URL + constants.ASUKOHT_KORTS + constants.ITEM_PHONE)
            time.sleep(1)

            ingredient_val = vars.phone_map_jook[ingredient]
            try:
                driver.find_elements_by_css_selector("table.mat_list tbody tr#compo_" + ingredient_val + ".hele")[0].find_elements_by_tag_name('td')[2].click()
            except:
                print('Already out of this ingredient, continuing')
                pass

        elif ingredient in vars.juice_map_jook:
            driver.get(constants.BASE_URL + constants.ASUKOHT_KORTS + constants.ITEM_JUICER)
            time.sleep(1)

            ingredient_val = vars.juice_map_jook[ingredient]
            try:
                driver.find_elements_by_css_selector("table.mat_list tbody tr#juicel_" + ingredient_val + ".hele")[0].find_elements_by_tag_name('td')[2].click()
            except:
                print('Already out of this ingredient, continuing')
                pass

    time.sleep(1)


def restock(driver, ingredient_list, token=None, max_errors=1000):
    emptyWares(driver, ingredient_list)

    driver.get(constants.BASE_URL + constants.ASUKOHT_KORTS + constants.ITEM_PHONE)
    time.sleep(1)
    allowed_amount = int(driver.find_element_by_css_selector('div#message-container p.message.help > strong').text.replace(' ', ''))
    juice_allowed_amount = int(allowed_amount // 2)
    print(allowed_amount)

    juices_amount = 0
    has_alcohol = 0
    # do juices first, otherwise there might not be enough room for other components
    for ingredient in ingredient_list:
        if ingredient in vars.juice_map_jook:
            juices_amount += 1
            select_material = Select(driver.find_element_by_id('mat'))
            select_material.select_by_value(vars.juice_map_jook[ingredient])

            driver.find_element_by_id('quant').send_keys(str(juice_allowed_amount))
            time.sleep(0.5)
            driver.find_element_by_name('order_mat').click()

            driver.get(constants.BASE_URL + constants.ASUKOHT_KORTS + constants.ITEM_JUICER)
            time.sleep(1)

            select_material = Select(driver.find_element_by_id('mpress_n'))
            select_material.select_by_value(vars.juice_map_jook[ingredient])

            driver.find_element_by_id('mpress_a').send_keys(str(juice_allowed_amount))
            time.sleep(0.5)
            driver.find_element_by_name('make_juice').click()

            driver.get(constants.BASE_URL + constants.ASUKOHT_KORTS + constants.ITEM_PHONE)
            time.sleep(1)

        elif ingredient == 'Piiritus':
            has_alcohol = 1

            driver.get(constants.BASE_URL + constants.ASUKOHT_KORTS + constants.ITEM_DRINKS)
            time.sleep(1)

            if int(driver.find_element_by_class_name('tume').find_elements_by_tag_name('td')[1].text.replace(' ', '')) > allowed_amount:
                driver.get(constants.BASE_URL + constants.ASUKOHT_KORTS + constants.ITEM_PHONE)
                time.sleep(1)
                continue

            driver.get(constants.BASE_URL + constants.ASUKOHT_KORTS + constants.ITEM_PHONE)
            time.sleep(1)

            select_material = Select(driver.find_element_by_id('mat'))
            select_material.select_by_value(vars.phone_map_jook['Nisu'])

            driver.find_element_by_id('quant').clear()

            driver.find_element_by_id('quant').send_keys(str(int(allowed_amount // 3)))
            driver.find_element_by_name('order_mat').click()
            time.sleep(0.5)

            select_material = Select(driver.find_element_by_id('mat'))
            select_material.select_by_value(vars.phone_map_jook['Vesi'])

            driver.find_element_by_id('quant').clear()

            driver.find_element_by_id('quant').send_keys(str(int(allowed_amount // 3)))
            driver.find_element_by_name('order_mat').click()
            time.sleep(0.5)

            select_material = Select(driver.find_element_by_id('mat'))
            select_material.select_by_value(vars.phone_map_jook['Suhkur'])

            driver.find_element_by_id('quant').clear()

            driver.find_element_by_id('quant').send_keys(str(int(allowed_amount // 3)))
            driver.find_element_by_name('order_mat').click()
            time.sleep(0.5)

            makeAlcohol(driver, token, max_errors)


    for ingredient in ingredient_list:
        if ingredient in vars.phone_map_jook:
            select_material = Select(driver.find_element_by_id('mat'))
            select_material.select_by_value(vars.phone_map_jook[ingredient])

            driver.find_element_by_id('quant').clear()

            driver.find_element_by_id('quant').send_keys(str(int(allowed_amount // (len(ingredient_list) - juices_amount - has_alcohol))))
            driver.find_element_by_name('order_mat').click()

            time.sleep(0.5)

    time.sleep(1)


def makeAlcohol(driver, token, max_errors=1000):
    driver.get(constants.BASE_URL + constants.ASUKOHT_KORTS + constants.ITEM_DISTILLER)
    time.sleep(1)

    select_item = Select(driver.find_element_by_id('drinks_list'))
    select_item.select_by_value('6')  # "Level 6 - Piiritus (Nisu + Vesi + Suhkur)"

    captchaContainer = driver.find_element_by_id('captcha_container')

    while True:
        try:
            while captchaContainer.value_of_css_property('display') == 'none' and not driver.find_elements_by_css_selector('div.bar_msg div#message-container p.message.error') and not vars.stop_thread:
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'nupuke420'))).click()
                time.sleep(0.15)

            if driver.find_elements_by_css_selector('div.bar_msg div#message-container p.message.error'):
                print('materjal otsas')
                print('exiting')
                driver.get(constants.BASE_URL + constants.ASUKOHT_KORTS + constants.ITEM_PHONE)
                time.sleep(1)
                break

            if vars.stop_thread:
                print('thread was signaled to stop')
                break

            else:
                captcha_solver.solveCaptcha(driver, captchaContainer, token)

        except Exception as error:
            error_handler.printError(driver, error, max_errors)
            continue


def joogimeister(driver, action, item, max_errors=1000, token=None, autolevel=False, new_location=False):
    if new_location:
        if item in vars.kitchen_map_jook:
            action = constants.ITEM_KITCHEN
        elif item in vars.cellar_map_jook:
            action = constants.ITEM_CELLAR
        elif item in vars.aerator_map_jook:
            action = constants.ITEM_AERATOR
        elif item in vars.distiller_map_jook:
            action = constants.ITEM_DISTILLER
        elif item in vars.cider_map_jook:
            action = constants.ITEM_CIDER
        elif item in vars.blender_map_jook:
            action = constants.ITEM_BLENDER

    driver.get(constants.BASE_URL + constants.ASUKOHT_KORTS + action)

    time.sleep(1)

    select_item = Select(driver.find_element_by_id('drinks_list'))
    select_item.select_by_value(vars.item_to_value_map_jook[item])

    captchaContainer = driver.find_element_by_id('captcha_container')

    current_level = int(driver.find_element_by_id('s_barkeeping').text)
    level_updated = int(driver.find_element_by_id('s_barkeeping').text)

    while True:
        try:
            while captchaContainer.value_of_css_property('display') == 'none' and not driver.find_elements_by_css_selector('div.bar_msg div#message-container p.message.error') and not vars.stop_thread:
                if autolevel:
                    if int(current_level) < int(level_updated):
                        # gained a level
                        print('Gained a level!!! Congrats!')
                        if str(level_updated) in vars.level_to_item_map_jook:
                            emptyWares(driver, vars.item_to_ingredients_map_jook[item])
                            #restock(driver, vars.item_to_ingredients_map_jook[str(level_updated)], token, max_errors)
                            joogimeister(driver, action, vars.level_to_item_map_jook[str(level_updated)], max_errors, token, autolevel, True)
                        else:
                            current_level = int(driver.find_element_by_id('s_barkeeping').text)

                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'nupuke420'))).click()
                time.sleep(0.1)
                try:
                    level_updated = int(driver.find_element_by_id('s_barkeeping').text)
                except:
                    print('ei leidnud uut levelit')
                    pass

            if driver.find_elements_by_css_selector('div.bar_msg div#message-container p.message.error'):
                print('materjal otsas')
                restock(driver, vars.item_to_ingredients_map_jook[item], token, max_errors)
                driver.get(constants.BASE_URL + constants.ASUKOHT_KORTS + action)

                time.sleep(1)

                select_item = Select(driver.find_element_by_id('drinks_list'))
                select_item.select_by_value(vars.item_to_value_map_jook[item])

                captchaContainer = driver.find_element_by_id('captcha_container')
                continue
                #joogimeister(driver, action, item, max_errors, token)

            if vars.stop_thread:
                print('thread was signaled to stop')
                break

            else:
                captcha_solver.solveCaptcha(driver, captchaContainer, token)

        except Exception as error:
            error_handler.printError(driver, error, max_errors)
            continue
