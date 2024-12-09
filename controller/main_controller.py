from model.postgresql_model import PostgreSQLModel
from model.mongo_model import MongoModel

class MainController:
    def __init__(self):
        print("Inicializando sistema de librería desde terminal...")

        # Configuración de PostgreSQL
        self.postgresql_model = PostgreSQLModel(
            host="localhost",
            user="maureentellez",  # Usuario de PostgreSQL
            password="1603",       # Contraseña de PostgreSQL
            database="Libreria"    # Base de datos
        )
        self.postgresql_model.connect()
        self.postgresql_model.test_connection()  # Verifica la conexión

        # Configuración de MongoDB
        self.mongo_model = MongoModel(uri="mongodb+srv://maureenbarra16:PopiMauLuna1677@cluster0.ifap9.mongodb.net/libreria?retryWrites=true&w=majority")
        self.mongo_model.connect()

        # Variable para el usuario autenticado
        self.current_user = None
        self.role = None

    def authenticate_user(self):
        username = input("Ingrese su nombre de usuario: ").strip()
        password = input("Ingrese su contraseña: ").strip()
        if not username or not password:
            print("Error: Usuario y contraseña no pueden estar vacíos.")
            return False

        user_data = self.postgresql_model.get_user_by_credentials(username, password)
        if user_data:
            self.role = user_data['role']
            print(f"¡Bienvenido, {username}!")
            return True
        else:
            print("Usuario o contraseña incorrectos.")
            return False

    def main_menu(self):
        if not self.authenticate_user():
            return

        while True:
            print("\n--- Sistema de Librería ---")
            print("1. Ver libros")
            print("2. Ver libros con reseñas")
            if self.role == "admin":
                print("3. Agregar un libro")
                print("4. Eliminar un libro")
                print("5. Agregar una editorial")
                print("6. Agregar un autor")
            if self.role == "user":
                print("3. Agregar una reseña")
            print("7. Salir")

            choice = input("Elige una opción: ").strip()
            try:
                if choice == "1":
                    self.get_books()
                elif choice == "2":
                    self.display_books_with_reviews()
                elif choice == "3" and self.role == "admin":
                    self.add_new_book()
                elif choice == "3" and self.role == "user":
                    self.add_new_review()
                elif choice == "4" and self.role == "admin":
                    self.delete_book()
                elif choice == "5" and self.role == "admin":
                    self.add_new_editorial()
                elif choice == "6" and self.role == "admin":
                    self.add_new_author()
                elif choice == "7":
                    print("¡Adiós!")
                    break
                else:
                    print("Opción inválida. Intenta de nuevo.")
            except Exception as e:
                print(f"Ha ocurrido un error: {e}")

    def display_books_with_reviews(self):
        books = self.postgresql_model.get_books()
        if not books:
            print("No hay libros registrados.")
            return

        for book in books:
            book_id = book[0]
            title = book[1]
            reviews = self.mongo_model.fetch_reviews(book_id)
            print(f"\nID: {book_id}, Título: {title}")
            if reviews:
                print("Reseñas:")
                for review in reviews:
                    print(f" - {review['review']}")
            else:
                print("No hay reseñas para este libro.")

    def add_new_review(self):
        try:
            book_id = int(input("Ingrese el ID del libro: ").strip())
            review = input("Escriba su reseña: ").strip()

            if not review:
                print("Error: La reseña no puede estar vacía.")
                return

            session = self.mongo_model.start_transaction()
            try:
                self.mongo_model.add_review(book_id, review, session)
                self.mongo_model.commit_transaction(session)
                print("Reseña agregada correctamente.")
            except Exception as e:
                self.mongo_model.abort_transaction(session)
                print(f"Error al agregar la reseña: {e}")

        except ValueError:
            print("Error: El ID del libro debe ser un número.")
        except Exception as e:
            print(f"Error inesperado: {e}")


    def add_new_book(self):
        try:
            id_book = int(input("Ingrese el ID del libro: ").strip())
            title = input("Ingrese el título del libro: ").strip()
            isbn = input("Ingrese el ISBN: ").strip()
            year_of_publication = int(input("Ingrese el año de publicación: ").strip())
            language = input("Ingrese el idioma: ").strip()
            editorial_id = int(input("Ingrese el ID de la editorial: ").strip())
            author_id = int(input("Ingrese el ID del autor: ").strip())

            if not (title and isbn and language):
                print("Error: Todos los campos son obligatorios.")
                return

            self.postgresql_model.begin_transaction()
            self.postgresql_model.add_book(id_book, title, isbn, year_of_publication, language, editorial_id, author_id)
            self.postgresql_model.commit_transaction()
            print(f"Libro '{title}' agregado correctamente.")
        except ValueError:
            print("Error: Asegúrate de ingresar números válidos para los IDs y el año.")
        except Exception as e:
            self.postgresql_model.rollback_transaction()
            print(f"Error al agregar el libro: {e}")


    def delete_book(self):
        try:
            book_id = int(input("Ingrese el ID del libro a eliminar: "))
            self.postgresql_model.begin_transaction()
            self.postgresql_model.delete_book(book_id)
            self.postgresql_model.commit_transaction()
            print(f"Libro con ID {book_id} eliminado correctamente.")
        except ValueError:
            print("Error: El ID del libro debe ser un número.")
        except Exception as e:
            self.postgresql_model.rollback_transaction()
            print(f"Error al eliminar el libro: {e}")

    def get_books(self):
        books = self.postgresql_model.get_books()
        if not books:
            print("No hay libros registrados.")
            return

        for book in books:
            book_id = book[0]
            title = book[1]
            print(f"ID: {book_id}, Título: {title}")

    def add_new_editorial(self):
        id_editorial = int(input("Ingrese el ID de la editorial: "))
        name = input("Ingrese el nombre de la editorial: ")
        country_of_origin = input("Ingrese el país de origen: ")
        year_established = int(input("Ingrese el año de establecimiento: "))

        if name and country_of_origin and year_established:
            try:
                self.postgresql_model.begin_transaction()
                self.postgresql_model.add_editorial(id_editorial, name, country_of_origin, year_established)
                self.postgresql_model.commit_transaction()
                print(f"Editorial '{name}' agregada correctamente.")
            except Exception as e:
                self.postgresql_model.rollback_transaction()
                print(f"Error al agregar la editorial: {e}")
        else:
            print("Error: Todos los campos son necesarios.")

    def add_new_author(self):
        id_author = int(input("Ingrese el ID del autor: "))
        name = input("Ingrese el nombre del autor: ")
        nationality = input("Ingrese la nacionalidad del autor: ")
        year_of_birth = int(input("Ingrese el año de nacimiento: "))
        year_of_death = input("Ingrese el año de fallecimiento (opcional): ")
        year_of_death = int(year_of_death) if year_of_death else None

        if name and nationality and year_of_birth:
            try:
                self.postgresql_model.begin_transaction()
                self.postgresql_model.add_author(id_author, name, nationality, year_of_birth, year_of_death)
                self.postgresql_model.commit_transaction()
                print(f"Autor '{name}' agregado correctamente.")
            except Exception as e:
                self.postgresql_model.rollback_transaction()
                print(f"Error al agregar el autor: {e}")
        else:
            print("Error: Todos los campos son necesarios.")

if __name__ == "__main__":
    controller = MainController()
    controller.main_menu()