from operator import itemgetter
import time
import json

from utils import constants


def extractIngredients(string, start='(', stop=')'):
    return string[string.index(start) + 1:string.index(stop)]

def scrapeTavernData(driver, close_after=True):
    data = {}
    juice_map = {}
    phone_map = {}
    kitchen_map = {}
    cellar_map = {}
    aerator_map = {}
    distiller_map = {}
    cider_map = {}
    blender_map = {}

    machinery = [constants.ITEM_KITCHEN, constants.ITEM_CELLAR, constants.ITEM_AERATOR, constants.ITEM_DISTILLER, constants.ITEM_CIDER, constants.ITEM_BLENDER]

    driver.get(constants.BASE_URL + constants.ASUKOHT_KORTS + constants.ITEM_JUICER)
    time.sleep(1)

    for option in driver.find_element_by_class_name('mat_list').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[1:]:
        juice_map[option.find_elements_by_tag_name('td')[0].text] = option.get_attribute('id').split('_')[1]

    driver.get(constants.BASE_URL + constants.ASUKOHT_KORTS + constants.ITEM_PHONE)
    time.sleep(1)
    for option in driver.find_element_by_class_name('mat_list').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[1:]:
        phone_map[option.find_elements_by_tag_name('td')[0].text] = option.get_attribute('id').split('_')[1]

    items = []

    for machine in machinery:
        current_map = {}
        driver.get(constants.BASE_URL + constants.ASUKOHT_KORTS + machine)
        time.sleep(1)
        for option in driver.find_element_by_id('drinks_list').find_elements_by_tag_name('option')[1:]:
            items.append((option.text, int(option.get_attribute('value'))))
            current_map[option.text] = option.get_attribute('value')

        if machine == '#kitchen':
            kitchen_map = current_map
        elif machine == '#cellar':
            cellar_map = current_map
        elif machine == '#aerator':
            aerator_map = current_map
        elif machine == '#distiller':
            distiller_map = current_map
        elif machine == '#cider':
            cider_map = current_map
        elif machine == '#blender':
            blender_map = current_map

    item_to_ingredients_map = {}
    item_to_value_map = {}
    item_names = []

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

    data['tugi_map'] = phone_map
    data['juice_map'] = juice_map
    data['kitchen_map'] = kitchen_map
    data['ahi_map'] = cellar_map
    data['aerator_map'] = aerator_map
    data['distiller_map'] = distiller_map
    data['cider_map'] = cider_map
    data['blender_map'] = blender_map
    data['item_to_ingredients_map'] = item_to_ingredients_map
    data['item_to_value_map'] = item_to_value_map
    data['item_names'] = item_names

    with open('data/joogimeister.txt', 'w') as outfile:
        json.dump(data, outfile)

    if close_after:
        driver.close()
