import psycopg2
from psycopg2 import sql
import os
from psycopg2.extras import RealDictCursor

class PostgreSQLModel:
    def __init__(self, host=None, user=None, password=None, database=None, port=None):
        self.host = host or os.getenv("DB_HOST", "localhost")
        self.user = user or os.getenv("DB_USER", "maureentellez")
        self.password = password or os.getenv("DB_PASSWORD", "1603")
        self.database = database or os.getenv("DB_NAME", "Libreria")
        self.port = port or os.getenv("DB_PORT", 5432)
        self.connection = None

    def connect(self):
        """Establece la conexión con la base de datos PostgreSQL"""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            self.connection.autocommit = False  # Desactivar autocommit para manejar transacciones manualmente
            print("Conexión exitosa a la base de datos PostgreSQL.")
        except psycopg2.OperationalError as e:
            print(f"Error al conectar con la base de datos: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def test_connection(self):
        """Verifica la conexión a la base de datos PostgreSQL"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()
            if result:
                print("Conexión a PostgreSQL verificada exitosamente.")
            else:
                print("Error al verificar la conexión a PostgreSQL.")
        except psycopg2.Error as e:
            print(f"Error al verificar la conexión: {e}")
        finally:
            cursor.close()

    def close_connection(self):
        """Cierra la conexión con la base de datos"""
        if self.connection:
            self.connection.close()
            print("Conexión cerrada.")

    def begin_transaction(self):
        """Inicia una nueva transacción"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("BEGIN;")
        except Exception as e:
            print(f"Error al iniciar la transacción: {e}")

    def commit_transaction(self):
        """Confirma la transacción actual"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("COMMIT;")
        except Exception as e:
            print(f"Error al confirmar la transacción: {e}")

    def rollback_transaction(self):
        """Deshace la transacción actual"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("ROLLBACK;")
        except Exception as e:
            print(f"Error al deshacer la transacción: {e}")

    def add_book(self, id_book, title, isbn, year_of_publication, language, editorial_id, author_id):
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO books (id_book, title, isbn, year_of_publication, language, editorial_id_editorial, author_id_author)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            print(f"Ejecutando consulta: {query}")
            print(f"Con valores: {id_book}, {title}, {isbn}, {year_of_publication}, {language}, {editorial_id}, {author_id}")
            cursor.execute(query, (id_book, title, isbn, year_of_publication, language, editorial_id, author_id))
            self.connection.commit()
            print("Libro agregado correctamente a la base de datos.")
        except psycopg2.Error as e:
            print(f"Error al agregar el libro: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    def add_editorial(self, id_editorial, name, country_of_origin, year_established):
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO editorial (id_editorial, name, country_of_origin, year_established)
                VALUES (%s, %s, %s, %s)
            """
            print(f"Ejecutando consulta: {query}")
            print(f"Con valores: {id_editorial}, {name}, {country_of_origin}, {year_established}")
            cursor.execute(query, (id_editorial, name, country_of_origin, year_established))
            self.connection.commit()
            print("Editorial agregada correctamente a la base de datos.")
        except psycopg2.Error as e:
            print(f"Error al agregar la editorial: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    def add_author(self, id_author, name, nationality, year_of_birth, year_of_death=None):
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO authors (id_author, name, nationality, year_of_birth, year_of_death)
                VALUES (%s, %s, %s, %s, %s)
            """
            print(f"Ejecutando consulta: {query}")
            print(f"Con valores: {id_author}, {name}, {nationality}, {year_of_birth}, {year_of_death}")
            cursor.execute(query, (id_author, name, nationality, year_of_birth, year_of_death))
            self.connection.commit()
            print("Autor agregado correctamente a la base de datos.")
        except psycopg2.Error as e:
            print(f"Error al agregar el autor: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    def execute_query(self, query, params=None):
        """Ejecuta una consulta SQL"""
        if not self.connection:
            print("Error: No se ha establecido una conexión con la base de datos.")
            return
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                self.connection.commit()
        except psycopg2.DatabaseError as e:
            print(f"Error al ejecutar la consulta: {e}")
            self.connection.rollback()
        except Exception as e:
            print(f"Error inesperado: {e}")

    def fetchall(self, query, params=None):
        """Obtiene todos los resultados de una consulta como diccionarios"""
        if not self.connection:
            print("Error: No se ha establecido una conexión con la base de datos.")
            return None
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall()
        except psycopg2.DatabaseError as e:
            print(f"Error al obtener los resultados: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None

    def get_books(self):
        try:
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM books;"
                cursor.execute(query)
                books = cursor.fetchall()
            return books
        except Exception as e:
            print(f"Error al obtener los libros: {e}")
            return []

    def get_user_by_credentials(self, username, password):
        """Obtiene un usuario de la base de datos según las credenciales proporcionadas"""
        query = "SELECT * FROM users WHERE username = %s AND password = %s;"
        params = (username, password)
        result = self.fetchall(query, params)
        if result:
            return result[0]  # Retorna el primer resultado como diccionario
        return None  # Si no hay usuario que coincida

    def delete_book(self, book_id):
        try:
            # Verificar que el libro exista
            with self.connection.cursor() as cursor:
                # Verificar si el libro existe antes de intentar eliminarlo
                query_check = "SELECT * FROM books WHERE id_book = %s"
                cursor.execute(query_check, (book_id,))
                book = cursor.fetchone()

                if not book:
                    print(f"El libro con ID {book_id} no existe.")
                    return  # Si no existe, salir de la función

                # Si el libro existe, proceder a eliminarlo
                query_delete = "DELETE FROM books WHERE  id_book = %s"
                cursor.execute(query_delete, (book_id,))
                self.connection.commit()  # Confirmar la transacción
                print(f"Libro con ID {book_id} eliminado correctamente.")
        except Exception as e:
            print(f"Error al eliminar el libro: {e}")