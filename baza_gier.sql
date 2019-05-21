drop table tytuly;
drop table kategorie;
drop table mechaniki;
drop table tytuly_kategorie;
drop table tytuly_mechaniki;

create table tytuly(
    id_tytulu INTEGER primary key AUTOINCREMENT,
    tytul TEXT NOT NULL,
	min_wiek INTEGER,
	min_liczba_graczy INTEGER,
	max_liczba_graczy INTEGER,
	min_czas INTEGER,
	max_czas INTEGER
    );

create table kategorie(
    id_kategorii INTEGER primary key AUTOINCREMENT,
    kategoria TEXT NOT NULL
    );

create table mechaniki(
    id_mechaniki INTEGER primary key AUTOINCREMENT,
    mechanika TEXT NOT NULL
    );

create table tytuly_kategorie(
    id_tytulu NOT NULL,
    id_kategorii NOT NULL,
foreign key(id_tytulu) REFERENCES tytuly(id_tytulu),
foreign key(id_kategorii) REFERENCES kategorie(id_kategorii)
    );

create table tytuly_mechaniki(
    id_tytulu NOT NULL,
    id_mechaniki NOT NULL,
foreign key(id_tytulu) REFERENCES tytuly(id_tytulu),
foreign key(id_mechaniki) REFERENCES mechaniki(id_mechaniki)
    );

