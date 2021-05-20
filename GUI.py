from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import tkinter as tk
from tkinter import ttk
import json
from tkinter import *
from os import path
import time
import threading

from scrapers import crafting_scraper, tavern_scraper, blacksmith_scraper, chemistry_scraper
from utils import credentials_handler, constants, vars
from house import crafting, blacksmithing, herbalism
from tavern import barkeeping
from streets import chemistry


t = threading.Thread()


def startDriverAndLogin(world='white'):
    global driver
    #disable and enable buttons
    enableButtons()

    window.update_idletasks()

    #start webdriver
    driver = webdriver.Chrome()
    driver.get('https://www.crime.ee')
    driver.find_element_by_id(world).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'username5'))).send_keys(username)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'password5'))).send_keys(password)
    driver.find_element_by_id('password5').send_keys(Keys.RETURN)

    time.sleep(1)


def changeProcess():
    global driver
    tab = getTabTitle()
    print(tab)
    if tab == 'Käsitöö':
        getSelectionKasi(change=True)

    elif tab == 'Joogimeister':
        getSelectionJook(True)

    elif tab == 'Sepikoda':
        getSelectionSepikoda(True)
    elif tab == 'Keemik':
        getSelectionChemistry(True)


def stopProcess():
    global driver, t
    vars.stop_thread = True
    t.join(2)
    driver.close()
    disableButtons()


def disableButtons():
    btn1_kasi['state'] = 'normal'
    btn2_kasi['state'] = 'disabled'
    btn3_kasi['state'] = 'disabled'
    btn1_jook['state'] = 'normal'
    btn2_jook['state'] = 'disabled'
    btn3_jook['state'] = 'disabled'
    btn1_sepikoda['state'] = 'normal'
    btn2_sepikoda['state'] = 'disabled'
    btn3_sepikoda['state'] = 'disabled'
    btn1_keemik['state'] = 'normal'
    btn2_keemik['state'] = 'disabled'
    btn3_keemik['state'] = 'disabled'


def enableButtons():
    btn1_jook['state'] = 'disabled'
    btn2_jook['state'] = 'normal'
    btn3_jook['state'] = 'normal'
    btn1_kasi['state'] = 'disabled'
    btn2_kasi['state'] = 'normal'
    btn3_kasi['state'] = 'normal'
    btn1_sepikoda['state'] = 'disabled'
    btn2_sepikoda['state'] = 'normal'
    btn3_sepikoda['state'] = 'normal'
    btn1_keemik['state'] = 'disabled'
    btn2_keemik['state'] = 'normal'
    btn3_keemik['state'] = 'normal'


def getSelectionJook(change=False):
    global chosen_option, t
    chosen_option = dropdown_joogimeister.get()
    autolevel = autolevel_jook.get()
    if not change:
        startDriverAndLogin()
    elif change:
        print('trying to change action to joogimeister')
        print('new item to make: ' + chosen_option)
        vars.stop_thread = True
        t.join(2)

    vars.stop_thread = False

    if chosen_option in vars.kitchen_map_jook:
        t = threading.Thread(target=barkeeping.joogimeister, args=(driver, constants.ITEM_KITCHEN, chosen_option,),
                             kwargs={'token': token, 'autolevel': autolevel})
        t.start()
    elif chosen_option in vars.cellar_map_jook:
        t = threading.Thread(target=barkeeping.joogimeister, args=(driver, constants.ITEM_CELLAR, chosen_option,),
                             kwargs={'token': token, 'autolevel': autolevel})
        t.start()
    elif chosen_option in vars.aerator_map_jook:
        t = threading.Thread(target=barkeeping.joogimeister, args=(driver, constants.ITEM_AERATOR, chosen_option,),
                             kwargs={'token': token, 'autolevel': autolevel})
        t.start()
    elif chosen_option in vars.distiller_map_jook:
        t = threading.Thread(target=barkeeping.joogimeister, args=(driver, constants.ITEM_DISTILLER, chosen_option,),
                             kwargs={'token': token, 'autolevel': autolevel})
        t.start()
    elif chosen_option in vars.cider_map_jook:
        t = threading.Thread(target=barkeeping.joogimeister, args=(driver, constants.ITEM_CIDER, chosen_option,),
                             kwargs={'token': token, 'autolevel': autolevel})
        t.start()
    elif chosen_option in vars.blender_map_jook:
        t = threading.Thread(target=barkeeping.joogimeister, args=(driver, constants.ITEM_BLENDER, chosen_option,),
                             kwargs={'token': token, 'autolevel': autolevel})
        t.start()


def getSelectionKasi(change=False):
    global chosen_option, t
    chosen_option = dropdown_kasitoo.get()
    autolevel = autolevel_kasi.get()
    if not change:
        startDriverAndLogin()
    elif change:
        print('trying to change action to käsitöö')
        print('new item to make: ' + chosen_option)
        vars.stop_thread = True
        t.join(2)

    vars.stop_thread = False
    if chosen_option in vars.puit_map:
        t = threading.Thread(target=crafting.kasitoo, args=(driver, constants.TEGEVUS_PUIT, chosen_option,), kwargs={'token': token, 'autolevel': autolevel})
        t.start()
    elif chosen_option in vars.tugi_map:
        t = threading.Thread(target=crafting.kasitoo, args=(driver, constants.TEGEVUS_TUGI, chosen_option,), kwargs={'token': token, 'autolevel': autolevel})
        t.start()
    elif chosen_option in vars.ahi_map:
        t = threading.Thread(target=crafting.kasitoo, args=(driver, constants.TEGEVUS_AHI, chosen_option,), kwargs={'token': token, 'autolevel': autolevel})
        t.start()


def getSelectionSepikoda(change=False):
    global chosen_option, t
    chosen_option = dropdown_menu_sepikoda.get()
    restock_amount = 5000
    qty_amount = '1'
    print(chosen_option)
    restock_amount = restock_entry.get()
    qty_amount = qty_entry.get()
    autolevel = autolevel_sepikoda.get()

    if not change:
        startDriverAndLogin()
    elif change:
        print('trying to change action to sepikoda')
        print('new item to make: ' + chosen_option)
        vars.stop_thread = True
        t.join(2)

    vars.stop_thread = False

    t = threading.Thread(target=blacksmithing.sepikoda, args=(driver, constants.TEGEVUS_ALAS, chosen_option, qty_amount,), kwargs={'token': token, 'remake': int(restock_amount), 'autolevel': autolevel})
    t.start()

def getSelectionChemistry(change=False):
    global chosen_option, t
    chosen_option = dropdown_menu_keemik.get()
    bakcpack_size = '100'
    print(chosen_option)
    autolevel = autolevel_keemik.get()
    backpack_size = backpack_size_entry.get()

    if not change:
        startDriverAndLogin()
    elif change:
        print('trying to change action to keemik')
        print('new item to make: ' + chosen_option)
        vars.stop_thread = True
        t.join(2)

    vars.stop_thread = False

    t = threading.Thread(target=chemistry.keemik,
                         args=(driver, chosen_option, backpack_size),
                         kwargs={'token': token, 'autolevel': autolevel})
    t.start()

def getTabTitle():
    return tabControl.tab(tabControl.select(), 'text')


def saveCredButtonClicked():
    credentials_handler.saveCredentials(e1.get(), e2.get(), e3.get())
    notice_label['text'] = "Credentials saved!"


def getAllData():
    startDriverAndLogin()

    crafting_scraper.scrapeCraftingInfo(driver, close_after=False)
    tavern_scraper.scrapeTavernData(driver)
    blacksmith_scraper.readData()
    chemistry_scraper.readData()
    disableButtons()


def getCraftingData():
    startDriverAndLogin()
    crafting_scraper.scrapeCraftingInfo(driver)
    disableButtons()


def getTavernData():
    startDriverAndLogin()
    tavern_scraper.scrapeTavernData(driver)
    disableButtons()


def getBlacksmithData():
    blacksmith_scraper.readData()

def getChemistryData():
    chemistry_scraper.readData()


driver = None
chosen_option = None
window = tk.Tk()
window.title('Crime.ee Autoclicker')
window.geometry('600x400')

tabControl = ttk.Notebook(window)

tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text='Käsitöö')

tab3 = ttk.Frame(tabControl)
tabControl.add(tab3, text='Joogimeister')

tab4 = ttk.Frame(tabControl)
tabControl.add(tab4, text='Sepikoda')

tab5 = ttk.Frame(tabControl)
tabControl.add(tab5, text='Keemik')
tabControl.grid(row=3, columnspan=4, pady=10, padx=10)


#
Label(window, text="Username").grid(row=0)
Label(window, text="Password").grid(row=1)
Label(window, text="API Token").grid(row=2)
notice_label = Label(window, text="")
notice_label.grid(row=0, rowspan=3, column=3, padx=20)

e1 = Entry(window)
e2 = Entry(window, show='*')
e3 = Entry(window, show='*')

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)

btn_save_credentials = Button(window, text='Save credentials', command=saveCredButtonClicked)
btn_save_credentials.grid(row=1, column=2)

btn_get_crafting = Button(window, text='Get Crafting Data', command=getCraftingData)
btn_get_crafting.grid(row=4, column=0, pady=10, padx=10)

btn_get_tavern = Button(window, text='Get Tavern Data', command=getTavernData)
btn_get_tavern.grid(row=4, column=1, sticky=W, padx=10, pady=10)

btn_get_blacksmith = Button(window, text='Get Blacksmith Data', command=getBlacksmithData())
btn_get_blacksmith.grid(row=4, column=2, sticky=W, padx=10, pady=10)

btn_get_blacksmith = Button(window, text='Get Chemistry Data', command=getChemistryData())
btn_get_blacksmith.grid(row=4, column=3, sticky=W, padx=10, pady=10)

btn_get_all = Button(window, text='Get all Data', command=getAllData)
btn_get_all.grid(row=5, column=1, sticky=W, pady=10, padx=10)

if path.exists('config.txt'):
    username, password, token = credentials_handler.getCredentials()
    e1.insert(0, username)
    e2.insert(0, password)
    e3.insert(0, token)


#### LOAD IN CRAFTING DATA
if path.exists('data/kasitoo.txt'):
    with open('data/kasitoo.txt') as json_file:
        data_kasitoo = json.load(json_file)
        vars.puit_map = data_kasitoo['puit_map']
        vars.tugi_map = data_kasitoo['tugi_map']
        vars.kapp_map = data_kasitoo['kapp_map']
        vars.ahi_map = data_kasitoo['ahi_map']
        vars.item_to_ingredients_map_kasitoo = data_kasitoo['item_to_ingredients_map']
        vars.item_to_value_map_kasitoo = data_kasitoo['item_to_value_map']
        vars.item_names_kasitoo = data_kasitoo['item_names']
        vars.ingredient_to_kapp_map = data_kasitoo['ingredient_to_kapp_map']
        vars.level_to_item_map_kasitoo = data_kasitoo['level_to_item_map']


dropdown_kasitoo = tk.StringVar()
dropdown_kasitoo.set(vars.item_names_kasitoo[0])
dropdown_menu_kasitoo = ttk.Combobox(tab2, textvariable=dropdown_kasitoo, values=data_kasitoo['item_names'], width=50)
dropdown_menu_kasitoo.grid(row=0, columnspan=3)

autolevel_kasi = IntVar()
Checkbutton(tab2, text="Automatically move to next item when the level allows", variable=autolevel_kasi).grid(row=1, column=1, sticky=W)

btn1_kasi = Button(tab2, text='Start', command=getSelectionKasi)
btn1_kasi.grid(row=2, column=0, pady=10, padx=10)
btn2_kasi = Button(tab2, text='Change item (choose new item first from dropdown)', command=changeProcess)
btn2_kasi.grid(row=2, column=1, pady=10, padx=10)
btn3_kasi = Button(tab2, text='Stop', command=stopProcess)
btn3_kasi.grid(row=3, columnspan=2, pady=10, padx=10)


#### LOAD IN BARKEEPING DATA
if path.exists('data/joogimeister.txt'):
    with open('data/joogimeister.txt') as json_file:
        data_joogid = json.load(json_file)
        vars.phone_map_jook = data_joogid['phone_map']
        vars.juice_map_jook = data_joogid['juice_map']
        vars.kitchen_map_jook = data_joogid['kitchen_map']
        vars.cellar_map_jook = data_joogid['cellar_map']
        vars.aerator_map_jook = data_joogid['aerator_map']
        vars.distiller_map_jook = data_joogid['distiller_map']
        vars.cider_map_jook = data_joogid['cider_map']
        vars.blender_map_jook = data_joogid['blender_map']
        vars.item_to_ingredients_map_jook = data_joogid['item_to_ingredients_map']
        vars.item_to_value_map_jook = data_joogid['item_to_value_map']
        vars.item_names_jook = data_joogid['item_names']
        vars.level_to_item_map_jook = data_joogid['level_to_item_map']

dropdown_joogimeister = tk.StringVar()
dropdown_joogimeister.set(data_joogid['item_names'][0])
dropdown_menu_joogimeister = ttk.Combobox(tab3, textvariable=dropdown_joogimeister, values=data_joogid['item_names'], width=50)
dropdown_menu_joogimeister.grid(row=0, columnspan=3)

autolevel_jook = IntVar()
Checkbutton(tab3, text="Automatically move to next item when the level allows", variable=autolevel_jook).grid(row=1, column=1, sticky=W)

btn1_jook = Button(tab3, text='Start', command=getSelectionJook)
btn1_jook.grid(row=2, column=0, pady=10, padx=10)
btn2_jook = Button(tab3, text='Change item (choose new item first from dropdown)', command=changeProcess)
btn2_jook.grid(row=2, column=1, pady=10, padx=10)
btn3_jook = Button(tab3, text='Stop', command=stopProcess)
btn3_jook.grid(row=3, columnspan=2, pady=10, padx=10)


#### LOAD IN BLACKSMITHING DATA
if path.exists('data/sepikoda.txt'):
    with open('data/sepikoda.txt') as json_file:
        data_sepikoda = json.load(json_file)
        vars.item_names_sepikoda = data_sepikoda['item_names']
        vars.item_to_value_map_sepikoda = data_sepikoda['item_to_value_map']
        vars.weapon_to_item_map_sepikoda = data_sepikoda['weapon_to_item_map']
        vars.level_to_item_map_sepikoda = data_sepikoda['level_to_item_map']

dropdown_sepikoda = tk.StringVar()
dropdown_sepikoda.set(data_sepikoda['item_names'][0])
dropdown_menu_sepikoda = ttk.Combobox(tab4, textvariable=dropdown_sepikoda, values=data_sepikoda['item_names'], width=50)
dropdown_menu_sepikoda.grid(row=0, columnspan=3)

autolevel_sepikoda = IntVar()
Checkbutton(tab4, text="Automatically move to next item when the level allows", variable=autolevel_sepikoda).grid(row=2, column=1, sticky=W)

btn1_sepikoda = Button(tab4, text='Start', command=getSelectionSepikoda)
btn1_sepikoda.grid(row=3, column=0, pady=10, padx=10)
btn2_sepikoda = Button(tab4, text='Change item (choose new item first from dropdown)', command=changeProcess)
btn2_sepikoda.grid(row=3, column=1, pady=10, padx=10)
btn3_sepikoda = Button(tab4, text='Stop', command=stopProcess)
btn3_sepikoda.grid(row=4, columnspan=2, pady=10, padx=10)

Label(tab4, text="Qty at once").grid(row=1, column=0)
qty_entry = Entry(tab4)
qty_entry.grid(row=1, column=1, sticky=W)
qty_entry['width'] = 5
qty_entry.insert(0, '1')

Label(tab4, text="Restock amount").grid(row=1, column=2, sticky=E)
restock_entry = Entry(tab4)
restock_entry.grid(row=1, column=3, sticky=W)
restock_entry['width'] = 10
restock_entry.insert(0, 5000)


#### LOAD IN CHEMISTRY DATA
if path.exists('data/chemistry.txt'):
    with open('data/chemistry.txt') as json_file:
        data_keemik = json.load(json_file)
        vars.plant_to_value_map_chemistry = data_keemik['plant_to_value_map']
        vars.juice_to_value_map_chemistry = data_keemik['juice_to_value_map']
        vars.item_names_chemistry = data_keemik['item_names']
        vars.narc_to_value_map_chemistry = data_keemik['narc_to_value_map']
        vars.level_to_item_map_chemistry = data_keemik['level_to_item_map']
        vars.item_to_narc_map_chemistry = data_keemik['item_to_narc_map']
        vars.item_to_ready_narc_value_map_chemistry = data_keemik['item_to_ready_narc_value_map']
        vars.item_to_juice_map_chemistry = data_keemik['item_to_juice_map']

dropdown_keemik = tk.StringVar()
dropdown_keemik.set(data_keemik['item_names'][0])
dropdown_menu_keemik = ttk.Combobox(tab5, textvariable=dropdown_keemik, values=data_keemik['item_names'], width=50)
dropdown_menu_keemik.grid(row=0, columnspan=3)

autolevel_keemik = IntVar()
Checkbutton(tab5, text="Automatically move to next item when the level allows", variable=autolevel_keemik).grid(row=2, column=1, sticky=W)

btn1_keemik = Button(tab5, text='Start', command=getSelectionChemistry)
btn1_keemik.grid(row=3, column=0, pady=10, padx=10)
btn2_keemik = Button(tab5, text='Change item (choose new item first from dropdown)', command=changeProcess)
btn2_keemik.grid(row=3, column=1, pady=10, padx=10)
btn3_keemik = Button(tab5, text='Stop', command=stopProcess)
btn3_keemik.grid(row=4, columnspan=2, pady=10, padx=10)

Label(tab5, text="Bakcpack size").grid(row=1, column=0)
backpack_size_entry = Entry(tab5)
backpack_size_entry.grid(row=1, column=1, sticky=W)
backpack_size_entry['width'] = 5
backpack_size_entry.insert(0, '100')

btn2_kasi['state'] = 'disabled'
btn3_kasi['state'] = 'disabled'
btn2_jook['state'] = 'disabled'
btn3_jook['state'] = 'disabled'
btn2_sepikoda['state'] = 'disabled'
btn3_sepikoda['state'] = 'disabled'
btn2_keemik['state'] = 'disabled'
btn3_keemik['state'] = 'disabled'

window.mainloop()
