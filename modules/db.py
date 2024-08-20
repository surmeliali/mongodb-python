import configparser
from pymongo import MongoClient

def getConfig():
    print("Reading Config file")
    config = configparser.ConfigParser()
    config.readfp(open('mongo-project.conf','r'))
    return config

def connect(config):
    host = config.get('mongo','host')
    port = config.get('mongo','port')
    database = config.get('mongo','database')
    collection = config.get('mongo','collection')

    # Build the uri to connect
    dburi = "mongodb://" + host + ":" + port + "/" + database

    # dburi = $"mongodb://{host}:{port}/{database}"
    print("Attempting to connect to: " + dburi)
    client = MongoClient(dburi)
    return client[database]

