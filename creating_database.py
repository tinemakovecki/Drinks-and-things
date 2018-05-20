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


def insert_into_table(table_name, column_names, entry_values):
    """ Inserts an entry into the selected table """

    # column names and entry values are lists
    names = ', '.join(column_names)
    values = ', '.join(entry_values)

    cur.execute("""
        INSERT INTO {}
        ({})
        VALUES 
        ({})
        """.format(table_name, names, values))
    connection.commit()


def upload_data(table, column_names, data_file):
    """ Uploads data from a selected file into a table. The data file has to be in .csv format. """
    with open(data_file) as file:
        read = csv.DictReader(file)
        next(read)  # leave out the head line
        for entry in read:
            values = [None if x in ('', '-') else x for x in entry]
            insert_into_table(table, column_names, values)


# open a connection with the database
connection = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


# ====================================== #
# SQL TEXT
# ====================================== #
# All the needed sql strings that will be used for creating the database

vrste_hrane = """   ime TEXT PRIMARY KEY
"""

vrste_pijace = """  ime TEXT PRIMARY KEY
"""

# price = None usually means the drink is discontinued or unavailable
# pivo_id = None -> the drink is a wine
# vino_id = None -> the drink is a beer
pijaca = """    id SERIAL PRIMARY KEY,
    ime TEXT NOT NULL,
    drzava TEXT NOT NULL,
    velikost INTEGER NOT NULL,
    stopnja_alkohola NUMERIC NOT NULL,
    vrsta TEXT REFERENCES vrste_pijace(ime),
    pivo_id INTEGER REFERENCES pivo(id),
    vino_id INTEGER REFERENCES vino(id),
    cena NUMERIC,
    opis TEXT
"""

pivo = """id SERIAL PRIMARY KEY,
    pivovarna TEXT NOT NULL
"""

vino = """  id SERIAL PRIMARY KEY,
    barva TEXT NOT NULL,
    regija TEXT
"""

priporocila = """   id SERIAL PRIMARY KEY,
    vrsta_hrane TEXT REFERENCES vrste_hrane(ime),
    vrsta_pijace TEXT REFERENCES vrste_pijace(ime)
"""

# ====================================== #
# EXECUTION
# ====================================== #

# creating the tables:
# create_table('vrste_hrane', vrste_hrane)
# create_table('vrste_pijace', vrste_pijace)
# create_table('priporocila', priporocila)
# create_table('pivo', pivo)
# create_table('vino', vino)
# create_table('pijaca', pijaca)
