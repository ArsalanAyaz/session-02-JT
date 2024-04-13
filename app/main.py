from fastapi import FastAPI
from starlette.datastructures import Secret
from sqlmodel import SQLModel, Field, create_engine, Session
from contextlib import asynccontextmanager

# SQLModel give ORM and data validation while BaseModel 
# of pydantic only give data validation


# from app import settings

DATABASE_URL : Secret = "postgresql://neondb_owner:VNvr9OI5wcUb@ep-damp-frost-a5dk94ol.us-east-2.aws.neon.tech/online-todo-server?sslmode=require"



# step 1 : Database schema

class Todo(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    
    # primary_key=True it means that the value of id would be unique and 
    # it would not be repeated in any case . each table would have different id
    
    title : str
    
    
# step 2 : connection to the database

connection_string : str = str(DATABASE_URL).replace(
    "postgresql" , "postgresql+psycopg"  
    
    # '''replacing postgresql with postgresql+psycopg because
    # psycopg is driver which helps on creating and managing connection with database'''
)
engine = create_engine(connection_string) 


# step 3 : creating tables in database

def create_db_table():
    
    print("creating tables")
    SQLModel.metadata.create_all(engine)   
    print("Tables have been created")
    
    
@asynccontextmanager
async def lifesapn(app : FastAPI):
    print("server-startup")
    create_db_table() # above function is calling here
    yield # because it is global funtion
    
app : FastAPI = FastAPI(lifespan=lifesapn)    


@app.get("/")
def Hello() -> str:
    # create_db_table()
    return "Hello World kesi ho aj kal "

@app.get("/db")
def database():
    return {"Database": DATABASE_URL, "connection":connection_string}

@app.post("/add_data")
def create_todo(add_data:Todo):
    with Session(engine) as session:
        session.add(add_data)
        session.commit()
        session.refresh(add_data)
        return add_data
     
    