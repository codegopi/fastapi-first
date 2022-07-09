from sys import modules
from typing import Optional
from colorama import Cursor
from fastapi import FastAPI, Query, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2 
from psycopg2.extras import RealDictCursor
import time
#from requests import Session
from . import models
from .database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session

#when you run this file, this line will create a new table if it doesn't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()



#to define the scheme and validate the inputs received
class Post(BaseModel):
    title: str
    content: str
    published: bool = True #optional value by default is True
    #rating: Optional[int] = None #optional value

#to connect to database
#while loop till the database is connected
while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database='fastapi', user='postgres', password='maran.28', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("connecting to database failed")
        print("Error: ", error)
        time.sleep(2) #retry connection after 2 seconds

#to store the data temperarily
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite food", "content": "I like pizza", "id": 2}]


def find_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/") #/ i the url eg /posts etc
def root():
    
    return {"message": "Hello World"}

#this is a test link
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    #sql query to fetch all post
    posts = db.query(models.Posts).all()
    return {"data": posts}

@app.get("/posts") #/ i the url eg /posts etc
def root(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts """)
    #posts = cursor.fetchall()
    posts = db.query(models.Posts).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
#def create_posts(payload: dict = Body(...)): 
def create_posts(post: Post, db: Session=Depends(get_db)): #saving Post class as post variable
    #gets data from body, converts as dictionary and stores in payload(variable)
    #print(payload)
    #return {"new_post": f"title: {payload['title']} content: {payload['content']}"}
    #print(post)
    #print(post.dict()) chaging from pydantic to dictionary
    #post_dict = post.dict()
    #post_dict['id'] = randrange(0, 1000000)
    #my_posts.append(post_dict)


    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) """, (post.title, post.content, post.published) )
    #new_post = cursor.fetchone
    #conn.commit()
    
    #new_post = models.Posts(title=post.title, content=post.content, published=post.published)
    #the following will do same as above but we dont have to type each row
    new_post = models.Posts(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response): #to get 1 particular post and validate that id is number
    #post = find_posts(int(id))
    cursor.execute("""SELECT * FROM POSTS WHERE id = %s""", (str(id),))
    test_post = cursor.fetchone()
    print(test_post)
    post = find_posts(id)
    if not post: #if post is not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} was not found"}
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    #find the index of the post and pop the index
    index = find_index_post(id)
    conn.commit()
    #if the post id doesn't exist
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesnot exists")
    #my_posts.pop(index)
    #return {"message": "post was successfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    #index = find_index_post(id)
    #if the post id doesn't exist
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesnot exists")
    #post_dict = post.dict()
    #post_dict['id'] = id
    #my_posts[index] = post_dict
    return {"data": updated_post}
