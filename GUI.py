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

from scrapers import crafting_scraper
from scrapers import tavern_scraper
from utils import credentials_handler, constants, vars
from house import crafting, blacksmithing, herbalism
from tavern import barkeeping


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
    driver.get('https://www.google.com')


def stopProcess():
    global driver
    driver.close()
    disableButtons()


def disableButtons():
    btn1_kasi['state'] = 'normal'
    btn2_kasi['state'] = 'disabled'
    btn3_kasi['state'] = 'disabled'
    btn1_jook['state'] = 'normal'
    btn2_jook['state'] = 'disabled'
    btn3_jook['state'] = 'disabled'


def enableButtons():
    btn1_jook['state'] = 'disabled'
    btn2_jook['state'] = 'normal'
    btn3_jook['state'] = 'normal'
    btn1_kasi['state'] = 'disabled'
    btn2_kasi['state'] = 'normal'
    btn3_kasi['state'] = 'normal'


def getSelectionJook():
    global chosen_option
    chosen_option = dropdown_joogimeister.get()
    if chosen_option in data_joogid['kitchen_map']:
        print('item is found in kitchen')
    elif chosen_option in data_joogid['cellar_map']:
        print('item is found in cellar')
    elif chosen_option in data_joogid['aerator_map']:
        print('item is found in aerator')
    elif chosen_option in data_joogid['distiller_map']:
        print('item is found in distiller')
    elif chosen_option in data_joogid['cider_map']:
        print('item is found in cider')
    elif chosen_option in data_joogid['blender_map']:
        print('item is found in blender')

    #startProcess()


def getSelectionKasi():
    global chosen_option
    chosen_option = dropdown_kasitoo.get()
    startDriverAndLogin()

    if chosen_option in vars.puit_map:
        crafting.kasitoo(driver, constants.TEGEVUS_PUIT, chosen_option, token=token)
    elif chosen_option in vars.tugi_map:
        crafting.kasitoo(driver, constants.TEGEVUS_TUGI, chosen_option, token=token)
    elif chosen_option in vars.ahi_map:
        crafting.kasitoo(driver, constants.TEGEVUS_AHI, chosen_option, token=token)


def getTabTitle():
    return tabControl.tab(tabControl.select(), 'text')


def saveCredButtonClicked():
    credentials_handler.saveCredentials(e1.get(), e2.get(), e3.get())
    notice_label['text'] = "Credentials saved!"


def getAllData():
    crafting_scraper.scrapeCraftingInfo(driver, close_after=False)
    tavern_scraper.scrapeTavernData(driver)
    disableButtons()


def getCraftingData():
    crafting_scraper.scrapeCraftingInfo(driver)
    disableButtons()


def getTavernData():
    tavern_scraper.scrapeTavernData(driver)
    disableButtons()


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
tabControl.grid(row=3, columnspan=3, pady=10, padx=10)


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

btn_get_all = Button(window, text='Get all Data', command=getAllData)
btn_get_all.grid(row=5, column=0, sticky=W, pady=10, padx=10)

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


dropdown_kasitoo = tk.StringVar()
dropdown_kasitoo.set(vars.item_names_kasitoo[0])
dropdown_menu_kasitoo = ttk.Combobox(tab2, textvariable=dropdown_kasitoo, values=data_kasitoo['item_names'], width=50)
dropdown_menu_kasitoo.grid(row=0, columnspan=3)

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

dropdown_joogimeister = tk.StringVar()
dropdown_joogimeister.set(data_joogid['item_names'][0])
dropdown_menu_joogimeister = ttk.Combobox(tab3, textvariable=dropdown_joogimeister, values=data_joogid['item_names'], width=50)
dropdown_menu_joogimeister.grid(row=0, columnspan=3)

btn1_jook = Button(tab3, text='Start', command=getSelectionJook)
btn1_jook.grid(row=2, column=0, pady=10, padx=10)
btn2_jook = Button(tab3, text='Change item (choose new item first from dropdown)', command=changeProcess)
btn2_jook.grid(row=2, column=1, pady=10, padx=10)
btn3_jook = Button(tab3, text='Stop', command=stopProcess)
btn3_jook.grid(row=3, columnspan=2, pady=10, padx=10)

#print(btn2_jook)
btn2_kasi['state'] = 'disabled'
btn3_kasi['state'] = 'disabled'
btn2_jook['state'] = 'disabled'
btn3_jook['state'] = 'disabled'

window.mainloop()