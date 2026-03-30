# Leffakanta

## Asennusohjeet

Lataa koodi
```
git clone https://github.com/palmikko/leffakanta.git
```
Luo tietokanta
```
sqlite3 database.db < schema.sql
```
Käynnistä sovellus
```
flask run
```
## Kuvaus

Käyttäjien lisäämien elokuvien tiedot ja arvostelut. Luo tunnus ja kirjaudu sisään lisätäksesi elokuvia. Voit myös selata tai käyttää hakutoimintoa lisättyjen elokuvien etsimiseen.

## Ominaisuudet

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään sovellukseen elokuvia. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään elokuvia.
* Käyttäjä näkee sovellukseen lisätyt elokuvat. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät elokuvat.
* Käyttäjä pystyy etsimään elokuvia hakusanalla. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä elokuvia.

## kehitteillä

* Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät elokuvat.
* Käyttäjä pystyy valitsemaan elokuvalle yhden tai useamman luokittelun (esim. genre, arvosana, elokuvan kesto). Mahdolliset luokat ovat tietokannassa.
* Käyttäjä pystyy antamaan elokuvalle kommentin ja arvosanan. Elokuvasta näytetään kommentit ja keskimääräinen arvosana.
