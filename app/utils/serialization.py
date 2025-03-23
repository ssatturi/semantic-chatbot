from bson import ObjectId
from typing import List, Union


def serialize_mongo_document(doc: dict) -> dict:
    """
    Convert a single MongoDB document to a JSON serializable format.
    """
    doc = dict(doc)  # Ensure it's a dict in case it's a pymongo Cursor object
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
        elif isinstance(value, dict):
            doc[key] = serialize_mongo_document(value)
        elif isinstance(value, list):
            doc[key] = serialize_mongo_documents(value)
    return doc


def serialize_mongo_documents(docs: Union[List[dict], List[object]]) -> List[dict]:
    """
    Convert a list of MongoDB documents to a JSON serializable format.
    """
    return [serialize_mongo_document(doc) for doc in docs]
