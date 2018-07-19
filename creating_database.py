# ====================================== #
# IMPORTS
# ====================================== #

# import authorization info
import auth
auth.db = "sem2018_%s" % auth.user

# import psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)  # bcoz šumniki

import csv

# ====================================== #
# FUNCTIONS
# ====================================== #


def create_table(name, sql_description):
    """ Create a table with a given name from a given sql description """
    cur.execute("""CREATE TABLE {}(
        {});
        """.format(name, sql_description))
    connection.commit()


def delete_table(name):
    """ Deletes a table """
    cur.execute("""
        DROP TABLE %s;
        """, name)
    connection.commit()


def insert_into_table(table_name, new_entry):  # TODO: test!
    """ Inserts an entry into the selected table """

    # getting column names
    column_names = new_entry.keys()

    # constructing a string for the sql command:
    names = ', '.join(column_names)
    # we format the values part of the string
    # so that .execute() will be able to insert parameters into the command
    filler_string = ""
    for name in column_names:
        filler_string += "%({})s, ".format(name)
    filler_string = filler_string[:-2]
    # format the parts together
    sql_command = """   INSERT INTO {}
        ({})
        VALUES 
        ({})
    """.format(table_name, names, filler_string)

    # execute the insert
    cur.execute(sql_command,
                new_entry)
    connection.commit()


def upload_data(table, data_file):
    """ Uploads data from a selected file into a table. The data file has to be in .csv format.
        The column names of the file have to match the attributes of the chosen table. """
    with open(data_file, encoding='utf-8') as file:
        read = csv.DictReader(file, delimiter=';')
        next(read)  # leave out the head line
        for entry in read:
            column_names = entry.keys()
            insert_into_table(table, column_names, entry)

# open a connection with the database
connection = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


# ====================================== #
# SQL TEXT
# ====================================== #
# All the needed sql strings that will be used for creating the database

vrste_hrane = """   id SERIAL PRIMARY KEY,
    ime TEXT UNIQUE
"""

jed = """    id SERIAL PRIMARY KEY,
    ime TEXT UNIQUE NOT NULL,
    opis TEXT
"""

vrsta_jedi = """    id SERIAL PRIMARY KEY,
    jed INTEGER REFERENCES jed(id),
    vrsta INTEGER REFERENCES vrste_hrane(id)
"""

vrste_pijace = """  id SERIAL PRIMARY KEY,
    ime TEXT UNIQUE
"""

# price = None usually means the drink is discontinued or unavailable
pijaca = """    id SERIAL PRIMARY KEY,
    ime TEXT NOT NULL,
    drzava TEXT NOT NULL,
    velikost NUMERIC NOT NULL,
    stopnja_alkohola NUMERIC,
    vrsta INTEGER REFERENCES vrste_pijace(id),
    cena NUMERIC,
    opis TEXT,
    slika TEXT
"""

pivo = """    id INTEGER REFERENCES pijaca(id),
    pivovarna TEXT NOT NULL,
    PRIMARY KEY (id)
"""

vino = """    id INTEGER REFERENCES pijaca(id),
    barva TEXT NOT NULL,
    regija TEXT,
    PRIMARY KEY (id)
"""

aroma = """    id SERIAL PRIMARY KEY,
    ime TEXT UNIQUE NOT NULL
"""

ima_vonj = """    id SERIAL PRIMARY KEY,
    aroma INTEGER NOT NULL REFERENCES aroma(id),
    vino INTEGER NOT NULL REFERENCES vino(id)
"""

okusi = """    id SERIAL PRIMARY KEY,
    ime TEXT UNIQUE NOT NULL
"""

ima_okus = """    id SERIAL PRIMARY KEY,
    okus INTEGER NOT NULL REFERENCES okusi(id),
    vino INTEGER NOT NULL REFERENCES vino(id)
"""

priporocila = """   id SERIAL PRIMARY KEY,
    vrsta_hrane INTEGER REFERENCES vrste_hrane(id),
    vrsta_pijace INTEGER REFERENCES vrste_pijace(id),
    is_perfect BIT NOT NULL
"""

# ====================================== #
# EXECUTION
# ====================================== #

# CREATING THE TABLES:
create_table('vrste_hrane', vrste_hrane)
create_table('jed', jed)
create_table('vrsta_jedi', vrsta_jedi)

create_table('vrste_pijace', vrste_pijace)
create_table('priporocila', priporocila)
create_table('pijaca', pijaca)
create_table('pivo', pivo)

create_table('vino', vino)
create_table('aroma', aroma)
create_table('ima_vonj', ima_vonj)
create_table('okusi', okusi)
create_table('ima_okus', ima_okus)




# UPLOADING DATA:
def beer_upload():
    """ Uploads data from the beer file into the database. """
    # we'll keep a dictionary of uploaded categories and their ids
    uploaded_categories = {}

    with open('beers.csv', encoding='utf-8') as file:
        read = csv.DictReader(file, delimiter=';')
        next(read)  # leave out the head line
        for entry in read:

            # table vrste_pijace
            if entry['vrsta'] not in uploaded_categories:
                cur.execute("""INSERT INTO vrste_pijace(ime)
                VALUES
                (%s)
                RETURNING id
                """, [entry['vrsta']])
                cat_id, = cur.fetchone()  # save the id to insert it into 'pijaca' table
                uploaded_categories[entry['vrsta']] = cat_id

            # table pijaca
            if entry['cena'] == '':
                entry['cena'] = None

            # switch the dictionary to contain vrsta id
            entry['vrsta'] = uploaded_categories[entry['vrsta']]

            cur.execute("""INSERT INTO
                pijaca(ime, vrsta, velikost, stopnja_alkohola, drzava, cena, opis, slika)
            VALUES
                (%(ime)s, %(vrsta)s, %(velikost)s, %(stopnja_alkohola)s, %(drzava)s, %(cena)s, %(opis)s, %(slika)s)
            RETURNING id
            """, entry)
            return_id, = cur.fetchone()

            # table pivo
            pivce = {'id': return_id, 'pivovarna': entry['pivovarna']}
            cur.execute("""INSERT INTO pivo(id, pivovarna)
            VALUES
            (%(id)s, %(pivovarna)s)
            """, pivce)

    connection.commit()
    print('Beer upload successful!')
    return uploaded_categories


def wine_upload():
    """ Uploads data from the wine file into the database. """
    # we'll keep a dictionary of uploaded info and their ids,
    # so we can correctly connect the tables when needed
    uploaded_categories = {}
    uploaded_smells = {}
    uploaded_tastes = {}

    with open('wines.csv', encoding='utf-8') as file:
        read = csv.DictReader(file, delimiter=';')
        next(read)  # leave out the head line
        for entry in read:

            # table vrste_pijace
            if entry['vrsta'] not in uploaded_categories:
                cur.execute("""INSERT INTO vrste_pijace(ime)
                VALUES
                (%s)
                RETURNING id
                """, [entry['vrsta']])
                cat_id, = cur.fetchone()  # save the id to insert it into 'pijaca' table
                # connection.commit()
                uploaded_categories[entry['vrsta']] = cat_id

            # table pijaca
            if entry['stopnja_alkohola'] == '':
                entry['stopnja_alkohola'] = None

            # switch the dictionary to contain vrsta id
            entry['vrsta'] = uploaded_categories[entry['vrsta']]

            cur.execute("""INSERT INTO
                pijaca(ime, vrsta, velikost, stopnja_alkohola, drzava, cena, opis, slika)
            VALUES
                (%(ime)s, %(vrsta)s, %(velikost)s, %(stopnja_alkohola)s, %(drzava)s, %(cena)s, %(opis)s, %(slika)s)
            RETURNING id
            """, entry)
            return_id, = cur.fetchone()

            # table vino
            vince = {'id': return_id, 'barva': entry['barva'], 'regija': entry['regija']}
            cur.execute("""INSERT INTO vino(id, barva, regija)
            VALUES
            (%(id)s, %(barva)s, %(regija)s)
            """, vince)

            # adding smells
            smell_string = entry['vonj']
            # we have to parse the string of smells
            smell_string = smell_string.strip(""" "'""")
            smell_list = smell_string.split(',')
            smell_list = smell_list[:-1] + smell_list[-1].split(' and ')
            smells = []
            for element in smell_list:
                smells.append(element.strip())

            for smell in smells:
                if smell not in uploaded_smells:
                    cur.execute("""INSERT INTO aroma(ime)
                    VALUES
                    (%s)
                    RETURNING id
                    """, [smell])
                    aroma_id, = cur.fetchone()  # save the id to insert it into other tables
                    uploaded_smells[smell] = aroma_id

                # connect the wine to its aroma
                cur.execute("""INSERT INTO ima_vonj(aroma, vino)
                VALUES
                (%(aroma)s, %(vino)s)
                """, {'aroma': uploaded_smells[smell], 'vino': return_id})

            # adding taste
            taste_string = entry['okus']
            # we have to parse the string of tastes
            taste_string = taste_string.strip(""" "'""")
            taste_list = taste_string.split(',')
            taste_list = taste_list[:-1] + taste_list[-1].split(' and ')
            tastes = []
            for element in taste_list:
                tastes.append(element.strip())

            for taste in tastes:
                if taste != "":
                    if taste not in uploaded_tastes:
                        cur.execute("""INSERT INTO okusi(ime)
                        VALUES
                        (%s)
                        RETURNING id
                        """, [taste])
                        taste_id, = cur.fetchone()  # save the id to insert it into other tables
                        uploaded_tastes[taste] = taste_id

                    # connect the wine to its taste
                    cur.execute("""INSERT INTO ima_okus(okus, vino)
                    VALUES
                    (%(okus)s, %(vino)s)
                    """, {'okus': uploaded_tastes[taste], 'vino': return_id})

    connection.commit()
    print('Wine upload successful!')
    return uploaded_categories


# execute the upload
beer_ids = beer_upload()
wine_ids = wine_upload()


# ====================================== #
# PAIRINGS
# ====================================== #

# ===== WINE ===== #

# VARIETIES
bold_red = ['Malbec', 'Syrah / Shiraz', 'Mourvedre / Mataro / Monastrell / Garrut', 'Petite Sirah', 'Cabernet Sauvignon']
medium_red = ['Merlot', 'Sangiovese', 'Zinfandel', 'Cabernet Franc', 'Tempranillo / Tinto Fino / Tinta Roriz', 'Nebbiolo']
light_red = ['Pinot Noir', 'Grenache / Garnacha', 'Gamay', 'Carignan / Carinena']
rich_white = ['Chardonnay', 'Roussanne']
light_white = ['Sauvignon Blanc', 'Pinot Bianco / Pinot Blanc', 'Pinot Gris / Pinot Grigio']
sweet_white = ['Muscat', 'Riesling', 'Chenin Blanc', 'Malvasia']
dessert = ['Port Varieties', 'Sherry Varieties']
unmatched = ['Cinsault', 'Refosco', 'Petit Verdot', 'Pinot Meunier'] # razen prvega vsi pomojem samo v blendih

# PERFECT MATCHES
perfect_matches = {'red meat': bold_red, 'cured meat': light_red + sweet_white, 'pork': medium_red,         # meat
                   'poultry': light_red + rich_white, 'mollusk': [], 'fish': light_white, 'shellfish': rich_white,
                   'grilled': bold_red, 'fried': light_red, 'smoked': medium_red, 'roasted': bold_red,     # preparation
                   'steamed': light_white,
                   'soft': light_red + rich_white, 'pungent': medium_red + dessert, 'hard': bold_red,       # cheese
                   'alliums': medium_red, 'green': light_white, 'root': [], 'nightshades': medium_red,      # vegetable
                   'funghi': medium_red + light_red + rich_white, 'nuts': sweet_white, 'beans': light_white,
                   'black pepper': bold_red, 'red pepper': medium_red, 'spicy': sweet_white,                # spices
                   'herbs': light_white, 'baking spices': dessert, 'exotic': medium_red + sweet_white,
                   'white starches': [], 'whole wheat': sweet_white,                                        # starches
                   'sweet starchy vegetables': sweet_white, 'potato': [],
                   'fruit': sweet_white, 'vanilla': [], 'chocolate': dessert, 'coffee': dessert}            # sweet

matches = {'red meat': medium_red, 'cured meat': bold_red + medium_red + dessert, 'pork': bold_red,         # meat
           'poultry': medium_red + light_white, 'mollusk': light_white, 'fish': rich_white,
           'shellfish': light_white + sweet_white,
           'grilled': medium_red + light_red + sweet_white, 'fried': rich_white + light_white,             # preparation
           'smoked': bold_red + light_red + dessert, 'roasted': medium_red + light_red + sweet_white,
           'steamed': rich_white + sweet_white,
           'soft': medium_red + light_white + sweet_white + dessert,                                        # cheese
           'pungent': bold_red + light_white + sweet_white, 'hard': medium_red + rich_white,
           'alliums': bold_red + light_red + rich_white + light_white + sweet_white, 'green': [],           # vegetable
           'root': rich_white + sweet_white, 'nightshades': bold_red + sweet_white, 'funghi': bold_red,
           'nuts': light_red + rich_white + light_white, 'beans': medium_red,
           'black pepper': medium_red, 'red pepper': bold_red + light_white + sweet_white,                  # spices
           'spicy': light_white, 'herbs': medium_red + light_red + rich_white,
           'baking spices': medium_red + sweet_white,'exotic': light_red,
           'white starches': bold_red + medium_red + light_red + rich_white + light_white + sweet_white +   # starches
                             dessert, 'whole wheat': light_red + rich_white, 'sweet starchy vegetables': [],
           'potato': bold_red + medium_red + light_red + rich_white + light_white + sweet_white,
           'fruit': dessert, 'vanilla': sweet_white + dessert, 'chocolate': [], 'coffee': []}               # sweet

# ===== BEER ===== #

# note: because of the sources available, wine matches could be split into "perfect" and "OK" categories,
# but the beer matches can't be. Therefore all beer matches will be "OK" and the distinction won't be relevant.

# add more pairings?
beer_matches = {'red meat': ['Bock Beer', 'Porter Beer', 'Red Ale Beer'],                                 # meat
                'cured meat': ['Porter Beer', 'Red Ale Beer'],
                'pork': ['IPA (India Pale Ale) Beer', 'Dubbel Beer', 'Dark Ale Beer'],
                'poultry': ['Lager / Pilsner Beer'],
                'mollusk': ['Saison Beer', 'Wheat / Wit / White Beer'],
                'fish': ['Porter Beer', 'Lager / Pilsner Beer'],
                'shellfish': ['Saison Beer', 'Wheat / Wit / White Beer'],

                'grilled': ['Bock Beer', 'Porter Beer', 'Smoked Beer', 'Blonde Beer', 'Oktoberfest Beer',  # preparation
                            'IPA (India Pale Ale) Beer', 'Stout Beer', 'Red Ale Beer'],
                'fried': ['IPA (India Pale Ale) Beer', 'Dark Lager / Schwarzbier Beer'],
                'smoked': ['Smoked Beer', 'Porter Beer', 'Stout Beer', 'Pale Ale Beer'],
                'roasted': ['Bock Beer', 'Lager / Pilsner Beer', 'Porter Beer'],
                'steamed': ['Lager / Pilsner Beer', 'Wheat / Wit / White Beer'],

                'soft': ['Lager / Pilsner Beer', 'Wheat / Wit / White Beer',                # cheese
                         'Pale Ale Beer', 'IPA (India Pale Ale) Beer'],
                'pungent': ['Pale Ale Beer', 'APA (American Pale Ale) Beer', 'IPA (India Pale Ale) Beer',
                            'Barley Wine Beer', 'Tripel Beer', 'Abbey / Trappist Beer', 'Dubbel Beer'],
                'hard': ['Stout Beer', 'Porter Beer', 'Bock Beer', 'Dark Ale Beer'],

                'alliums': ['Pale Ale Beer', 'Lager / Pilsner Beer', 'IPA (India Pale Ale) Beer'],        # vegetable
                'green': ['Lager / Pilsner Beer'],
                'root': ['Red Ale Beer', 'Alt, Kolsch Beer', 'Blonde Beer'],
                'nightshades': ['Lager / Pilsner Beer', 'IPA (India Pale Ale) Beer', 'Saison Beer'],
                'funghi': ['Stout Beer', 'Dark Lager / Schwarzbier Beer'],
                'nuts': ['Stout Beer', 'Lager / Pilsner Beer', 'IPA (India Pale Ale) Beer'],
                'beans': ['Wheat / Wit / White Beer'],

                'black pepper': ['Lager / Pilsner Beer'],                                     # spices
                'red pepper': ['Lager / Pilsner Beer', 'Wheat / Wit / White Beer',
                               'IPA (India Pale Ale) Beer', 'Bock Beer'],
                'spicy': ['Lager / Pilsner Beer', 'Wheat / Wit / White Beer', 'Oktoberfest Beer',
                          'IPA (India Pale Ale) Beer', 'Alt, Kolsch Beer'],
                'herbs': ['Bock Beer', 'IPA (India Pale Ale) Beer'],
                'baking spices': ['IPA (India Pale Ale) Beer', 'Blonde Beer', 'Pale Ale Beer'],
                'exotic': ['Lager / Pilsner Beer'],

                'white starches': ['Lager / Pilsner Beer', 'Blonde Beer', 'Pale Ale Beer'],              # starches
                'whole wheat': ['Herb / Spice Beer', 'Quadrupel Beer', 'Stout Beer', 'Barley Wine Beer'],
                'sweet starchy vegetables': [],
                'potato': ['Lager / Pilsner Beer'],

                'fruit': ['Sour / Lambic Beer', 'Fruit Beer', 'Wheat / Wit / White Beer'],               # sweets
                'vanilla': ['Barley Wine Beer', 'Sour / Lambic Beer', 'Fruit Beer'],
                'chocolate': ['Bock Beer', 'Porter Beer', 'Barley Wine Beer', 'Coffee / Chocolate / Honey Beer'],
                'coffee': ['Coffee / Chocolate / Honey Beer']}

# ===== PAIRING UPLOAD ===== #

def food_upload():
    """ Uploads food types that are going to be matched with drinks """
    uploaded_food = {}
    for food in matches:
        cur.execute("""INSERT INTO vrste_hrane(ime)
                        VALUES
                        (%s)
                        RETURNING id
                        """, [food])
        cat_id, = cur.fetchone()
        uploaded_food[food] = cat_id
    connection.commit()
    print('Upload successful!')
    return uploaded_food


food_ids = food_upload()


def pairing_upload():
    """ Uploads food and drink pairings """
    for food in matches:

        for sort in matches[food]:
            pair = {'vrsta_pijace': wine_ids[sort], 'vrsta_hrane': food_ids[food], 'is_perfect': '0'}
            cur.execute("""INSERT INTO priporocila(vrsta_hrane, vrsta_pijace, is_perfect)
                        VALUES
                        (%(vrsta_hrane)s, %(vrsta_pijace)s, %(is_perfect)s)
                        """, pair)

        for sort in perfect_matches[food]:
            pair = {'vrsta_pijace': wine_ids[sort], 'vrsta_hrane': food_ids[food], 'is_perfect': '1'}
            cur.execute("""INSERT INTO priporocila(vrsta_hrane, vrsta_pijace, is_perfect)
                                    VALUES
                                    (%(vrsta_hrane)s, %(vrsta_pijace)s, %(is_perfect)s)
                                    """, pair)

        for sort in beer_matches[food]:
            pair = {'vrsta_pijace': beer_ids[sort], 'vrsta_hrane': food_ids[food], 'is_perfect': '0'}
            cur.execute("""INSERT INTO priporocila(vrsta_hrane, vrsta_pijace, is_perfect)
                                    VALUES
                                    (%(vrsta_hrane)s, %(vrsta_pijace)s, %(is_perfect)s)
                                    """, pair)
    connection.commit()
    print('Pairing upload successful!')


pairing_upload()


# ====================================== #
# VIEWS
# ====================================== #


def search_view():
    cur.execute("""CREATE VIEW search AS
                (SELECT pijaca.id, pijaca.ime, pijaca.drzava, pijaca.velikost, pijaca.stopnja_alkohola, pijaca.slika, vrsta.id AS vrsta, hrana.ime AS hrana FROM pijaca 
                JOIN vrste_pijace AS vrsta ON vrsta.id = pijaca.vrsta
                JOIN priporocila AS p ON vrsta.id = p.vrsta_pijace
                JOIN vrste_hrane AS hrana ON hrana.id = p.vrsta_hrane
                GROUP BY pijaca.id, vrsta.id, hrana.ime)""")
    connection.commit()
    print('Search view created!')


search_view()



