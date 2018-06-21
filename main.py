#!/usr/bin/python
# -*- encoding: utf-8 -*-

# Preprost primer uporabe bottle, v katerem hranimo telefonski imenik
# v podatkovni bazi.

from bottle import *

# uncomment if you want to see error reports
# debug(True)

@get('/')
def index():
    return template('osnova.html')

@get('/besedilo')
def index():
    return "Sporočilo iz strežnika"

######################################################################
# Glavni program

# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8080, reloader=True)
