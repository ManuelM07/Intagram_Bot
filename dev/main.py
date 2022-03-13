from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
import time
import os
import random


PASSWORD = os.environ.get("PASSWORD")
USERNAME = os.environ.get("USERNAME")
SIMILAR_ACCOUNT = os.environ.get("SIMILAR_ACCOUNT")


BRAVE_PATH = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
option = webdriver.ChromeOptions()
option.binary_location = BRAVE_PATH
CHROME_DRIVER_PATH = "/Users/Manuel/Documents/apps_dev/chromedriver"


class InstaFollower:

    def __init__(self, driver_path, option):
        self.driver = webdriver.Chrome(executable_path=driver_path, options=option)
        self.start = 0
        self.count = 0
        self.start_modal = 0

    
    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/") # Se ingresa al login de instagram
        time.sleep(5+self.sleep())
        self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').click()


        action = ActionChains(self.driver)
        action.send_keys(USERNAME)
        action.perform()


        password = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input') 
        password.send_keys(PASSWORD)
        password.send_keys(Keys.ENTER)
        time.sleep(10+self.sleep())

        # Las siguiente 3 excepciones se crean debido a que se notó un patrón de cambio en los div del sitio web
        try: 
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/section/div/button').click()
        except:
            self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/section/main/div/div/div/section/div/button').click() #//*[@id="react-root"]/div/div/section/main/div/div/div/section/div/button
        time.sleep(5+self.sleep())

        try:
            self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div/div[3]/button[2]").click() #/html/body/div[5]/div/div/div/div[3]/button[2]
        except:
            self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]').click()

        time.sleep(10+self.sleep())
        try:
            source = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input') # //*[@id="react-root"]/div/div/section/nav/div[2]/div/div/div[2]/input
        except:
            source = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/section/nav/div[2]/div/div/div[2]/input')

        source.send_keys(SIMILAR_ACCOUNT)
        time.sleep(2+self.sleep())
        source.send_keys(Keys.ENTER)
        time.sleep(2)
        source.send_keys(Keys.ENTER)
        time.sleep(10+self.sleep())
        # En la siguiente excepción también se controla el cambio de los div
        try:
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/div').click() # //*[@id="react-root"]/div/div/section/main/div/header/section/ul/li[2]/a/div
        except:
            self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/section/main/div/header/section/ul/li[2]/a/div').click()
        time.sleep(10+self.sleep())



    def find_followers(self):
        """Esta función nos permite buscar las cuentas que deseamos seguir"""
        while True: #for _ in range(8+self.sleep()): #TODO # se cambia por while para que mueva el scroll la cantidad de veces que sea
            if self.count == 40:
                break 
            self.follow()
            self.driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div[2]/ul/div//a').send_keys(Keys.END) # Esta linea nos permite hacer scroll en el modal
            time.sleep(3+self.sleep())
            self.start += 1


    def follow(self):
        """Esta función permite seguir a las cuentas deseadas"""
        all_buttons = self.driver.find_elements_by_css_selector("li button") # Permite guardar todos los button de las cuentas que se encuentran en ese momento en el modal
        for i in range(self.start_modal, len(all_buttons)):
            self.start_modal += 1
            button_text = all_buttons[i].text # Se guarda el texto del boton
            print(button_text)
            # try:
            if button_text == "Seguir": # Se verifica que ese boton contenga la palabra (seguir or follow), esto con el fin de no tocar el boton de las personas que ya seguimos o que estan en pendiente por aceptar nuestra solicitud
                all_buttons[i].click() # Si se cumple lo anterior se presiona el boton
                time.sleep(3+self.sleep())
                self.count += 1
            #except ElementClickInterceptedException:
            #    cancel_button = self.driver.find_element_by_xpath('/html/body/div[7]/div/div/div/div[3]/button[2]') 
            #    cancel_button.click()
            #    time.sleep(2)
            #    self.count -= 1
            print(self.count)
            if self.count == 41:
                exit()        


    def sleep(self):
        """Esto función retorna un numero aleatorio entre 1 y 5, esto se hace con el fin de que las pausas
            siempre se hagan en tiempo aleatorio y no demuestren un patrón, de esta forma se bajan las probabilidades
            de que el algoritmo de Instagram descubra el uso del bot"""
        return random.randint(1, 5)
            


bot = InstaFollower(CHROME_DRIVER_PATH, option)
bot.login()
bot.find_followers()
#bot.follow()