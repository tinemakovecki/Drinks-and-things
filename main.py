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

@get('/')
def index():
    return template('front_page.html')

@get('/drinks')
def index():
    return template('drinks.html', )

@get('/search')
def index():
    return template('search.html')

@post('/search_drinks')
def search_drinks_post():
    """ Performs a search through the drink databse with the given preferences """

    # collecting the values entered into the search form by the user
    query_dic = {"meat": request.forms.meat,
                 "prep": request.forms.prep,
                 "starch":  request.forms.starch,

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

    # constructing the sql command
    if len(key_terms) >= 1:
        sql_query = """(SELECT id, ime, drzava, velikost, stopnja_alkohola, vrsta
            FROM search WHERE hrana = %s)"""
    else:
        sql_query = """ SELECT * FROM search """

    if len(key_terms) > 1:
        for _ in range(1, len(key_terms)):
            additional_criteria = """
            INTERSECT
            (SELECT id, ime, drzava, velikost, stopnja_alkohola, vrsta
            FROM search WHERE hrana = %s)"""
            sql_query += additional_criteria

    # communication with database
    # TODO: fix the execute values!!!
    cur.execute(sql_query, key_terms)

    # show the results
    results = cur
    return template('drinks.html', results=results)

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
