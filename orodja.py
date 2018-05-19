import csv
import os
import sys
import requests

def pripravi_imenik(ime_datoteke):
    '''ce se ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)


def shrani(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        #print('Shranjujem {}...'.format(url), end = '')
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno ze od prej!')
            return
        r = requests.get(url, headers={'Accept-Language': 'en'})
    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')
    else:
        pripravi_imenik(ime_datoteke)
        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            print('shranjeno!')


def vsebina_datoteke(ime_datoteke):
    '''Vrne niz z vsebino datoteke z danim imenom.'''
    with open(ime_datoteke, encoding='utf-8') as datoteka:
        vsebina = datoteka.read()
    return vsebina


def datoteke(imenik):
    '''Vrne imena vseh datotek v danem imeniku skupaj z imenom imenika.'''
    return [os.path.join(imenik, datoteka) for datoteka in os.listdir(imenik)]


def zapisi_tabelo(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8', newline='') as csv_dat:
        writer = csv.DictWriter(csv_dat, fieldnames=imena_polj, delimiter = ';')
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)


# DATA PRE-PROCESSING:
# needed for easier upload to database

def transform_beer():

    directory = os.path.dirname(__file__)
    file = directory +'/CSV/piva2.csv'

    beers = []
    country_dic = {'Scotch Beer': 'Scotland',
                   'English Beer': 'England',
                   'Belgian Beer': 'Belgium',
                   'American Beer': 'United States',
                   'Japanese Beer': 'Japan',
                   'Dutch Beer': 'Netherlands',
                   'Danish Beer': 'Denmark',
                   'Kiwi Beer': 'New Zealand',
                   'Australian Beer': 'Australia',
                   'German Beer': 'Germany',
                   'Icelandic Beer': 'Iceland'}

    # transform the file into a list of dictionaries, where each element represents a beer
    # along the way the entries are changed to a more practical form
    with open(file, encoding='utf-8',) as source:
        reader = csv.DictReader(source, delimiter=';')
        for row in reader:
            ime = row['Name']
            pivovarna = row['Brewery']
            vrsta = row['Style']
            velikost = row['Volume']
            stopnja_alkohola = row['ABV']
            drzava = country_dic[row['Country']]

            if row['Price'] == 'Discontinued':
                cena = None
            else:
                cena = row['Price']

            entry = {'ime': ime,
                     'pivovarna': pivovarna,
                     'vrsta': vrsta,
                     'velikost': velikost,
                     'stopnja_alkohola': stopnja_alkohola,
                     'drzava': drzava,
                     'cena': cena,
                     'opis': ''}
            beers.append(entry)

    column_names = ['ime', 'pivovarna', 'vrsta', 'velikost',
                    'stopnja_alkohola', 'drzava', 'cena', 'opis']

    # write a new file with the adjusted data
    zapisi_tabelo(beers, column_names, 'beers.csv')


transform_beer()