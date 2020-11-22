import sqlite3
from sqlite3 import Error as SQLiteError
from settings import ROOT_DIR, DB_DIR, DB_FILE, DATA_DIR 

QUERIES = {
    # Table: hourly_prices
    "create_table_hourly_prices": """
        CREATE TABLE IF NOT EXISTS hourly_prices (
            price_time TEXT NOT NULL,
            region TEXT NOT NULL,
            price REAL NOT NULL,
            PRIMARY KEY (price_time, region)
        )
    """,
    
    # Table: named hourly prices
    "create_named_table_hourly_prices": """
        CREATE TABLE IF NOT EXISTS {0} (
            price_time TEXT NOT NULL,
            region TEXT NOT NULL,
            price REAL NOT NULL,
            PRIMARY KEY (price_time, region)
        )
    """,
    
    # Data insertion into hourly_prices
    "insert_hourly_price": """
        INSERT INTO hourly_prices (price_time, region, price)
        VALUES (?, ?, ?)
    """,
    
    # Data insertion into custom hourly prices table
    "insert_named_hourly_price": """
        INSERT INTO {0} (price_time, region, price)
        VALUES (?, ?, ?)
    """,
    
    # Insert - Select
    "insert_from_table": """
        INSERT INTO hourly_prices (price_time, region, price)
            SELECT price_time, region, price 
            FROM {0}
    """,
    
    # Drop table
    "drop table": """
        DROP TABLE IF EXISTS {0};
    """,
}
    

def create_connection(dbfile=None):
    conn = None
    if dbfile == None:
        dbfile = DB_FILE
    try:
        conn = sqlite3.connect(dbfile)
    except SQLiteError as e:
        print(e)
    return conn
    
def create_table(conn, create_table_query):
    """
        Creates table from sql query statement.
        Input parameters:
            create_table_query: CREATE TABLE SQL query
        Return: 0 or 1: 1: success, 0: failure
    """
    operation_result = 0
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        operation_result = 1
    except SQLiteError as e:
        print(e)
    return operation_result

def insert_hourly_price(conn, insert_query, data_tuple):
    try:
        cursor = conn.cursor()
        cursor.execute(insert_query, data_tuple)
        conn.commit()
        return cursor.lastrowid
    except SQLiteError as err:
        print("SQLiteError:\n", err)
        return -1
    
def insert_from_table(conn, insert_query, data_table):
    try:
        cursor = conn.cursor()
        insert_query = insert_query.format(data_table)
        cursor.execute(insert_query)
        conn.commit()
        return 0
    except SQLiteError as err:
        print("SQLiteError:\n", err)
        return -1    
    
def drop_table(conn, table_name):
    try:
        cursor = conn.cursor()
        drop_query = QUERIES['drop_table'].format(table_name)
        cursor.execute(drop_query)
        conn.commit()
        return 0
    except SQLiteError as err:
        print("SQLiteError:\n", err)
        return -1      
    
def select_data(conn, query, query_params_tuple = None):
    cur = conn.cursor()
    if query_params_tuple:
        cur.execute(query, query_params_tuple)
    else:
        cur.execute(query)
    rows = cur.fetchall()
    return rows
        

