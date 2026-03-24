from sqlalchemy  import create_engine, MetaData,text, Table, Column,select, Integer,Float,String,VARCHAR,ForeignKey, insert


from dotenv import load_dotenv
import os 
load_dotenv()

DB_NAME = os.environ.get("DB_NAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_USER = os.environ.get("DB_USER")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_SCHEMA =os.environ.get("DB_SCHEMA")

CONNECTION_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(CONNECTION_URL)
metadata = MetaData(schema = DB_SCHEMA )

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

metadata.create_all(engine)
print("Table has been succesfully creared..")