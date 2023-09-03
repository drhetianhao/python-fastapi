import uvicorn
from fastapi import Body, FastAPI, Depends
from app.model import PostSchema
from app.model import PostSchema, UserLoginSchema, UserSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer

posts = [
    {"id": 1, "title": "penguins", "text": "some texts"},
    {"id": 2, "title": "tigers", "text": "some tigers"},
    {"id": 3, "title": "koalas", "text": "kkkkkkk"},
]

users = []

app = FastAPI()


# get testing
@app.get("/", tags=["test"])
def greet():
    return {"Hello": "World!"}


@app.get("/posts", tags=["posts"])
def get_posts():
    return {"data": posts}


@app.get("/posts/{id}", tags=["posts"])
def get_one_post(id: int):
    if id > len(posts):
        return {"msg": "not exist"}
    for post in posts:
        if post["id"] == id:
            return {"data": post}


@app.post("/posts", dependencies=[Depends(jwtBearer())], tags=["posts"])
def add_post(post: PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {"info": "Post Added!"}


# user sign up
@app.post("/user/signup", tags=["user"])
def user_signup(user: UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.email)


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False


@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return {"error": "invalid login"}
