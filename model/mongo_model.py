from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError

class MongoModel:
    def __init__(self, uri):
        """Inicializa la conexión de MongoDB con la URI proporcionada"""
        self.uri = uri
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        """Establece la conexión con MongoDB"""
        try:
            # Crear una instancia del cliente de MongoDB con la URI de conexión
            self.client = MongoClient(self.uri, server_api=ServerApi('1'))
            self.db = self.client.get_database('libreria')  # Especifica la base de datos 'libreria'
            self.collection = self.db.reviews  # Accede a la colección 'reviews'
            print("Conexión exitosa a MongoDB.")
        except Exception as e:
            print(f"Error al conectar con MongoDB: {e}")

    def start_transaction(self):
        """Inicia una nueva transacción en MongoDB"""
        # Inicia una sesión para la transacción
        session = self.client.start_session()
        session.start_transaction()  # Inicia la transacción
        return session

    def commit_transaction(self, session):
        """Confirma una transacción en MongoDB"""
        try:
            session.commit_transaction()
            print("Transacción confirmada.")
        except PyMongoError as e:
            print(f"Error al confirmar la transacción: {e}")
            session.abort_transaction()  # En caso de error, aborta la transacción

    def abort_transaction(self, session):
        """Aborta una transacción en MongoDB"""
        try:
            session.abort_transaction()
            print("Transacción abortada.")
        except PyMongoError as e:
            print(f"Error al abortar la transacción: {e}")

    def fetch_reviews(self, book_id):
        """Obtiene las reseñas de un libro desde MongoDB"""
        try:
            reviews = self.collection.find({"book_id": book_id})  # Filtra las reseñas por `book_id`
            return list(reviews)  # Devuelve las reseñas como una lista
        except Exception as e:
            print(f"Error al obtener las reseñas de MongoDB: {e}")
            return []

    def add_review(self, book_id, review_text, session=None):
        """Agrega una nueva reseña a MongoDB dentro de una transacción"""
        try:
            review_data = {
                "book_id": book_id,
                "review": review_text
            }
            # Si se proporciona una sesión, realiza la operación dentro de la transacción
            if session:
                self.collection.insert_one(review_data, session=session)
            else:
                self.collection.insert_one(review_data)  # Sin transacción
            print("Reseña agregada exitosamente.")
        except Exception as e:
            print(f"Error al agregar la reseña: {e}")
            if session:
                session.abort_transaction()  # Aborta la transacción si hay un error

