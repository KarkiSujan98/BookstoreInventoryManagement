from sqlalchemy import create_engine, MetaData,Table, Column,VARCHAR,Integer,Float,ForeignKey,delete

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
with engine.connect() as conn:
    print(" Delete Menu:")
    print(" 1. Delete Book")
    print(" 2. Delete Author (and their books)")
    
    choice = int(input("Enter choice: "))

    if choice == 1:
        book_id = int(input("Enter Book ID to delete: "))
        conn.execute(delete(book).where(book.c.book_id == book_id))
        conn.commit()
        print("Book deleted.")

    elif choice == 2:
        author_id = int(input("Enter Author ID to delete: "))
        # delete books of author
        conn.execute(delete(book).where(book.c.author_id == author_id))
        # delete author
        conn.execute(delete(author).where(author.c.author_id == author_id))
        conn.commit()
        print("Author and related books deleted.")

    else:
        print("Invalid choice")