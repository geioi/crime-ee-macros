# Crime.ee macros (still WIP)

This is a fairly simple auto clicker i've made for a browser-based game Crime using Selenium library, since i wanted to reduce the 
chance of me getting a carpal tunnel and retain the lifespan of my mouse.  
This is still a work in progress and is slowly being developed when the developer has the time for it

# 

## External libraries used
* Selenium
* PIL
* requests
* anticaptchaofficial
* tkinter
* cryptography

## Pictures

Crafting             |  Barkeeping          |  Blacksmithing
:-------------------------:|:-------------------------:|:-------------------------:
![](https://user-images.githubusercontent.com/16280237/88703312-357b1a80-d115-11ea-8f15-a5d5962f6132.png)   | ![](https://user-images.githubusercontent.com/16280237/88703412-58a5ca00-d115-11ea-9ec1-573cb76f68c4.png) |  ![](https://user-images.githubusercontent.com/16280237/88703497-6eb38a80-d115-11ea-99ad-7848269bc776.png)



## Working features 
### General  
* Finally a GUI!
* Password and API token encryption 
    * Just for the hell of it since these things are saved only locally anyway
    * secret key folder and file generation which is used to encrypt and decrypt (generated when user saves the credentials)
* Ability to save user credentials which to log in with
    * Password and API characters are hidden
    * Password is encrypted using secret key
* Dropdown lists of items available with levels and materials required for each skill
* Ability to change makeable item (or skill) on the fly, without having to close the browser window 
* Ability to kill the window with the control area without stopping the program
* Ability to quickly gather skill information (levels, needed materials, base ingredients etc.) in case of game updates (The most up to date ones are included with the repository already in data folder)
* In case of a level-up in skill - option to automatically move up to the next makeable item if the level allows
* Program uses paid captcha solving API (Anti-Captcha) to solve the 3-digit captcha that is thrown at you from time-to-time to prove that human being is playing (hehehe)

### Crafting
* Making chosen items
* Restocking the materials that are required for the current item that is being made
* Nothing else, really. This skill was the first and probably the easiest to develop macro for

### Barkeeping
* Making chosen drinks
* restocking on base ingredients and juices depending on the current allowed max amount
* Making alcohol if the drink requires it as one of the ingredients
* Emptying wares to make room for new ingredients


### Blacksmithing  
* Forging chosen weapons 
* Ability to choose how many weapons to make at once 
* Restock on required raw material, which is made with crafting, in case it runs out (restocking in crafting section works through crafting interface, if needed)
* Ability to enter the amount of raw material to be made if it runs out

### Herbalism (on hold until chemistry is ready)
* Ability to make med-kits, given that the needed ingredients exist

### Chemistry (planned to be developed next)
*

##

## TODO's/Known bugs 
### General  
* Add an ability to change the click intervals in GUI as some PCs might perform slower so higher intervals could fix that (current default is 0.1 seconds)
* Add an ability to change the max error count per session, as depending on the click interval the element might not reload fast enough after click, throwing exception. Depending on the task and click interval, the max error count might fill up faster or slower (current max default is 1000)
* Provide support for multiple captcha solving APIs (currently available API support is only for Anti-Captcha) AND/OR maybe construct and train a CNN model (god help me if it comes to that...)
* Maybe add a checkbox if user is VIP member or not as currently it assumes that the user is VIP and ignores the 0.5 minimum click interval and 360 moves/5 minutes for regular users (could also be fixed with the click interval changing)

### Crafting
* Add an ability to change the amount that is used to resupply materials (current default is 150 times, or 12500 pieces of material)

### Barkeeping
* Add the option to empty wares on new program startup before starting to make new drinks to maximize warehouse storage efficiently, currently only does this when level is gained and automatically moving to next drink is allowed
* Fix the case if the drink uses two different juices as its materials (only a single case - level 99 drink)


### Blacksmithing  
* Make the amount of items made at once to dropdown, as max 10 items is allowed anyway, not much point having to type it in

### Herbalism
* Make the material crafting automatic in case the user runs out of them (plant harvesting every 2 hours - maybe set a timer?)

### Chemistry
* General skill flow
    * Stealing plants from the garden 
    * Pressing juice out of the stolen plants
    * Purchasing narcotics from the streets
    * Combining purchased narcotics and pressed juices to make a new narcotic
    * Sell the new product on streets
    * repeat
* Check stolen bank items if they are found when stealing plants (maybe set amount threshold when to check, to save time)
* Improve the backpack size if the infamy allows that
* Travel to cities/countries with best buy/sell prices (if we want to be extra fancy with this skill)
* Buy juices from market if user runs out of tickets to steal plants with

### Misc
* Try to develop ways to train all available skills (would need to set a lot of timers) - in the FAR FAR future, and a HUGE maybe

##