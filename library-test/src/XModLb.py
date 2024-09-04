# -- > Author : Rizky Nurahman
# -- > Script Created In, 23-Oktober-2023


# -- Module

import os
import sys
import time
import requests
from bs4 import BeautifulSoup as bs


# -- Color

BLACK 			= "\033[0;30m"
RED 			= "\033[0;31m"
GREEN 			= "\033[0;32m"
BROWN 			= "\033[0;33m"
BLUE 			= "\033[0;34m"
PURPLE 			= "\033[0;35m"
CYAN 			= "\033[0;36m"
LIGHT_GRAY 		= "\033[0;37m"
DARK_GRAY 		= "\033[1;30m"
LIGHT_RED 		= "\033[1;31m"
LIGHT_GREEN 	= "\033[1;32m"
YELLOW 			= "\033[1;33m"
LIGHT_BLUE 		= "\033[1;34m"
LIGHT_PURPLE 	= "\033[1;35m"
LIGHT_CYAN 		= "\033[1;36m"
LIGHT_WHITE 	= "\033[1;37m"


# -- > font style

BOLD 			= "\033[1m"
FAINT 			= "\033[2m"
ITALIC 			= "\033[3m"
UNDERLINE 		= "\033[4m"
BLINK 			= "\033[5m"
NEGATIVE 		= "\033[7m"
CROSSED 		= "\033[9m"
END 			= "\033[0m"


# -- > Funtion Clear

def clear():
	if 'win' in sys.platform.lower():
		os.system('cls')
	else:
		os.system('clear')


# -- > Printer Succes

def Succes(teks):
	print('%s%s%s%s%s'%(LIGHT_GREEN, BLINK, ITALIC, teks, END))


# -- > Printer Failled

def Failled(teks):
	print('%s%s%s%s%s'%(LIGHT_RED, BLINK, ITALIC, teks, END))


# -- > Printer Writing

def Writing(teks,color):
	if 'a' in color:
		color = RED
	elif 'b' in color:
			color = YELLOW
	elif 'c' in color:
			color = GREEN
	for i in teks:
		sys.stdout.write('%s%s%s'%(color,i,END))
		sys.stdout.flush()
		time.sleep(0.1)
	print('')


# -- > Function Scraping Non Cookie

def Scrapt(url):
	try:
		get = bs(requests.get(url).text, 'html.parser')
		return get
	except Exception as e:
		print(e)


# -- > Function Scraping With Cookie

def Scraping(url,cookie):
	try:
		get = bs(requests.get(url, cookies={'cookie':cookie}).text, 'html.parser')
		return get
	except Exception as e:
		print(e)

