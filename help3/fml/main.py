import asyncio
from enum import Enum
from typing import List

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from requests import Request
from starlette.responses import JSONResponse


class OurException(Exception):
    def __init__(self, msg: str):
        self.message = msg

class Role(Enum):
    ADMIN = 0
    REGULAR = 1


class User(BaseModel):
    name: str | None
    password: str | None


class UserAccount(BaseModel):
    user_id: int
    name: str
    amount: int
    role_id: int
    role: Role


app = FastAPI()

@app.exception_handler(OurException)
async def our_exception_handler(request: Request, ex: OurException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {ex.message} did something. What a..."},
    )

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/user/{user_id}")
async def get_user(user_id: int):
    if user_id == 0:
        raise OurException("ffffffff")

    if user_id % 2 == 0:
        return {"message": "Hello ty!"}
    else:
        return {"message": "Go away now!"}


# @app.get("/user/login/{name}/{password}")
# async def login_user(name: str, password: str):
#     if password == "ty":
#         return UserAccount(name=name, user_id=100, amount=2000)
#     else:
#         return {"message": "Go away now!"}


@app.post("/login/")
async def login(user: User) -> UserAccount:
    print(f"Login user {user.name}...")
    ua = UserAccount(name=user.name, user_id=100, amount=2000, role_id=0, role=Role.ADMIN)
    await asyncio.sleep(5)
    print(f"User {user.name} logged-in")
    return ua


# bulk

@app.post("/bulk_login/")
async def login_bulk(user: List[User]) -> List[UserAccount]:
    users = []
    # for u in user:
    #     ua = UserAccount(name=u.name, user_id=100, amount=2000)
    #     users.append(ua)
    # return users
    queue = asyncio.Queue()
    # run the producer and consumers
    await asyncio.gather(producer(queue, user), consumer(queue, users))

    # with tasks:

    # # start the consumer
    # _ = asyncio.create_task(consumer(queue))
    # # start the producer and wait for it to finish
    # await asyncio.create_task(producer(queue))
    # # wait for all items to be processed
    # await queue.join()

    return users


async def producer(queue: asyncio.Queue, users: List[User]):
    for u in users:
        await asyncio.sleep(1)
        await queue.put(u)
    await queue.put(None)


async def consumer(queue: asyncio.Queue, users: List[UserAccount]):
    current = 1
    while True:
        # user = await queue.get()
        try:
            user = queue.get_nowait()
        except asyncio.QueueEmpty:
            print('Consumer: got nothing, waiting a while...')
            await asyncio.sleep(0.5)
            continue

        if user is None:
            break
        user = UserAccount(name=user.name, password=user.password, amount=10, user_id=current, role_id=2,
                           role=Role.REGULAR)
        users.append(user)
        current += 1

# end of bulk




if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)
