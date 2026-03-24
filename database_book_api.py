
################________FOR BOOK_________###################

from sqlalchemy import create_engine, MetaData,Table,Column,Integer,VARCHAR,Float,ForeignKey,insert,select, delete, update

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

app = Flask(__name__)

@app.route("/books", methods = ["GET","POST", "PUT","DELETE"])
def get_books():
    if request.method == "GET":
        with engine.connect() as conn:
            result = conn.execute(select(book))
            books = [] # list 
        for row in result:
            # Access columns by attribute
            books.append({
                "book_id":row.book_id,
                "title":row.title,
                "author_id": row.author_id,
                "price": row.price
            })
        return jsonify(books)
    
    ##Get all books with author info...

    if request.method == "POST":
        data = request.json
        with engine.begin() as conn:
            conn.execute(
                insert(book).values(
                    book_id=data["book_id"],
                    title=data["title"],
                    price=data["price"],
                    author_id=data["author_id"]   
                )
            )
        return {"message": "Book added successfully"}
    
    if request.method == "PUT":
        data = request.json
        with engine.begin() as conn:
            conn.execute(
                update(book)
                .where(book.c.book_id == data["book_id"])
                .values(
                    title=data.get("title"),
                    price=data.get("price"),
                    author_id=data.get("author_id")
                )
            )
        return jsonify({"message": "Book updated successfully"})
    
    if request.method == "DELETE":
        data = request.json
        with engine.begin() as conn:
            conn.execute(
                delete(book).where(book.c.book_id == data["book_id"])
            )
        return jsonify({"message": "Book deleted successfully"})


####____GETTING All BOOKS WITH AUTHOR INFO______#####

@app.route("/bookss/<int:author_id>", methods=["GET"])
def get_books_by_author_info(author_id):
    with engine.connect() as conn:
        result = conn.execute(
            select(
                book.c.book_id,
                book.c.title,
                book.c.price,
                author.c.author_id,
                author.c.name,
                author.c.email
            )
            .join(author, book.c.author_id == author.c.author_id)
            .where(author.c.author_id == author_id)  # filter by author
        )

        books_list = []
        author_info = None

        for row in result:
            if not author_info:
                author_info = {
                    "author_id": row.author_id,
                    "name": row.name,
                    "email": row.email,
                    "books": []
                }
            author_info["books"].append({
                "book_id": row.book_id,
                "title": row.title,
                "price": row.price
            })
    if not author_info:
        return jsonify({"error": "Author not found"})
    return jsonify(author_info)

# This is for to dump book in json disk ....
@app.route("/dump/books",methods = ["POST"])
def dump_book():
    with engine.connect() as conn:
        result = conn.execute(select(book))
        books = [dict(row) for row in result.mappings().all()]

    os.makedirs("dumps", exist_ok=True)
    with open("dumps/books_dump.json", "w") as f:
        json.dump(books, f, indent=4)
    return{ 
        "message": "Books dumped successfully"
    }