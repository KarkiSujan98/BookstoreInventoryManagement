from  sqlalchemy  import create_engine , MetaData, Column, Integer, Table,VARCHAR,Float,ForeignKey, select 


# for hiding data base detail from files 
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

# creating table 
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
print("Choose what to insert:")
print("1. Author")
print("2. Book")

choice = int(input("Enter choice (1 or 2): "))

with engine.connect() as conn:
    if choice == 1:
        author_id = int(input("Enter author id: "))

        result = conn.execute(
        select(author).where(author.c.author_id == author_id)
        ).fetchone()

        if result:
            print(dict(result._mapping))   # pretty output
        else:
            print("Author not found")

    elif choice == 2:
        book_id = int(input("Enter the book id: "))
        result = conn.execute(
        select(book).where(book.c.book_id == book_id)
        ).fetchone()

        if result:
        # show as dictionary
            print(dict(result._mapping))   
        else:
            print("Book not found")

    else:
        print(" Invalid choice ")
