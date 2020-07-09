
#Libreria necesarias
import os 
import datetime
import paho.mqtt.publish as publish
from gtts import gTTS
import random 
import calendar
import re
import webbrowser
import smtplib
import requests
from pyowm import OWM
#import youtube_dl
#import vlc
import urllib
import json
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

class AssistenPython(object):
	"""docstring for AssistenPython"""
	def __init__(self, name):
		self.name = name

    #Compara si la frase dicha es el comienzo de una orden
	def wakeWord(self,text):
		wake_word = ['hola computador','okay computador'] #Palabras para desperatar el computador
		text = text.lower()

		for phrase in wake_word: #Busca la palabra
			if phrase in text:
				return True

		return False 
	#Retorna el dia en que se encuentra(texto)
	def getDate(self):
		now = datetime.datetime.now()
		my_date = datetime.datetime.today()
		weekday = calendar.day_name[my_date.weekday()]
		monthNum = now.month
		dayNum = now.day

		#Lista de meses
		month_names = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio"
		               ,"Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

		translate  = {'Monday':'lunes','Tuesday':'martes','Wednesday':'miercoles','Thursday':'jueves',
		               'Friday':'viernes','Saturday':'sabado','Sunday':'domingo'}

		return 'Hoy es '+f'{translate[weekday]}'+ ','+f'{dayNum}'+" "+"de"+" "+ f'{month_names[monthNum-1]}'+'.'

	#Funcion que da una respuesta aleatoria
	def greeting(self,text):

		greting_response = ['Hola','Holi'] #Respuestas 

		greeting_inputs = ['hola','hey']

		for word in text.split():
			if word.lower() in greeting_inputs:
				return random.choice(greting_response)+'.'

		return ''
    #Funcion que permite interactuar con dispositivos MQTT
	def actions(self,text):

		possible_inputs = ['lampara','apagar','encender']
	

		if possible_inputs[0] in text and possible_inputs[1] in text:
			publish.single("esp/helios/iluminacion",
				"F",
				 qos=0,
				 retain=False,
				 hostname="54.227.205.125",
				 port=10515,
				 client_id="",
				 keepalive=60,
				 will=None,
				 auth={'username':"placa1", 'password':"12345678"}, tls=None,
				 )
			return 'lámpara apagada'
		elif possible_inputs[0] in text and possible_inputs[2] in text:
			    publish.single("esp/helios/iluminacion",
				"N",
				 qos=0,
				 retain=False,
				 hostname="54.227.205.125",
				 port=10515,
				 client_id="",
				 keepalive=60,
				 will=None,
				 auth={'username':"placa1", 'password':"12345678"}, tls=None,
				 )
			    return 'lámpara encendida'
		return ''
	#Busca una pagina en el buscador
	def search_pag(self,text):
		if 'abrir' in text.lower():
			reg_ex = re.search('abrir (.+)', text.lower()) #Bsuca caracteres despues de "abrir"
			if reg_ex:
			  domain = reg_ex.group(1)
			  print(domain)
			  url = 'https://www.' + domain + '.com'
			  webbrowser.open(url)  #Abre el buscador
			  return 'Abriendo buscador'
		else:
			return ''
    #Funcion que da el clima en una ciudad
	def current_whether(self,text):
		if 'clima en ' in text.lower():
			
			reg_ex = re.search('Clima en (.*)', text)

		

			if reg_ex:
				translate = {'Mist':'Neblado','Clouds':'Nubes','wednesaday':'miercoles','Thursday':'jueves',
		                     'Friday':'viernes','Saturday':'sabado','Sunday':'domingo'} #Traducir el clima
				city = reg_ex.group(1) #Extrae la ciudad
				print(city)
				owm = OWM('7992ea246848a4714f069cfd46aaaf17') #Clave para acceder ak servidor
				obs = owm.weather_at_place(city) # Clima de la ciudad
				w = obs.get_weather()
				k = w.get_status() #Clima
				x = w.get_temperature(unit='celsius') #Temperatura
				x_min = x['temp_min']
				x_max = x['temp_max']
				wether =  (f'El clima actual en {city} es {translate[k]}. El máximo de temperatura es {x_max} grados celcius y el minimo de temperatura es {x_min} grados celcius')
				return wether
		else:
			return ''
     #Funcion que da las noticias del dia en Colombia
	def news_today(self,text):
		news  = [] #Lista de noticias

		if 'noticias del día' or 'noticias del dia'  in text.lower():

			try:
			 news_url="https://news.google.com/rss?hl=es-419&gl=CO&ceid=CO:es-419" #Url de la pagina de google de noticias en Colombia
			 Client=urlopen(news_url) 
			 xml_page=Client.read()
			 Client.close()
			 soup_page=soup(xml_page,"html5lib") #Extaer el texto plano
			 tags =soup_page.findAll("title") # Busca la etiqueta title en el texto

			 

			 for tag in tags:
			 	#print(tag.getText()) #Ciclo da las noticias importantes
			 	news.append(tag.getText()) #Agrega las notcias a una lista

			 return('Algunas noticias del día son:'+ news[1] +','+ news[3] +','+ news[4] +','+ news[5]+'.')

			except :
				print('Hubo un error en la busqueda')

				return 'Hubo un error en la busqueda'
		else:
			return ''



				
		       