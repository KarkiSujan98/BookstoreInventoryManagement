from  sqlalchemy  import create_engine , MetaData, Column, Integer, Table,VARCHAR,Float,ForeignKey, select,update


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
print("Choose what to insert:")
print("1. Author")
print("2. Book")

choice = int(input("Enter choice (1 or 2): "))

with engine.connect() as conn:
    if choice == 1:
        author_id = int(input("Enter Author ID: "))
        new_email = input("Enter new email: ")
        conn.execute(update(author).where(author.c.author_id == author_id).values(email=new_email))
        conn.commit()
        print("Author email updated!")

    elif choice == 2:
        book_id = int(input("Enter Book ID: "))
        new_price = float(input("Enter new price: "))
        conn.execute(update(book).where(book.c.book_id == book_id).values(price=new_price))
        conn.commit()
        print("Book price updated!")

    else: 
        print("Invalid choice")
