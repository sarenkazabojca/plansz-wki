import sqlite3
from flask import Flask, render_template, request


class Baza:
    def __init__(self):
        self.connection = sqlite3.connect("gameBase.db")
        self.cursor = self.connection.cursor()
        self.connection.commit()

    def __del__(self):
        self.connection.close()

    def pobierzMechaniki(self):
        self.cursor.execute("select * from mechaniki;")
        return list(map(lambda wiersz: dict({
            "id":               wiersz[0],
            "nazwa":            wiersz[1],
        }), self.cursor.fetchall()))

    def pobierzKategorie(self):
        self.cursor.execute("select * from kategorie;")
        return list(map(lambda wiersz: dict({
            "id":               wiersz[0],
            "nazwa":            wiersz[1],
        }), self.cursor.fetchall()))

    def pobierzGry(self, zapytanie):
        self.cursor.execute(zapytanie)
        return list(map(lambda wiersz: dict({
            "nazwa":            wiersz[0],
            "link":             wiersz[1],
            "rating":           wiersz[2]
        }), self.cursor.fetchall()))


serwer = Flask(__name__)


@serwer.route("/")
def main():
    baza = Baza()
    return render_template("ankieta.html", mechaniki=baza.pobierzMechaniki(), kategorie=baza.pobierzKategorie())


@serwer.route("/wynik", methods=["POST"])
def zapytanie1():
    baza = Baza()
    data = request.form
    kategorie = data.getlist("kategoria[]")
    mechaniki = data.getlist("mechanika[]")
    wiek = data.get("wiek")
    gracze_od = data.get("gracze_od")
    gracze_do = data.get("gracze_do")
    czas_od = data.get("czas_od")
    czas_do = data.get("czas_do")
    warunki = list()
    zapytanie = "SELECT DISTINCT tytul, link, rating from tytuly AS t, tytuly_kategorie AS k, tytuly_mechaniki as m WHERE t.id_tytulu = k.id_tytulu AND t.id_tytulu = m.id_tytulu AND "
    if len(kategorie) > 0:
        warunki.append("k.id_kategorii IN (" + ",".join(kategorie) + ")")
    if len(mechaniki) > 0:
        warunki.append("m.id_mechaniki IN (" + ",".join(mechaniki) + ")")
    if wiek != "":
        warunki.append(wiek + " >= t.min_wiek")
    if gracze_od != "":
        warunki.append("t.min_liczba_graczy <= " + gracze_od + " AND t.max_liczba_graczy >= " + gracze_od)
    if gracze_do != "":
        warunki.append("t.min_liczba_graczy <= " + gracze_do + " AND t.max_liczba_graczy >= " + gracze_do)
    if czas_od != "":
        warunki.append("t.min_czas >= " + czas_od)
    if czas_do != "":
        warunki.append("t.max_czas <= " + czas_do)
    zapytanie += " AND ".join(warunki)
    zapytanie += " ORDER BY t.rating"
    return render_template("wynik.html", gry=baza.pobierzGry(zapytanie))


if __name__ == "__main__":
    serwer.run()
