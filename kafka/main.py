import asyncio
from enum import Enum
from typing import Any

import requests as requests
from pydantic import BaseModel, parse_obj_as, TypeAdapter
import json

from requests import Response

from kafka_consumer import KafkaConsumerClient

url_root = "http://127.0.0.1:8000/"


def send_request(endpoint: str, data: Any, get_or_post: bool) -> Any:
    hs = {'Content-Type': 'application/json'}
    if get_or_post:
        try:
            r = requests.post(f"{url_root}{endpoint}/", json=data.model_dump(), headers=hs)
        except TimeoutError:
            print("The long operation timed out, but we've handled it.")

        # r = requests.post(f"{url_root}{endpoint}/", json=data.model_dump(), headers=hs)
        return r.json()
    else:
        r = requests.get(f"{url_root}{endpoint}/", headers=hs)
        return r.json()


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


# async def do_login(user: User) -> Response:
#     return await send_request("login", user, True)

async def start_consumer():
    # Initialize the consumer client for 'my_topic'
    consumer = KafkaConsumerClient("my_topic")

    print("Starting consumer...")

    # Simulate client session (running for 10 seconds in this example)
    await consumer.consume_for_duration(duration=10)

    print("Consumer has stopped.")


async  def start_main():
    #async def main():
    await start_consumer()

    response = requests.get(url_root)

    name = input("Enter name:")

    user = User(name=name, password='hhh')
    print(user.model_dump_json())

    headers = {'Content-Type': 'application/json'}
    # response = requests.post(f"{url_root}login/", json=user.model_dump(), headers=headers)
    # print(f"Result: {response.status_code}, json={response.json()}")

    #rrr = do_login(user)
    rrr = send_request("login", user, True)

    # user_dict = json.loads(response.json())

    if rrr.status_code != 200:
        print(f"Endpoint error: {rrr.status_code}")
    else:
        ua = UserAccount(**rrr)
    # ua = parse_obj_as(UserAccount, response.json())
    # ua = user = TypeAdapter(UserAccount).validate_json(response.text)
        print(f"{ua.name}, {ua.user_id}, {ua.amount}")

if __name__ == '__main__':
    asyncio.run(start_main())