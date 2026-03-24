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


### _________FOR AUTHOR____________###

@app.route("/authors/<int:author_id>", methods = ["GET"])
def get_authors_by_id(author_id):
    with engine.connect() as conn:
        result = conn.execute(select(author).where(author.c.author_id == author_id)).fetchone()
        # Access columns by attribute
        authors_data={
        "author_id": result.author_id,
        "name":result.name, 
        "email": result.email 
        }
    return jsonify(authors_data)

@app.route("/authors", methods = ["GET","POST","PUT","DELETE"])
def get_authors():
    if request.method == "GET":
        with engine.connect() as conn:
            result = conn.execute(select(author))
            authors = [] # list 
            for row in result:
            # Access columns by attribute
                authors.append({
                    "author_id": row.author_id,
                    "name": row.name,
                    "email": row.email
            })
        return jsonify(authors)
    
    if request.method == "POST": 
        data = request.json
        with engine.begin() as conn:
            conn.execute(
                insert(author).values(
                    author_id=data["author_id"],
                    name=data["name"],
                    email = data["email"]
                    
                )
            )
            
        return jsonify({"message": "Author added successfully"})
    
    
    if request.method == "DELETE":
        data = request.json
        author_id = data["author_id"]

        with engine.begin() as conn:
            conn.execute(
                delete(author).where(author.c.author_id == author_id)
            )
        return jsonify(
            {
            "message": "Author deleted successfully"
            }
        )
    
# This is for to dump in json to disk ....
@app.route("/dump/authors",methods = ["POST"])
def get_auhtor():
    with engine.connect() as conn:
        result = conn.execute(select(author))
        result1 = [dict(row) for row in result.mappings().all()]

    os.makedirs("dumps", exist_ok=True)
    with open("dumps/authors_dump.json", "w") as f:
        json.dump(result1, f, indent=4)
    return{ 
        "message": "Author dumped successfully"
    }