import os
import urllib.parse
from array import array

import requests
from bs4 import BeautifulSoup
import io
import time


class PageCategory:
    filepart = "category_page"

    def __init__(self, filespath, url, categoryID):
        self.filespath = filespath
        self.url = url
        self.categoriaID = categoryID
        self.pages = list()
        self.products_urls = list()
        self.products = list() # TODO: in memory list of products
        self.url_pages = []  # TODO: generate category pages url
        self.filenames = []  # TODO: disk file category list

        # Generare il primo oggetto parsato con il contenuto della prima pagina di categoria
        html_filename = "%s_%d_%d.html" % (self.filepart, self.categoriaID, 1)
        firstcategory_html = self.scrap_or_load(html_filename, self.url)

        # Salvo l'oggetto di BeautifulSoap relativo alla prima pagina di categoria
        soup = BeautifulSoup(firstcategory_html, "html.parser")
        self.pages.append(soup)

        # Ricavo il numero di pagine totali da questa prima pagina
        self.num_pages = int(len(self.pages[0].find_all("a", class_="page-numbers")) / 2)

        # Per ogni altra pagina di categoria
        for i in range(2, self.num_pages+1):
            html_filename = "%s_%d_%d.html" % (self.filepart, self.categoriaID, i)
            category_html = self.scrap_or_load(html_filename, self.url, i)
            soup = BeautifulSoup(category_html, "html.parser")
            self.pages.append(soup)


    # Recupera da Internet il file se non presente su disco nella cartella di archivio
    def scrap_or_load(self, html_filename, scrap_url, page=1):
        html_filepath = "%s%s" % (self.filespath, html_filename)
        if os.path.isfile(html_filepath):
            catfile = io.open(html_filepath, mode="r")
            return catfile.read()
        else:
            html_text = self.scrap_category_page(scrap_url, page)
            self.save_categorypage(html_filename, html_text)
            return html_text

    # Restituisce il testo della pagina recuperata da internet
    def scrap_page(self, url):
        return requests.get(url).text

    # Ritorna il testo HTML di una pagina scrappata di tipo categoria
    def scrap_category_page(self, seed_url, page_number=1):
        # "https://scarpesp.com/categoria-prodotto/donna/?count=36&paged="
        formatted_url = "%s%d" % (seed_url, page_number)
        return self.scrap_page(formatted_url)

    def scrap_fist_page(self):
        ### Scarico la prima pagina di categoria
        return self.scrap_category_page(self.url)

    def save_categorypage(self, html_filename, html_cat_text):
        f = open("%s%s" % (self.filespath, html_filename), "w")
        f.write(html_cat_text)
        f.close()

    def get_products_urls(self):

        txt_content = str(self.pages[0].findAll("script", {'type': 'text/template'})[2].text)
        txt_content = txt_content.replace("\\t\\t\\n", "")
        txt_content = txt_content.replace("\\n\\t\\n\\t", "")
        txt_content = txt_content.replace("\\n", "")
        txt_content = txt_content.replace("\\t\\t", "")
        txt_content = txt_content.replace("\\t", "")
        txt_content = txt_content.replace("\\/", "/")
        txt_content = txt_content.replace("\\\\/", "/")
        txt_content = txt_content.replace("\\\"", "\"")

        soup = BeautifulSoup(txt_content, "html.parser")
        products_html = soup.find_all("li", "product-col")
        for product_li in products_html:
            self.products_urls.append(product_li.a['href'])




# Singolo prodotto
class Shoe:
    def __init__(self):
        self.url = ""
        self.urls_images = []
        self.title = ""
        self.price = ""
        self.cod = ""
        self.categories = []
        self.tags = []


# Lista di Shoe
shoes = []

# Urls delle categorie da dove estrarre i singoli articoli
categorie_urls = [
    "https://scarpesp.com/categoria-prodotto/donna/?count=36&paged=",
]

# Indice della categorie
categorie_index = 0
page_index = 1

if __name__ == "__main__":
    start_time = time.time()



    html_filepath = "C:\\Users\\davide\\PycharmProjects\\ScrapShoes\\src\\"
    c = PageCategory(html_filepath, categorie_urls[0], 0)
    c.get_products_urls()



    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Elapsed time: ", elapsed_time)

    # shoes = soup_page.find_all("li", class_="product-col")


    ### Ricavo la lista delle URL di ogni articolo presente nella pagina
    ### Per ogni articolo presente nella lista degli articoli
    ### Creo il nuovo articolo Shoe e recupero i dati possibili
    ### Carico la pagina specifica dell'articolo
    ### Estraggo i dati mancanti dalla pagina specifica
    ### Aggiungo l'articolo alla lista totale degli articoli
    ### Trasformo in csv la lista totale deglli articoli
