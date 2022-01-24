import jsonschema
from pymongo import MongoClient

from main.configs import (
    MONGODB_HOST,
    MONGODB_REPLICA_SET_NAME,
    MONGODB_USERNAME,
    MONGODB_PASSWORD,
    MONGODB_DATABASE,
    DB_COLLECTION,
    get_invoice_schema,
    get_contact_schema,
)


def get_mongodb_collection():
    """
    Establish mongodb connection, create DB and collection
    if they don't exist.

    Returns
    -------
    pymongo.Collection, app_collection.
    """
    client = MongoClient(
        MONGODB_HOST,
        username=MONGODB_USERNAME,
        password=MONGODB_PASSWORD,
        authSource=MONGODB_DATABASE,
        replicaSet=MONGODB_REPLICA_SET_NAME,
    )
    database = client[MONGODB_DATABASE]
    app_collection = database[DB_COLLECTION]
    return app_collection


def validate_invoice_with_schema(doc):
    """
    Validate a doc with invoice schema

    Returns
    -------
    Will raise exceptions if doc is not valide
    """
    schema = get_invoice_schema()
    jsonschema.validate(instance=doc, schema=schema)


def validate_contact_with_schema(doc):
    """
    Validate a doc with contact schema

    Returns
    -------
    Will raise exceptions if doc is not valide
    """
    schema = get_contact_schema()
    jsonschema.validate(instance=doc, schema=schema)
