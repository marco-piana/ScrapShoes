import os
import uuid
import bs4
import numpy
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

        # Generare il primo oggetto parsato con il contenuto della prima pagina di categoria
        html_filename = "%s_%s_%d.html" % (self.filepart, self.categoriaID, 1)
        firstcategory_html = self.scrap_or_load(html_filename, self.url)

        # Salvo l'oggetto di BeautifulSoap relativo alla prima pagina di categoria
        soup = BeautifulSoup(firstcategory_html, "html.parser")
        self.pages.append(soup)

        # Ricavo il numero di pagine totali da questa prima pagina
        a_num_pages = self.pages[0].find_all("a", class_="page-numbers")
        span_num_pages = self.pages[0].find_all("span", class_="page-numbers")

        len_a = int(len(a_num_pages) / 2)
        len_span = int(len(span_num_pages) / 2)

        # Se entrambi sono diversi da zero vanno scrappate altre pagine altrimenti non faccio nulla
        if len_a != 0 and len_span != 0:

            # Se len_span 1 e len_a e 2 allora prendo a da 0 (2 pagine)
            if len_span == 1 and len_a == 2:
                self.num_pages = int(a_num_pages[0].text)

            # Se len_span 1 e len_a e 3 allora prendo a da 1 (3 pagine)
            if len_span == 1 and len_a == 3:
                self.num_pages = int(a_num_pages[1].text)

            # Se len_span 1 e len_a e 4 allora prendo a da 2 (4 pagine)
            if len_span == 1 and len_a == 4:
                self.num_pages = int(a_num_pages[2].text)

            # Se len_span 2 e len_a e 4 allora prendo a da 2 (5 o piu pagine)
            if len_span == 2 and len_a == 4:
                self.num_pages = int(a_num_pages[2].text)

            # Per ogni altra pagina di categoria
            for i in range(2, self.num_pages + 1):
                html_filename = "%s_%s_%d.html" % (self.filepart, self.categoriaID, i)
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

    def print_product_urls(self):
        for url in self.products_urls:
            print(url)

    def scrap_products_urls(self):
        for page in self.pages:

            # TODO: riconoscere meglio la parte di codice contente i dati da estrarre dei prodotti
            txt_content = str(page.findAll("script", {'type': 'text/template'})[2].text)
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


class PageProduct:

    def __init__(self, filepath, url, id):
        self.urls_images = list()
        self.title = ""
        self.price = ""
        self.cod = ""
        self.categories = list()
        self.tags = list()
        self.main_image_url = ""
        self.images_urls = list()
        self.descrizione = ""
        self.additionals = ""
        self.additional_dict = {}

        self.page = ""
        self.filepath = filepath
        self.url = url
        self.id = id if id != "" else uuid.uuid4

        self.html_filename = "%s_%s.html" % (self.filepart, self.id)

        firstcategory_html = self.scrap_or_load(self.html_filename, self.url)
        self.page = BeautifulSoup(firstcategory_html, "html.parser")

        self.scrap_product()

    def scrap_or_load(self, html_filename, url):
        html_filepath = "%s%s" % (self.filepath, html_filename)
        if os.path.isfile(html_filepath):
            catfile = io.open(html_filepath, mode="r", encoding="UTF-8")
            return catfile.read()
        else:
            html_text = requests.get(url).text
            self.save_page(html_filename, html_text)
            return html_text

    def save_page(self, html_filename, html_text):
        f = open("%s%s" % (self.filepath, html_filename), "w", encoding="UTF-8")
        f.write(html_text)
        f.close()

    def scrap_product(self):
        pass

    def get_csv(self):

        fields = dict()
        fields["Titolo"] = self.title.strip()
        fields["COD"] = self.cod.strip()
        fields["Categorie"] = ','.join(f'\"{x}\"' for x in self.categories)
        fields["Tags"] = ','.join(f'\"{x}\"' for x in self.tags)
        fields["Prezzo"] = self.price.strip()
        fields["Immagine Principale"] = self.main_image_url.strip()
        fields["Immagini Secondarie"] = ','.join(f'\"{x}\"' for x in self.images_urls)
        fields["Descrizione HTML"] = self.descrizione

        for key in self.additional_dict.keys():
            fields[key] = self.additional_dict[key].strip()

        return fields


class Accessorio(PageProduct):
    filepart = "accessorio"

    def scrap_product(self):

        # TODO: riconoscere meglio la parte di codice contente i dati da estrarre dei prodotti
        obj = self.page.findAll("script", {'type': 'text/template'})

        txt_content = ""
        a = 0
        for sc in obj:
            try:
                if sc['id'] == None:
                    pass
            except:
                txt_content = obj[a].text
            a += 1

        txt_content = txt_content.replace("\\n\\t", "")
        txt_content = txt_content.replace("\\t\\t\\t\\t", "")
        txt_content = txt_content.replace("\\t\\t", "")
        txt_content = txt_content.replace("\\t", "")
        txt_content = txt_content.replace("\\n", "")
        txt_content = txt_content.replace("\\/", "/")
        txt_content = txt_content.replace("\\\"", "\"")
        # TODO: capire come mai nell'estrazione sono errati i caratteri Unicode
        txt_content = txt_content.replace("\\u00aa", u"\u00aa")
        txt_content = txt_content.replace("\\u1d2c", u"\u1d2c")
        txt_content = txt_content.replace("\\u00e0", u"\u00e0")
        txt_content = txt_content[1:-1]

        soup = BeautifulSoup(txt_content, "html.parser")
        try:
            # Titolo
            self.title = soup.find_all("h2", {"class": "product_title"})[0].text

            # Codice
            self.cod = soup.find_all("span", {"class": "sku"})[0].text

            # Categorie
            categorie = soup.find("span", {"class": "posted_in"}).findChildren("a", recursive=False)
            for categoria in categorie:
                self.categories.append(categoria.text)

            # Tags
            tags = soup.find("span", {"class": "tagged_as"}).findChildren("a", recursive=False)
            for tag in tags:
                self.tags.append(tag.text)

            # Prezzo
            self.price = soup.find("span", {"class": "woocommerce-Price-amount"}).bdi.text

            # Immagini
            self.main_image_url = soup.find("img", {"class": "woocommerce-main-image"})["src"]
            images_url = soup.find_all("img", {"class": "img-responsive"})
            for i in range(0, int(len(images_url) / 2)):
                self.images_urls.append(images_url[i]["src"])

            # Descrizione
            description = soup.find("div", {"id": "tab-description"})
            description.attrs = {}
            for tag in description.descendants:
                if isinstance(tag, bs4.element.Tag):
                    tag.attrs = {}
            self.descrizione = description

            # Informazioni aggiuntive
            self.additionals = soup.find("table", {"class": "woocommerce-product-attributes"})
            self.additionals = self.additionals.find_all("tr")

            for tr in self.additionals:
                self.additional_dict[tr.th.text] = tr.td.p.text
        except:
            print("Problema nella lettura delle informazioni nel file %s: " % self.html_filename)


class Donna(PageProduct):
    filepart = "donna"

    def scrap_product(self):

        # TODO: riconoscere meglio la parte di codice contente i dati da estrarre dei prodotti
        obj = self.page.findAll("script", {'type': 'text/template'})

        txt_content = ""
        a = 0
        for sc in obj:
            try:
                if sc['id'] == None:
                    pass
            except:
                txt_content = obj[a].text
            a += 1

        txt_content = txt_content.replace("\\n\\t", "")
        txt_content = txt_content.replace("\\t\\t\\t\\t", "")
        txt_content = txt_content.replace("\\t\\t", "")
        txt_content = txt_content.replace("\\t", "")
        txt_content = txt_content.replace("\\n", "")
        txt_content = txt_content.replace("\\/", "/")
        txt_content = txt_content.replace("\\\\/", "/")
        txt_content = txt_content.replace("\\\"", "\"")
        # TODO: capire come mai nell'estrazione sono errati i caratteri Unicode
        txt_content = txt_content.replace("\\u00aa", u"\u00aa")
        txt_content = txt_content.replace("\\u00a0", u"\u00a0")
        txt_content = txt_content.replace("\\u1d2c", u"\u1d2c")
        txt_content = txt_content.replace("\\u00e0", u"\u00e0")
        txt_content = txt_content[1:-1]

        soup = BeautifulSoup(txt_content, "html.parser")
        try:
            # Titolo
            self.title = soup.find_all("h2", {"class": "product_title"})[0].text

            # Codice
            self.cod = soup.find_all("span", {"class": "sku"})[0].text

            # Categorie
            categorie = soup.find("span", {"class": "posted_in"}).findChildren("a", recursive=False)
            for categoria in categorie:
                self.categories.append(categoria.text)

            # Tags
            tags = soup.find("span", {"class": "tagged_as"}).findChildren("a", recursive=False)
            for tag in tags:
                self.tags.append(tag.text)

            # Prezzo
            self.price = soup.find("span", {"class": "woocommerce-Price-amount"}).bdi.text

            # Immagini
            self.main_image_url = ""
            images_url = soup.find_all("img", {"loading": "lazy"})
            for i in range(0, len(images_url)):
                self.images_urls.append(images_url[i]["src"])

            # Descrizione
            description = soup.find("div", {"id": "tab-description"})
            description.attrs = {}
            for tag in description.descendants:
                if isinstance(tag, bs4.element.Tag):
                    tag.attrs = {}
            self.descrizione = description

            # Informazioni aggiuntive
            self.additionals = soup.find("table", {"class": "woocommerce-product-attributes"})
            self.additionals = self.additionals.find_all("tr")

            for tr in self.additionals:
                self.additional_dict[tr.th.text] = tr.td.p.text
        except:
            raise


class Uomo(PageProduct):
    filepart = "uomo"

    def scrap_product(self):

        # TODO: riconoscere meglio la parte di codice contente i dati da estrarre dei prodotti
        obj = self.page.findAll("script", {'type': 'text/template'})

        txt_content = ""
        a = 0
        for sc in obj:
            try:
                if sc['id'] == None:
                    pass
            except:
                txt_content = obj[a].text
            a += 1

        txt_content = txt_content.replace("\\n\\t", "")
        txt_content = txt_content.replace("\\t\\t\\t\\t", "")
        txt_content = txt_content.replace("\\t\\t", "")
        txt_content = txt_content.replace("\\t", "")
        txt_content = txt_content.replace("\\n", "")
        txt_content = txt_content.replace("\\/", "/")
        txt_content = txt_content.replace("\\\\/", "/")
        txt_content = txt_content.replace("\\\"", "\"")
        # TODO: capire come mai nell'estrazione sono errati i caratteri Unicode
        txt_content = txt_content.replace("\\u00aa", u"\u00aa")
        txt_content = txt_content.replace("\\u1d2c", u"\u1d2c")
        txt_content = txt_content.replace("\\u00e0", u"\u00e0")
        txt_content = txt_content[1:-1]

        soup = BeautifulSoup(txt_content, "html.parser")
        try:
            # Titolo
            self.title = soup.find_all("h2", {"class": "product_title"})[0].text

            # Codice
            self.cod = soup.find_all("span", {"class": "sku"})[0].text

            # Categorie
            categorie = soup.find("span", {"class": "posted_in"}).findChildren("a", recursive=False)
            for categoria in categorie:
                self.categories.append(categoria.text)

            # Tags
            tags = soup.find("span", {"class": "tagged_as"}).findChildren("a", recursive=False)
            for tag in tags:
                self.tags.append(tag.text)

            # Prezzo
            self.price = soup.find("span", {"class": "woocommerce-Price-amount"}).bdi.text

            # Immagini
            self.main_image_url = ""
            images_url = soup.find_all("img", {"loading": "lazy"})
            for i in range(0, len(images_url)):
                self.images_urls.append(images_url[i]["src"])

            # Descrizione
            description = soup.find("div", {"id": "tab-description"})
            try:
                description.attrs = {}
                for tag in description.descendants:
                    if isinstance(tag, bs4.element.Tag):
                        tag.attrs = {}
                self.descrizione = description
            except:
                self.descrizione = ""

            # Informazioni aggiuntive
            self.additionals = soup.find("table", {"class": "woocommerce-product-attributes"})
            self.additionals = self.additionals.find_all("tr")

            for tr in self.additionals:
                self.additional_dict[tr.th.text] = tr.td.p.text
        except:
            raise


class Bambino(PageProduct):
    filepart = "bambino"

    def scrap_product(self):

        # TODO: riconoscere meglio la parte di codice contente i dati da estrarre dei prodotti
        obj = self.page.findAll("script", {'type': 'text/template'})

        txt_content = ""
        a = 0
        for sc in obj:
            try:
                if sc['id'] == None:
                    pass
            except:
                txt_content = obj[a].text
            a += 1

        txt_content = txt_content.replace("\\n\\t", "")
        txt_content = txt_content.replace("\\t\\t\\t\\t", "")
        txt_content = txt_content.replace("\\t\\t", "")
        txt_content = txt_content.replace("\\t", "")
        txt_content = txt_content.replace("\\n", "")
        txt_content = txt_content.replace("\\/", "/")
        txt_content = txt_content.replace("\\\\/", "/")
        txt_content = txt_content.replace("\\\"", "\"")
        # TODO: capire come mai nell'estrazione sono errati i caratteri Unicode
        txt_content = txt_content.replace("\\u00aa", u"\u00aa")
        txt_content = txt_content.replace("\\u00a0", u"\u00a0")
        txt_content = txt_content.replace("\\u1d2c", u"\u1d2c")
        txt_content = txt_content.replace("\\u00e0", u"\u00e0")
        txt_content = txt_content[1:-1]

        soup = BeautifulSoup(txt_content, "html.parser")
        try:
            # Titolo
            self.title = soup.find_all("h2", {"class": "product_title"})[0].text

            # Codice
            self.cod = soup.find_all("span", {"class": "sku"})[0].text

            # Categorie
            categorie = soup.find("span", {"class": "posted_in"}).findChildren("a", recursive=False)
            for categoria in categorie:
                self.categories.append(categoria.text)

            # Tags
            tags = soup.find("span", {"class": "tagged_as"}).findChildren("a", recursive=False)
            for tag in tags:
                self.tags.append(tag.text)

            # Prezzo
            self.price = soup.find("span", {"class": "woocommerce-Price-amount"}).bdi.text

            # Immagini
            self.main_image_url = ""
            images_url = soup.find_all("img", {"loading": "lazy"})
            for i in range(0, len(images_url)):
                self.images_urls.append(images_url[i]["src"])

            # Descrizione
            description = soup.find("div", {"id": "tab-description"})
            for tag in description.descendants:
                if isinstance(tag, bs4.element.Tag):
                    tag.attrs = {}
            description.attrs = {}
            self.descrizione = description

            # Informazioni aggiuntive
            self.additionals = soup.find("table", {"class": "woocommerce-product-attributes"})
            self.additionals = self.additionals.find_all("tr")

            for tr in self.additionals:
                self.additional_dict[tr.th.text] = tr.td.p.text
        except:
            raise


# Lista di Shoe
shoes = []

def scrap():
    # Urls delle categorie da dove estrarre i singoli articoli
    categorie_urls = [
        [Donna, "https://scarpesp.com/categoria-prodotto/donna/?count=36&paged="],
        [Uomo, "https://scarpesp.com/categoria-prodotto/uomo/?count=36&paged="],
        [Bambino, "https://scarpesp.com/categoria-prodotto/bambino/?count=36&paged="],
        [Accessorio, "https://scarpesp.com/categoria-prodotto/accessori/?count=36&paged="],
    ]

    start_time = time.time()
    scrapped_files = []
    # html_filepath = "C:\\Users\\davide\\PycharmProjects\\ScrapShoes\\src\\"
    html_filepath = "/home/shoes/public_html/www/scrap/"

    # Per ogni categoria di scarpesp.com della lista
    for cat_url in categorie_urls:
        # Estraggo da tutte le pagine della categoria l'elenco delle URL dei prodotti esistenti
        category_instance = PageCategory(html_filepath, cat_url[1], cat_url[0].__name__)
        category_instance.scrap_products_urls()
        product_urls = category_instance.products_urls
        #print("Sono stati estratti %d URL di Prodotti dalla categoria %s" % (len(product_urls), category_instance.url))

        headers = ""
        product_objects = list()
        for i in range(0, len(product_urls)):
            try:
                product_instance = cat_url[0](html_filepath, product_urls[i], i)
                product_objects.append(product_instance)
            except:
                # print(i)
                raise
                # print("IMPOSSIBILE ACQUISIRE DATI DA %s" % p.html_filename)

        keys = dict()
        for product in product_objects:
            for key in product.get_csv().keys():
                try:
                    keys[key] = keys[key] + 1
                except KeyError as e:
                    keys[key] = 1

        headers = keys.keys()
        # for key in headers:
        #     print("%s: %s" % (key, keys[key]))
        # print(keys.keys())

        rows = list()
        for product in product_objects:
            l = list()
            for key in keys.keys():
                try:
                    l.append(product.get_csv()[key])
                except KeyError as e:
                    continue
                except:
                    raise
            rows.append('|'.join(f'{x}' for x in l))

        try:
            filecsv = '%s%s.csv' % (html_filepath, cat_url[0].__name__)
            numpy.savetxt(filecsv, rows,
                          header='|'.join(x for x in headers), delimiter="|", fmt='% s', encoding="utf-8")
            #print("------ Scritto il file %s" % filecsv)
        except:
            raise

        scrapped_files.append('%s.csv' % cat_url[0].__name__)
    end_time = time.time()
    elapsed_time = end_time - start_time
    #print("Elapsed time: ", elapsed_time)


def application(environ, start_response):
    status = '200 OK'
    request_method = environ['REQUEST_METHOD']
    apiRichiesta = str(environ['QUERY_STRING'])
    if request_method == 'GET':
    #if True:
        # Distinguere in base al parametro la chiamata la funzione
        if apiRichiesta == "type=scrap":
            output = scrap()
        else:
            output = "0x10: Comando GET non accettato."

    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(output))),
        ('Access-Control-Allow-Origin', '*')
    ]
    start_response(status, response_headers)
    return [output]
