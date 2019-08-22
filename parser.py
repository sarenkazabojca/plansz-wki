from urllib.request import urlopen
from htmldom import htmldom
import re
import sqlite3
import io


class Game:
    name = ''
    categories = list()
    rating = ''
    mechanics = list()
    age = ''
    gamers = ''
    time = ''
    link = ''


class gameBase:
    def __init__(self):
        self.connection = sqlite3.connect("gameBase.db")
        self.cursor = self.connection.cursor()
        self.connection.commit()

    def __del__(self):
        self.connection.close()

    def wykonaj(self, instrukcje):
        self.cursor.executescript(instrukcje)
        self.connection.commit()


with io.open('baza_gier.sql', mode='r', encoding='utf-8') as sql:
    base = gameBase()
    base.wykonaj(sql.read())


def getUrlDom(url):
    request = urlopen(url) #tworzymy żądanie po zawartość podanego adresu
    html = request.read().decode('windows-1250') #pobieramy treść odpowiedzi, a następnie dekodujemy ją z kodowania windows 1250, bo parser pewnie pracuje w jakimś innym
    return htmldom.HtmlDom().createDom(html) #na podstawie html tworzymy drzewo dokumentu (htmldom to biblioteka do tworzenie drzewa dokumentu)


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


def getMinMax(str):
    match = re.search("od (\\d+) do (\\d+)", str)
    if match != None:
        return match.groups()
    match = re.search("od (\\d+)", str)
    if match != None:
        return match.groups()[0], None
    match = re.search("do \\d+", str)
    if match != None:
        return None, match.groups()[0]
    match = re.search("\d+", str)
    if match != None:
        num = match.group()
        return num, num
    else:
        return None, None


def getId(name, id_field, field, table):
    if name != None:
        base.cursor.execute("SELECT " + id_field + " FROM " + table + " WHERE " + field + " = \"" + name + "\";")
        row = base.cursor.fetchone()
        if row:
            return row[0]
        else:
            base.cursor.execute("INSERT INTO " + table + " VALUES (NULL, ?)", (name,))
            return base.cursor.lastrowid


def saveGame(game):
    min_age = getMinMax(game.age)[0]
    time = getMinMax(game.time)
    min_time = time[0]
    max_time = time[1]
    gamers = getMinMax(game.gamers)
    min_gamers = gamers[0]
    max_gamers = gamers[1]

    base.cursor.execute("INSERT INTO tytuly VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
                        (game.name, min_age, min_gamers, max_gamers, min_time, max_time, game.link))
    title_id = base.cursor.lastrowid
    category_ids = list()
    for category in game.categories:
        category_ids.append(getId(category, "id_kategorii", "kategoria", "kategorie"))
    mechanic_ids = list()
    for mechanic in game.mechanics:
        mechanic_ids.append(getId(mechanic, "id_mechaniki", "mechanika", "mechaniki"))
    for category_id in category_ids:
        base.cursor.execute("INSERT INTO tytuly_kategorie VALUES (?, ?)", (title_id, category_id))
    for mechanic_id in mechanic_ids:
        base.cursor.execute("INSERT INTO tytuly_mechaniki VALUES (?, ?)", (title_id, mechanic_id))
    base.connection.commit()
    print("Zapisuję grę: " + game.name)


print("Odczytuję listę gier")

url = 'http://gra24h.pl/'
dom = getUrlDom(url)
games = dom.find('div#nazwa a')

print("Rozpoczynam pracę")

for game in games.nodeList:
    try:
        g = Game()
        link = url + game.attributes['href'][0]
        dom = getUrlDom(link)
        g.name = dom.find('h2.panel-title').nodeList[0].children[0].text.strip()
        keys = dom.find('div.panel-body dl.dl-horizontal dt')
        values = dom.find('div.panel-body dl.dl-horizontal dd')
        g.categories = getValuesForKey(values, keys, 'Kategorie')
        g.rating = getValueForKey(values, keys, 'Pozycja na BGG')
        g.mechanics = getValuesForKey(values, keys, 'Mechaniki')
        g.age = getValueForKey(values, keys, 'Wiek')
        g.gamers = getValueForKey(values, keys, 'Liczba graczy')
        g.time = getValueForKey(values, keys, 'Czas gry')
        g.link = link
        saveGame(g)
    except:
        print("Błędny format danych")
        continue

