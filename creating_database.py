# ====================================== #
# IMPORTS
# ====================================== #


# import authorization info
import auth
auth.db = "sem2018_%s" % auth.user

# import psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # bcoz šumniki

import csv

# ====================================== #
# FUNCTIONS
# ====================================== #


def create_table(name, sql_description):
    ''' Create a table with a given name from a given sql description '''
    cur.execute("""" 
        CREATE TABLE name(
        {});
        """.format(name, sql_description))
    connection.commit()


def delete_table(name):
    ''' Deletes a table '''
    cur.execute("""
        DROP TABLE {};
        """.format(name))
    connection.commit()


def insert_into_table(table_name, column_names, entry_values):
    ''' Inserts an entry into the selected table '''
    cur.execute("""
        INSERT INTO {}
        ({})
        VALUES 
        ({})
        """.format(table_name, column_names, entry_values))
    connection.commit()

def upload_data(table, column_names, data_file):
    ''' Uploads data from a selected file into a table. The data file has to be in .csv format. '''
    with open(data_file) as file:
        read = csv.reader(file)
        next(read)  # leave out the head line
        for entry in read:
            # TODO: scrape values from entry
            insert_into_table(table, column_names, values)

            


connection = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
