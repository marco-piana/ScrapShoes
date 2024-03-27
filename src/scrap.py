import requests
from bs4 import BeautifulSoup
import io


class Shoe:
    def __init__(self):
        self.urls_images = []
        self.title = ""
        self.price = ""
        self.cod = ""
        self.categories = []
        self.tags = []


def browse_page(seed_url, page_number=1):
    #"https://scarpesp.com/categoria-prodotto/donna/?count=36&paged="
    formatted_url = "%s%d" % (seed_url, page_number)
    return requests.get(formatted_url).text


if __name__ == "__main__":



    seedurl = "https://scarpesp.com/categoria-prodotto/donna/?count=36&paged="
    html_text = io.open("C:\\Users\\davide\\PycharmProjects\\ScrapShoes\\src\\page_list.html", mode="r", encoding="utf-8")
    #html_text = browse_page(seedurl)

    soup = BeautifulSoup(html_text, "html.parser")
    print(soup.head.title)

    shoes = soup.find_all("li", class_="product-col")
    pages = soup.find_all("a", class_="page-numbers")
    print(len(shoes))
    print(len(pages))
    print(pages[len(pages)-2].text)
    # print("List Items:")
    # for item in shoes:
    #     print("- " + item.text)

    ### Per ogni pagina di categoria nella lista
        ### Scarico la pagina di categoria
        ### Ricavo il numero di pagine totali da questa prima pagina
        ### Per ogni pagina ulteriore a partire da quella già scaricata
            ### Ricavo la lista delle URL di ogni articolo presente nella pagina
            ### Per ogni articolo presente nella lista degli articoli
                ### Creo il nuovo articolo Shoe e recupero i dati possibili
                ### Carico la pagina specifica dell'articolo
                ### Estraggo i dati mancanti dalla pagina specifica
                ### Aggiungo l'articolo alla lista totale degli articoli
        ### Trasformo in csv la lista totale deglli articoli

