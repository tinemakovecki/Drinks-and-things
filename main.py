#!/usr/bin/python
# -*- encoding: utf-8 -*-

from bottle import *

# uncomment if you want to see error reports
# debug(True)

@get('/')
def index():
    return template('drinks.html')

@get('/search')
def index():
    return template('search.html')

@post('/search_drinks')
def search_drinks_post():
    # this is actually just a test

    ime = request.forms.ime
    drzava = request.forms.drzava

    print(ime + " ; " + drzava)

    vrsta = request.forms.vrsta_menu

    print(vrsta)

    check = request.forms.check1

    print(check)

    redirect("/")

# ====================================== #
# MAIN PROGRAM
# ====================================== #

# we run the server on port 8080, access at: http://localhost:8080/
run(host='localhost', port=8080, reloader=True)
