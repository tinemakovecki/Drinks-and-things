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
        DROP TABLE {};
        """.format(name))
    connection.commit()


def insert_into_table(table_name, new_entry):  # TODO: test!
    """ Inserts an entry into the selected table """

    # getting column names
    column_names = new_entry.keys()
    # piecing together the sql command
    names = ', '.join(column_names)
    values = ""
    for name in column_names:
        values += "%({})s, ".format(name)
    values = values[:-2]
    sql_command = """   INSERT INTO {}
        ({})
        VALUES 
        ({})
    """.format(table_name, names, values)

    # execute the insert
    cur.execute(sql_command,
                new_entry)
    connection.commit()


def upload_data(table, column_names, data_file):
    """ Uploads data from a selected file into a table. The data file has to be in .csv format. """
    with open(data_file, encoding='utf-8') as file:
        read = csv.reader(file, delimiter=';')
        next(read)  # leave out the head line
        for entry in read:
            values = [None if x in ('', '-') else x for x in entry]
            insert_into_table(table, column_names, values)  # TODO: change for new insert function


# open a connection with the database
connection = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


# ====================================== #
# SQL TEXT
# ====================================== #
# All the needed sql strings that will be used for creating the database

vrste_hrane = """   id SERIAL PRIMARY KEY
    ime TEXT UNIQUE
"""

vrste_pijace = """  id SERIAL PRIMARY KEY
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
    vrsta TEXT REFERENCES vrste_pijace(ime),
    cena NUMERIC,
    opis TEXT
"""

# TODO: check if it works correctly
pivo = """    id INTEGER REFERENCES pijaca(id),
    pivovarna TEXT NOT NULL,
    FOREIGN KEY (id) REFERENCES pijaca(id)
"""

vino = """    id INTEGER REFERENCES pijaca(id),
    barva TEXT NOT NULL,
    regija TEXT,
    FOREIGN KEY (id) REFERENCES pijaca(id)
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
    """ Uploads data from the beer file into the database.
    Because of several references etc. it requires a separate function. """
    # preparation
    uploaded_categories = []

    with open('beers.csv', encoding='utf-8') as file:
        read = csv.DictReader(file, delimiter=';')
        next(read)  # leave out the head line
        for entry in read:

            # table vrste_pijace
            if entry['vrsta'] not in uploaded_categories:
                cur.execute("""INSERT INTO vrste_pijace(ime)
                VALUES
                (%s)
                """, [entry['vrsta']])
                connection.commit()
                uploaded_categories.append(entry['vrsta'])

            # table pijaca
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


# execute the upload
# beer_upload()
