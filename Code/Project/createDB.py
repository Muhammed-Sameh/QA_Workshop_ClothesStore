import db
import sqlite3
from msilib.schema import tables
from db import get_db, close_db 

def create_users_tables():
    connect_db = get_db()

    try: 
        #Create Table
        connect_db.execute("""CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            role TEXT NOT NULL
            );""")
    except Exception as err:
        print("Users Table is Created Before", str(err))

    connect_db.commit()
    close_db(connect_db) 
create_users_tables()           


def create_movies_table():
    connect_db = get_db()

    try: 
        cursor = connect_db.cursor()

        #Create Table
        cursor.execute("""CREATE TABLE product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sizes TEXT NOT NULL,
            description TEXT NOT NULL,
            color TEXT NOT NULL,
            quantity TEXT NOT NULL,
            price TEXT NOT NULL,
            image BLOB NOT NULL);""")

    except Exception as err:
        print("Product Table is Created Before", str(err))

    connect_db.commit()
    close_db(connect_db) 
create_movies_table() 

def create_buy_table():
    connect_db = get_db()

    try: 
        #Create Table
        connect_db.execute("""CREATE TABLE buy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT NOT NULL,
            email TEXT NOT NULL,
            date TEXT NOT NULL,
            quantity TEXT NOT NULL
            );""")
    except Exception as err:
        print("Buy Table is Created Before", str(err))

    connect_db.commit()
    close_db(connect_db) 
create_buy_table()   


def convertToBinaryData(filename):
	
	# Convert binary format to images or files data
	with open(filename, 'rb') as file:
		blobData = file.read()
	return blobData


def insertIntoDB(name, sizes, description, color, quantity, price, image):
    connect_db = get_db()

    try: 
        #Create Table
        cursor =  connect_db.cursor()
        sqlite_insert_blob_query = """ INSERT INTO product
                                  (name, sizes, description, color, quantity, price, image) VALUES (?, ?, ?, ?, ?, ?, ?);"""
        product_img = convertToBinaryData(image)
        data_tuple = (name, sizes, description, color, quantity, price, product_img)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        connect_db.commit()
        print("Image and file inserted successfully as a BLOB into a table")

        close_db(cursor) 

    except Exception as err:
        print("Failed to insert blob data into sqlite table", str(err))
    


def create_favorite_tables():
    connect_db = get_db()

    try: 
        #Create Table
        connect_db.execute("""CREATE TABLE cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT NOT NULL,
            email TEXT NOT NULL);""")
    except Exception as err:
        print("Cart Table is Created Before", str(err))

    connect_db.commit()
    close_db(connect_db) 
create_favorite_tables()

#### Adding Data In movies_data #####
#(name, sizes, description, color, quantity, image)
insertIntoDB("Accessory 1", "S", "Al Karam", "Silver", "3","95.50 $" ,"static//images//Accessory 1.png")
insertIntoDB("Accessory 2", "M", "Al Karam", "Silver", "3","85.00 $" ,"static//images//Accessory 2.png")
insertIntoDB("Accessory 3", "S", "Al Karam", "Golden", "3","90.50 $" ,"static//images//Accessory 3.png")
insertIntoDB("Accessory 4", "M", "Al Karam", "Silver", "3","198.00 $" ,"static//images//Accessory 4.png")
insertIntoDB("Accessory 5", "S", "Al Karam", "Silver", "3","89.50 $" ,"static//images//Accessory 5.png")
insertIntoDB("Accessory 6", "M", "Al Karam", "Silver", "3","97.00 $" ,"static//images//Accessory 6.png")

insertIntoDB("Long Dress", "M", "Al Karam", "White", "4","95.00 $" ,"static//images//Long Dress.png")
insertIntoDB("Colorful Dress", "M", "Al Karam", "Blue", "4","76.00 $" ,"static//images//Colorful Dress.png")
insertIntoDB("Shiny Dress", "M", "Al Karam", "Golden", "4","99.50 $" ,"static//images//Shiny Dress.png")
insertIntoDB("White Dress", "M", "Al Karam", "White", "4","155.00 $" ,"static//images//White Dress.png")
insertIntoDB("White Shirt", "M", "Al Karam", "White", "4","93.50 $" ,"static//images//White Shirt.png")
insertIntoDB("Colorful Dress", "M", "Al Karam", "White", "4","98.00 $" ,"static//images//Colorful Dress.png")