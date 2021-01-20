
from bs4 import BeautifulSoup
import requests
from deep_translator import GoogleTranslator

def news(region):

    html = requests.get("https://anna-news.info/category/"+region)

    soup = BeautifulSoup(html.text, "html.parser")

    links = soup.find_all('a')

    lst = []

    for link in links:
        if "svodka-sobytij" in link.get('href'):
            lst.append(link.get('href'))


    html = requests.get(lst[0])

    soup = BeautifulSoup(html.text, "html.parser")

    par = soup.find_all('p')

    for item in par:

        if len(item.text) > 1:

            item1 = GoogleTranslator(source='russian', target='english').translate(item.text)
            item.string = item1

    return par

def news2():

    html = requests.get("https://anna-news.info/category/all_news/")

    soup = BeautifulSoup(html.text, "html.parser")

    links = soup.find_all('a')

    lst = []

    for link in links:
        if "glavnoe" in link.get('href'):
            lst.append(link.get('href'))


    html = requests.get(lst[0])

    soup = BeautifulSoup(html.text, "html.parser")

    par = soup.find_all('p')

    for item in par:

        if len(item.text) > 1:

            item1 = GoogleTranslator(source='russian', target='english').translate(item.text)
            item.string = item1

    return par







