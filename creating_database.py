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
    # we format the "values" part of the string
    # so that .execute() will be able to insert parameters into the command
    values = ""
    for name in column_names:
        values += "%({})s, ".format(name)
    values = values[:-2]
    # format the parts together
    sql_command = """   INSERT INTO {}
        ({})
        VALUES 
        ({})
    """.format(table_name, names, values)

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

vrste_pijace = """  id SERIAL PRIMARY KEY,
    ime TEXT UNIQUE
"""

# price = None usually means the drink is discontinued or unavailable
# pivo_id = None -> the drink is a wine
# vino_id = None -> the drink is a beer
pijaca = """    id SERIAL PRIMARY KEY,
    ime TEXT NOT NULL,
    drzava TEXT NOT NULL,
    velikost NUMERIC NOT NULL,
    stopnja_alkohola NUMERIC NOT NULL,
    vrsta INTEGER REFERENCES vrste_pijace(id),
    cena NUMERIC,
    opis TEXT
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

priporocila = """   id SERIAL PRIMARY KEY,
    vrsta_hrane INTEGER REFERENCES vrste_hrane(id),
    vrsta_pijace INTEGER REFERENCES vrste_pijace(id)
"""

# ====================================== #
# EXECUTION
# ====================================== #

# CREATING THE TABLES:
# create_table('vrste_hrane', vrste_hrane)
# create_table('vrste_pijace', vrste_pijace)
# create_table('priporocila', priporocila)
# create_table('pijaca', pijaca)
# create_table('pivo', pivo)
# create_table('vino', vino)


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
                connection.commit()
                uploaded_categories[entry['vrsta']] = cat_id

            # table pijaca
            if entry['cena'] == '':
                entry['cena'] = None

            # switch the dictionary to contain vrsta id
            entry['vrsta'] = uploaded_categories[entry['vrsta']]

            cur.execute("""INSERT INTO
                pijaca(ime, vrsta, velikost, stopnja_alkohola, drzava, cena, opis)
            VALUES
                (%(ime)s, %(vrsta)s, %(velikost)s, %(stopnja_alkohola)s, %(drzava)s, %(cena)s, %(opis)s)
            RETURNING id
            """, entry)
            return_id, = cur.fetchone()
            connection.commit()

            # table pivo
            pivce = {'id': return_id, 'pivovarna': entry['pivovarna']}
            cur.execute("""INSERT INTO pivo(id, pivovarna)
            VALUES
            (%(id)s, %(pivovarna)s)
            """, pivce)
            connection.commit()

    print('Upload successful!')


def wine_upload():
    """ Uploads data from the wine file into the database. """
    # we'll keep a dictionary of uploaded categories and their ids
    uploaded_categories = {}

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
                connection.commit()
                uploaded_categories[entry['vrsta']] = cat_id

            # table pijaca
            if entry['stopnja_alkohola'] == '':
                entry['stopnja_alkohola'] = None

            # switch the dictionary to contain vrsta id
            entry['vrsta'] = uploaded_categories[entry['vrsta']]

            cur.execute("""INSERT INTO
                pijaca(ime, vrsta, velikost, stopnja_alkohola, drzava, cena, opis)
            VALUES
                (%(ime)s, %(vrsta)s, %(velikost)s, %(stopnja_alkohola)s, %(drzava)s, %(cena)s, %(opis)s)
            RETURNING id
            """, entry)
            return_id, = cur.fetchone()
            connection.commit()

            # table vino
            vince = {'id': return_id, 'barva': entry['barva'], 'regija': entry['regija']}
            cur.execute("""INSERT INTO vino(id, barva, regija)
            VALUES
            (%(id)s, %(barva)s, %(regija)s)
            """, vince)
            connection.commit()

    print('Upload successful!')


# execute the upload
# beer_upload()
wine_upload()