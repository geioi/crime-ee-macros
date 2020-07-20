from operator import itemgetter
import time
import json

from utils import constants


def extractIngredients(string, start='(', stop=')'):
    return string[string.rindex(start) + 1:string.rindex(stop)]


def scrapeCraftingInfo(driver, close_after=True):
    data = {}
    kapp_map = {}
    tugi_map = {}
    puit_map = {}
    ahi_map = {}

    actions = [constants.TEGEVUS_TUGI, constants.TEGEVUS_PUIT, constants.TEGEVUS_AHI]

    driver.get(constants.BASE_URL + constants.ASUKOHT_MAJA + constants.TEGEVUS_KAPP)
    time.sleep(1)

    for i in range(1,12):
        kapp_map[driver.find_element_by_id('cmatrow_' + str(i)).find_elements_by_tag_name('td')[0].text] = str(i)

    ingredient_to_kapp_map = {'Värv': 'Värvitopsid',
                              'Tina': 'Tinatükid',
                              'Raud': 'Rauatükid',
                              'Vask': 'Vasetükid',
                              'Savi': 'Savitükid',
                              'Plastik': 'Plastikutükid',
                              'Titaan': 'Titaanitükid',
                              'Nahk': 'Nahatükid',
                              'Puit': 'Puidutükid',
                              'Niit': 'Niidirullid',
                              'Riie': 'Riiderullid'}

    items = []

    for action in actions:
        current_map = {}
        driver.get(constants.BASE_URL + constants.ASUKOHT_MAJA + action)
        time.sleep(1)
        for option in driver.find_element_by_class_name('kast').find_elements_by_tag_name('option')[1:]:
            items.append((option.text, int(option.get_attribute('value'))))
            current_map[option.text] = option.get_attribute('value')

        if action == constants.TEGEVUS_PUIT:
            puit_map = current_map
        elif action == constants.TEGEVUS_AHI:
            ahi_map = current_map
        elif action == constants.TEGEVUS_TUGI:
            tugi_map = current_map

    item_to_ingredients_map = {}
    item_to_value_map = {}
    item_names = []
    level_to_item_map = {}

    sorted_items = sorted(items, key=itemgetter(1))
    for item in sorted_items:
        ingredient_string = extractIngredients(item[0])

        ingredient_list = []
        ingredients = ingredient_string.split(' + ')
        for ingredient in ingredients:
            ingredient_list.append(ingredient)

        item_to_ingredients_map[item[0]] = ingredient_list
        item_to_value_map[item[0]] = str(item[1])
        item_names.append(item[0])

        level = item[0].split(' - ')[0].split(' ')[1]
        level_to_item_map[level] = item[0]


    data['tugi_map'] = tugi_map
    data['kapp_map'] = kapp_map
    data['puit_map'] = puit_map
    data['ahi_map'] = ahi_map
    data['item_to_ingredients_map'] = item_to_ingredients_map
    data['item_to_value_map'] = item_to_value_map
    data['item_names'] = item_names
    data['ingredient_to_kapp_map'] = ingredient_to_kapp_map
    data['level_to_item_map'] = level_to_item_map

    with open('data/kasitoo.txt', 'w') as outfile:
        json.dump(data, outfile)

    if close_after:
        driver.close()
