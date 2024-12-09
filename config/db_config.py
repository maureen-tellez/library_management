import pymysql
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Configuración para MySQL
def get_mysql_connection():
    return pymysql.connect(
        host="localhost",
        user="maureentellez",
        password="1603",
        database="libreria",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

# Configuración para MongoDB
def get_mongo_connection():
    uri = "mongodb+srv://maureenbarra16:<db_password>@cluster0.ifap9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Conexión exitosa a MongoDB.")
    except Exception as e:
        print("Error conectando a MongoDB:", e)
    return client
