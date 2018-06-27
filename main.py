#!/usr/bin/python
# -*- encoding: utf-8 -*-

from bottle import *

# uncomment if you want to see error reports
# debug(True)

@get('/')
def index():
    return template('osnova.html')

@get('/besedilo')
def index():
    return "Sporočilo iz strežnika"

@get('/id')
def index():
    return """<thead>
        <tr>
            <th>Drink name</th>
            <th>drink type</th>
            <th>country</th>
            <th>size</th>
            <th>price</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>f</td>
            <td>fe</td>
            <td>fec</td>
            <td>feck</td>
            <td>test</td>
        </tr>
    </tbody>"""

######################################################################
# Glavni program

# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8080, reloader=True)
