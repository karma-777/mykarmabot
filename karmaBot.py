import telebot
import time
from aules_info import deberes
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import  By
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
import random

TOKEN = '1085604387:AAHgNdTdnbS-pJNsc_NCtYpxa6UDbEAobM0'
bot = telebot.TeleBot(TOKEN)

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chatid = message.chat.id
    nombreUser = message.chat.first_name + " " + message.chat.last_name
    saludo = "Hola {nombre}, Bienvenido a KaRmAbot"
    bot.send_message(chatid, saludo.format(nombre=nombreUser))
    #bot.reply_to(message, "Bienvenido a K_armaBot\nEsto es un Bot de prueba de Kirill")

@bot.message_handler(commands=['aules'])
def send_deberes(message):
    driver = webdriver.Chrome(executable_path='C:\WebDriver\chromedriver.exe')
    driver.get('https://aules.edu.gva.es/fp/calendar/view.php')

    # Parte de autorización
    username = '10962199'
    password = 'zhi220500'
    input_user = driver.find_element(By.XPATH, '//input[@id="username"]')
    input_pass = driver.find_element(By.XPATH, '//input[@id="password"]')
    boton = driver.find_element(By.XPATH, '//button[@id="loginbtn"]')

    input_user.send_keys(username)
    input_pass.send_keys(password)
    boton.click()
    sleep(random.randint(1, 3))

    # Parte de extracción
    a = []
    b = []
    titulos = driver.find_elements(By.XPATH, '//h3[@class="name d-inline-block"]')
    acceso_tiempos = driver.find_elements(By.XPATH,'//div[@class="description card-body"]/div[@class="row"]/div[@class="col-11"]/a')

    for x in titulos:
        a.append(x.text)
    for y in acceso_tiempos:
        b.append(y.text)

    frame_data = {'Titulo': a, 'Tiempo': b}
    df = pd.DataFrame(frame_data)

    sleep(1)
    driver.quit()
    driver.quit()


    chatid = message.chat.id
    nombreUser = message.chat.first_name + " " + message.chat.last_name
    resultado = df
    deberes = "{} los deberes que hay son:\n" + str(resultado)
    bot.send_message(chatid, deberes.format(nombreUser))

print("Ejecutando")
bot.polling()
