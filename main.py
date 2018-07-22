#!/usr/bin/python
# -*- encoding: utf-8 -*-

from bottle import *

# TODO: switch to public authorization
import auth

# import psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)  # bcoz šumniki

# uncomment if you want to see error reports
# debug(True)

LAST_BEER_ID = 1041


@get('/')
def index():
    return template('front_page.html')

@get('/drinks')
def index():
    return template('drinks.html', )

@get('/search')
def index():
    return template('search.html')

@get('/general_info')
def index():
    return template('general_info.html')

@get('/statistics')
def index():
    return template('statistics.html')

@get('/wine_info/:x/')
def get_wine_info(x):
    """ Performs a search through the drink database about the wine with id x """
    drink_query = """(SELECT DISTINCT pijaca.ime, drzava, velikost, stopnja_alkohola, vrste_pijace.ime AS vrsta, cena, opis, slika
                FROM pijaca JOIN vrste_pijace on pijaca.vrsta = vrste_pijace.id
                WHERE pijaca.id = %s)"""
    wine_query = """(SELECT barva,regija
                    FROM vino WHERE id = %s)"""
    taste_query = """(SELECT DISTINCT ime
                    FROM okusi JOIN ima_okus ON okusi.id = ima_okus.okus
                    WHERE vino = %s)"""
    smell_query = """(SELECT DISTINCT ime
                    FROM aroma JOIN ima_vonj ON aroma.id = ima_vonj.aroma
                    WHERE vino = %s)"""
    cur.execute(drink_query, [int(x)])
    r1 = next(cur)
    cur.execute(wine_query, [int(x)])
    r2 = next(cur)
    cur.execute(taste_query, [int(x)])
    r3 = []
    for [t] in cur:
        r3.append(t)
    cur.execute(smell_query, [int(x)])
    r4 = []
    for [s] in cur:
        r4.append(s)
    return template('wine_info.html', res1=r1, res2=r2, taste=r3, smell=r4)

@get('/beer_info/:x/')
def get_beer_info(x):
    """ Performs a search through the drink database about the beer with id x """
    drink_query = """(SELECT DISTINCT pijaca.ime, drzava, velikost, stopnja_alkohola, vrste_pijace.ime AS vrsta, cena, opis, slika
                FROM pijaca JOIN vrste_pijace on pijaca.vrsta = vrste_pijace.id
                WHERE pijaca.id = %s)"""
    beer_query = """(SELECT pivovarna
                    FROM pivo WHERE id = %s)"""
    cur.execute(drink_query, [int(x)])
    result = next(cur)
    cur.execute(beer_query, [int(x)])
    [brewery] = next(cur)
    return template('beer_info.html', result=result, pivovarna=brewery)

@get('/country/:x/')
def get_country(x):
    """ Performs a search through the drink database with the chosen country """
    country_query = """(SELECT id, ime, drzava, velikost, stopnja_alkohola, slika, cena, vrsta
                        FROM pijaca WHERE drzava = %s)"""
    cur.execute(country_query, [x])
    results = cur
    return template('drinks.html', results=results, pictures=True)

@post('/search_drinks')
def search_drinks_post():
    """ Performs a search through the drink database with the given preferences """
    # collecting the values entered into the search form by the user
    query_dic = {"grilled": request.forms.grilled,
                 "fried": request.forms.fried,
                 "roasted": request.forms.roasted,
                 "smoked": request.forms.smoked,
                 "steamed": request.forms.steamed,

                 #meat
                 "red_meat": request.forms.red_meat,
                 "cured": request.forms.cured_meat,
                 "pork": request.forms.pork,
                 "poultry": request.forms.poultry,
                 "mollusk":  request.forms.mollusk,
                 "fish": request.forms.fish,
                 "shellfish": request.forms.shellfish,

                 # starch
                 "white": request.forms.white_starch,
                 "whole": request.forms.whole_wheat,
                 "sweet": request.forms.sweet_starchy_vegetables,
                 "potato": request.forms.potato,

                 # vegetables
                 "alliums": request.forms.alliums,
                 "green": request.forms.green,
                 "mushrooms": request.forms.mushrooms,
                 "beans": request.forms.beans,
                 "nuts": request.forms.nuts,
                 "nightshades": request.forms.nightshades,

                 # spices
                 "spicy": request.forms.spicy,
                 "herbs": request.forms.herbs,
                 "black": request.forms.black_pepper,
                 "red": request.forms.red_pepper,
                 "baking": request.forms.baking,
                 "exotic": request.forms.exotic,

                 # cheese
                 "soft": request.forms.soft,
                 "hard": request.forms.hard,
                 "pungent": request.forms.pungent,

                 # sweets
                 "fruit": request.forms.fruit,
                 "vanilla": request.forms.vanilla,
                 "chocolate": request.forms.chocolate,
                 "coffee": request.forms.coffee}

    # gather the search terms actually selected by the user
    l = query_dic.values()
    key_terms = [x for x in l if x != ""]

    pref_drink = request.forms.drink

    # constructing the sql command
    if len(key_terms) >= 1:
        if pref_drink == "both":
            sql_query = """(SELECT id, ime, drzava, velikost, stopnja_alkohola, slika, cena, vrsta
                            FROM search WHERE hrana = %s)"""
        elif pref_drink == "beer":
            sql_query = """(SELECT id, ime, drzava, velikost, stopnja_alkohola, slika, cena, vrsta
                            FROM search WHERE id <= 1041 AND hrana = %s)"""
        else:
            sql_query = """(SELECT id, ime, drzava, velikost, stopnja_alkohola, slika, cena, vrsta
                            FROM search WHERE id > 1041 AND hrana = %s)"""
    else:
        if pref_drink == "both":
            sql_query = """(SELECT id, ime, drzava, velikost, stopnja_alkohola, slika, cena, vrsta
                            FROM search)"""
        elif pref_drink == "beer":
            sql_query = """(SELECT id, ime, drzava, velikost, stopnja_alkohola, slika, cena, vrsta
                            FROM search WHERE id <= 1041)"""
        else:
            sql_query = """(SELECT id, ime, drzava, velikost, stopnja_alkohola, slika, cena, vrsta
                            FROM search WHERE id > 1041)"""

    if len(key_terms) > 1:
        for _ in range(1, len(key_terms)):
            additional_criteria = """
            INTERSECT
            (SELECT id, ime, drzava, velikost, stopnja_alkohola, slika, cena, vrsta
            FROM search WHERE hrana = %s)"""
            sql_query += additional_criteria

    # communication with database
    # TODO: fix the execute values!!!
    #var = [LAST_BEER_ID] + key_terms
    cur.execute(sql_query, key_terms)

    # show the results
    results = cur

    # does the user want to see pictures by the suggested drinks
    pictures = True
    if request.forms.pictures == "no":
        pictures = False

    return template('drinks.html', results=results, pictures=pictures)

    #redirect("/")

# ====================================== #
# MAIN PROGRAM
# ====================================== #

# connection to the database
connection = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)  # we disable transactions?
cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

# we run the server on port 8080, access at: http://localhost:8080/
run(host='localhost', port=8080, reloader=True)
