import json
import os

# Определяем файл для хранения данных библиотеки / Define the file to store library data
DATA_FILE = "library.json"

# Класс для книги / Book class
class Book:
    def __init__(self, id: int, title: str, author: str, year: int, status: str = "in stock"):
        self.id = id  # Уникальный идентификатор книги / Unique identifier for the book
        self.title = title  # Название книги / Book title
        self.author = author  # Автор книги / Book author
        self.year = year  # Год издания / Publication year
        self.status = status  # Статус книги ("в наличии", "выдана") / Book status ("in stock", "issued")

    def to_dict(self):
        # Возвращает словарь с данными книги / Returns a dictionary representation of the book
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

# Класс системы управления библиотекой / Library Management System class
class LibraryManagementSystem:
    def __init__(self):
        # Загружаем книги из файла / Load books from the data file
        self.books = self.load_books()

    def load_books(self):
        # Загрузка данных книг из JSON-файла / Load book data from the JSON file
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                return [Book(**book) for book in json.load(file)]
        return []

    def save_books(self):
        # Сохраняем данные книг в JSON-файл / Save book data to the JSON file
        with open(DATA_FILE, "w") as file:
            json.dump([book.to_dict() for book in self.books], file, indent=4)

    def add_book(self, title: str, author: str, year: int):
        # Добавление новой книги в библиотеку / Add a new book to the library
        book_id = len(self.books) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_books()
        print(f"Книга успешно добавлена с ID: {book_id}")  # Book added successfully with ID

    def delete_book(self, book_id: int):
        # Удаление книги по ID / Delete a book by ID
        book = next((book for book in self.books if book.id == book_id), None)
        if book:
            self.books.remove(book)
            self.save_books()
            print(f"Книга с ID {book_id} успешно удалена.")  # Book deleted successfully
        else:
            print("Книга не найдена!")  # Book not found

    def search_books(self, keyword: str):
        # Поиск книг по ключевому слову / Search books by a keyword
        results = [book for book in self.books if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower()]
        if results:
            print("Результаты поиска:")  # Search results
            self.display_books(results)
        else:
            print("Книги, соответствующие ключевому слову, не найдены.")  # No books found

    def display_books(self, books=None):
        # Отображение списка книг / Display a list of books
        books = books if books else self.books
        if books:
            print("Список книг:")  # List of books
            for book in books:
                print(f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}")
        else:
            print("Библиотека пуста.")  # Library is empty

    def change_status(self, book_id: int, new_status: str):
        # Изменение статуса книги / Change the status of a book
        if new_status not in ["in stock", "issued"]:
            print("Недопустимый статус!")  # Invalid status
            return
        book = next((book for book in self.books if book.id == book_id), None)
        if book:
            book.status = new_status
            self.save_books()
            print(f"Статус книги с ID {book_id} успешно обновлен на '{new_status}'.")  # Book status updated successfully
        else:
            print("Книга не найдена!")  # Book not found

# Интерфейс командной строки / Command Line Interface
def main():
    system = LibraryManagementSystem()
    print("Система управления библиотекой")  # Library Management System
    print("Команды: add, delete, search, display, change, exit")  # Commands

    while True:
        command = input("Введите команду: ").strip().lower()  # Enter command

        if command == "add":
            title = input("Введите название: ")  # Enter title
            author = input("Введите автора: ")  # Enter author
            year = int(input("Введите год: "))  # Enter year
            system.add_book(title, author, year)

        elif command == "delete":
            book_id = int(input("Введите ID книги: "))  # Enter book ID
            system.delete_book(book_id)

        elif command == "search":
            keyword = input("Введите ключевое слово для поиска: ")  # Enter search keyword
            system.search_books(keyword)

        elif command == "display":
            system.display_books()

        elif command == "change":
            book_id = int(input("Введите ID книги: "))  # Enter book ID
            new_status = input("Введите новый статус (in stock/issued): ").strip()  # Enter new status
            system.change_status(book_id, new_status)

        elif command == "exit":
            print("Выход из системы управления библиотекой. До свидания!")  # Exiting Library Management System
            break

        else:
            print("Недопустимая команда! Попробуйте снова.")  # Invalid command

# Создаем JSON-файл, если его нет / Create JSON file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

main()
