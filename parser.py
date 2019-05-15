from urllib.request import urlopen
from htmldom import htmldom


class Game:
    name = ''
    categories = list()
    rating = ''
    mechanics = list()
    age = ''
    gamers = ''
    time = ''


def getUrlDom(url):
    request = urlopen(url) #tworzymy żądanie po zawartość podanego adresu
    html = request.read().decode('windows-1250') #pobieramy treść odpowiedzi, a następnie dekodujemy ją z kodowania windows 1250, bo parser wernie pracuje w jakimś innym
    return htmldom.HtmlDom().createDom(html) #na podstawie html tworzymy drzewo dokumentu (htmldom to bibliotekja do tworzenie drzewa dokumentu)


#zwracamy tekst wewnątrz wązła do listy
def getValues(parentNode):
    values = list()
    for node in parentNode.children:
        text = node.text
        if text != '':
            values.append(text)
    return values


#zwraca indeks danego ciągu znaków wewnątrz listy węzłów kluczy
def getKeyIndex(keys, key):
    l = keys.nodeList
    for i in range(0, len(l)):
        if l[i].children[0].text == key:
            return i
    return False


#zwraca listę szukanych wartości dla danego klucza
def getValuesForKey(values, keys, key):
    index = getKeyIndex(keys, key)
    if index == False:
        return list()
    else:
        return getValues(values.nodeList[index])


#zwraca jedną(str) szukaną wartość dla danego klucza (aby nie uzyskać listy(tak jak w getValuesForKey) z jadną wartością)
def getValueForKey(values, keys, key):
    values = getValuesForKey(values, keys, key)
    if len(values) > 0:
        return values[0]
    else:
        return ''


url = 'http://gra24h.pl/'
dom = getUrlDom(url)
games = dom.find('div#nazwa a')
data = list()

for game in games.nodeList:
    g = Game()
    dom = getUrlDom(url + game.attributes['href'][0])
    g.name = dom.find('h2.panel-title').nodeList[0].children[0].text.strip()
    keys = dom.find('div.panel-body dl.dl-horizontal dt')
    values = dom.find('div.panel-body dl.dl-horizontal dd')
    g.categories = getValuesForKey(values, keys, 'Kategorie')
    g.rating = getValueForKey(values, keys, 'Pozycja na BGG')
    g.mechanics = getValuesForKey(values, keys, 'Mechaniki')
    g.age = getValueForKey(values, keys, 'Wiek')
    g.gamers = getValueForKey(values, keys, 'Liczba graczy')
    g.time = getValueForKey(values, keys, 'Czas gry')
    data.append(g)


