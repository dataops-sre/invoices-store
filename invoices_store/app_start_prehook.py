from pymongo import MongoClient
import os

MONGODB_HOST = os.getenv("MONGODB_HOST", "mongodb://localhost:27017/")

"""
It is to be run in entrypoint.sh
"""


def health_check():
    try:
        client = MongoClient(MONGODB_HOST)
        client.server_info()
        return 200
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print(f"Mongodb Service {MONGODB_HOST} is not ready yet")
        return -1
    else:
        print(f"Mongodb service {MONGODB_HOST} is up!")
        return 200


if __name__ == "__main__":

    def main():
        while health_check() != 200:
            time.sleep(1)
