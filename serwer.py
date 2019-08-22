import sqlite3
import io
from flask import Flask, render_template, request


class Baza:
    def __init__(self):
        self.connection = sqlite3.connect("gameBase.db")
        self.cursor = self.connection.cursor()
        self.connection.commit()

    def __del__(self):
        self.connection.close()

    def wykonaj(self, instrukcje):
        self.cursor.executescript(instrukcje)
        self.connection.commit()

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
    conditions = list()
    query = "SELECT DISTINCT tytul, link from tytuly AS t, tytuly_kategorie AS k, tytuly_mechaniki as m WHERE t.id_tytulu = k.id_tytulu AND t.id_tytulu = m.id_tytulu AND "
    if len(kategorie) > 0:
        conditions.append("k.id_kategorii IN (" + ",".join(kategorie) + ")")
    if len(mechaniki) > 0:
        conditions.append("m.id_mechaniki IN (" + ",".join(mechaniki) + ")")
    if wiek != "":
        conditions.append(wiek + " >= t.min_wiek")
    if gracze_od != "":
        conditions.append("t.min_liczba_graczy <= " + gracze_od + " AND t.max_liczba_graczy >= " + gracze_od)
    if gracze_do != "":
        conditions.append("t.min_liczba_graczy <= " + gracze_do + " AND t.max_liczba_graczy >= " + gracze_do)
    if czas_od != "":
        conditions.append("t.min_czas >= " + czas_od)
    if czas_do != "":
        conditions.append("t.max_czas <= " + czas_do)
    query += " AND ".join(conditions)
    print(query)
    print(baza.pobierzGry(query))
    return render_template("wynik.html", gry=baza.pobierzGry(query))


if __name__ == "__main__":
    serwer.run()
