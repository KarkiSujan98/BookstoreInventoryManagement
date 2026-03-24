from sqlalchemy import create_engine, MetaData,Table,Column,Integer,VARCHAR,Float,ForeignKey,insert,select

from flask import Flask,jsonify,request, json
from dotenv import load_dotenv
import os 

load_dotenv()

DB_NAME = os.environ.get("DB_NAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_USER = os.environ.get("DB_USER")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_SCHEMA =os.environ.get("DB_SCHEMA")

CONNECTION_URL =f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(CONNECTION_URL)
metadata = MetaData(schema = DB_SCHEMA)
author = Table(
    "author", metadata,
    Column("author_id",Integer, primary_key = True),
    Column("name",VARCHAR(100)),
    Column("email",VARCHAR(100))
)

book = Table(
    "book", metadata,
    Column("book_id", Integer, primary_key=True),
    Column("title", VARCHAR(20)),
    Column("price",Float),
    Column("author_id", Integer,ForeignKey("author.author_id")),

) 

# This program let us use terminal to insert data in database 
#metadata.create_all(engine)
print("Choose what to insert:")
print("1. Author")
print("2. Book")

choice = int(input("Enter choice (1 or 2): "))

with engine.connect() as conn:
    if choice == 1:
        author_id = int(input("Enter author ID: "))
        name = input("Enter author name: ")
        email = input("Enter author email: ")

        result1 = insert(author).values(
            author_id=author_id,
            name=name,
            email=email
        )
        conn.execute(result1)
        conn.commit()
        print("Author inserted successfully")

    elif choice == 2:
        book_id = int(input("Enter book ID: "))
        title = input("Enter book title: ")
        price = float(input("Enter book price: "))
        author_id = int(input("Enter author ID (must exist): "))

        result2 = insert(book).values(
            book_id=book_id,
            title=title,
            price=price,
            author_id=author_id
        )
        conn.execute(result2)
        conn.commit()
        print("Book inserted successfully")

    else:
        print(" Invalid choice ")
