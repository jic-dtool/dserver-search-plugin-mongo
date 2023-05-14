import os

CONFIG_SECRETS_TO_OBFUSCATE = [
    "SEARCH_MONGO_URI",
    "SEARCH_MONGO_DB",
    "SEARCH_MONGO_COLLECTION"
]

class Config(object):
    SEARCH_MONGO_URI = os.environ.get("SEARCH_MONGO_URI", "mongodb://localhost:27017/")
    SEARCH_MONGO_DB = os.environ.get("SEARCH_MONGO_DB", "dtool_info")
    SEARCH_MONGO_COLLECTION = os.environ.get("SEARCH_MONGO_COLLECTION", "datasets")