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

    meat = request.forms.meat
    starch = request.forms.starch
    nuts = request.forms.nuts
    beans = request.forms.beans
    green = request.forms.green

    if green:
        print('fuck')
    print(meat)
    print(starch)
    print(nuts)
    print(beans)
    print(green)

    redirect("/")

# ====================================== #
# MAIN PROGRAM
# ====================================== #

# we run the server on port 8080, access at: http://localhost:8080/
run(host='localhost', port=8080, reloader=True)
