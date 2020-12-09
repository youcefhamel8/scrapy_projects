import bs4
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import scrapy

"""class test_basic(scrapy.Spider):
	name="test"
	def open_file():

		filename ="res1.csv"
		f = open(filename, "w")
		entete = "date; name; desc; price\n"
		f.write(entete)
		return f


	def parcouir_enregistrer(f,first_url):

		# ouvrir une connexion avec bs4
		cnx = urlopen(first_url)

		# récuperer les données html de la page
		html_page = cnx.read()

		# fermer la connexion
		cnx.close()

		# parcourir le contenu de toute la page avec BS
		soup = BeautifulSoup(html_page, 'html.parser')

		# parcourir les cartes des annonces qui contiennent les attributs a récupérer a partir du contenu html
		data = soup.findAll("div",{"class":"annonce annonce_store"})

		# parcourir les elements de l'élement
		for element in data:
			
			if element.findAll("h2",{"itemprop":"name"}):
				name = element.findAll("h2")[0].text.strip()
			else:
				name = "null"
			
			if element.findAll("span",{"class":"annonce_get_description"}):
				surface = element.findAll("span",{"class":"annonce_get_description"})[0].text.split()
			else:
				surface = "null"
			
			if element.findAll("span",{"class":"annonce_prix"}):
				price = element.findAll("span",{"class":"annonce_prix"})[0].text.strip()
			else:
				price = "null"
			
			if element.findAll("p",{"class":"annonce_date"}):
				date = element.findAll("p",{"class":"annonce_date"})[0].text.strip()
			else:
				date = "null"

			print("date : "+date)
			print("lieu : "+name)
			print("desc : "+" ".join(str(x) for x in surface))
			print("prix : "+price)
			
			#f.write("date : "+date+" ;"+"lieu : "+name+" ;" +"desc : "+" ".join(str(x) for x in surface)+ " ;"+"prix : "+price +"\n")
			f.write("date : "+date+" ;" +"lieu : "+name+" ;" +"desc : "+" ".join(str(x).replace(';',' ') for x in surface)+ " ;"+"prix : "+price +"\n")
			
			print (len(data))

	def close_file(f):

		f.close()

	# time start
	timestart = datetime.datetime.now()

	# url
	initial_url = "https://www.ouedkniss.com/immobilier"
	first_url = "https://www.ouedkniss.com/immobilier/2"


	f = open_file()

	# in terminal get path with pwd|pbcopy
	browser = webdriver.Chrome('./chromedriver')

	browser.get(initial_url)
	parcouir_enregistrer(f,initial_url)
	#time.sleep(5)


	i=0
	while i != 0:
		# ouvrir une connexion avec selenium
		browser.get(first_url)

		if first_url:
			parcouir_enregistrer(f,first_url)
			i = i +1
		else:
			break

		#elem = browser.find_elements_by_xpath('//*[@id="divPages"]/a[2]')
		elem = browser.find_elements_by_class_name('page_arrow')
		#for link in elem:
			#print(link.get_attribute('href'))

		first_url = elem[1].get_attribute('href')

		print(first_url)
		#time.sleep(5)
		elem[1].click()


	close_file(f)
	timeend = datetime.datetime.now()

	dure = timeend - timestart
	print('duré : '+ str(dure))"""




