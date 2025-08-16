import csv
import os

class Book:
    def _init_(self, title, author, available=True):
        self.title = title
        self.author = author
        self.available = available

class Library:
    FILE_NAME = "library_books.csv"

    def _init_(self):
        # Create CSV file if it doesn't exist
        if not os.path.exists(self.FILE_NAME):
            with open(self.FILE_NAME, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Title", "Author", "Available"])
            
            # Preload some books
            self.add_book(Book("Python Crash Course", "Eric Matthes"))
            self.add_book(Book("Automate the Boring Stuff", "Al Sweigart"))
            self.add_book(Book("Clean Code", "Robert C. Martin"))
            self.add_book(Book("Learning Python", "Mark Lutz"))
            self.add_book(Book("Data Science from Scratch", "Joel Grus"))

    def add_book(self, book):
        with open(self.FILE_NAME, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([book.title, book.author, "Yes" if book.available else "No"])
        print(f"✅ '{book.title}' by {book.author} added to the library!")

    def view_books(self):
        print("\n📚 Library Books:")
        with open(self.FILE_NAME, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                print(f"{row['Title']} by {row['Author']} - {'Available' if row['Available']=='Yes' else 'Borrowed'}")

    def search_book(self, keyword):
        print("\n🔍 Search Results:")
        found = False
        with open(self.FILE_NAME, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if keyword.lower() in row["Title"].lower() or keyword.lower() in row["Author"].lower():
                    print(f"{row['Title']} by {row['Author']} - {'Available' if row['Available']=='Yes' else 'Borrowed'}")
                    found = True
        if not found:
            print("No matching books found.")

    def borrow_book(self, title):
        books = []
        borrowed = False
        with open(self.FILE_NAME, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Title"].lower() == title.lower() and row["Available"] == "Yes":
                    row["Available"] = "No"
                    borrowed = True
                books.append(row)
        with open(self.FILE_NAME, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Title", "Author", "Available"])
            writer.writeheader()
            writer.writerows(books)
        if borrowed:
            print(f"📖 You borrowed '{title}'")
        else:
            print("❌ Book not available.")

    def return_book(self, title):
        books = []
        returned = False
        with open(self.FILE_NAME, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Title"].lower() == title.lower() and row["Available"] == "No":
                    row["Available"] = "Yes"
                    returned = True
                books.append(row)
        with open(self.FILE_NAME, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Title", "Author", "Available"])
            writer.writeheader()
            writer.writerows(books)
        if returned:
            print(f"✅ You returned '{title}'")
        else:
            print("❌ Book not found or was not borrowed.")

# ------------------- MAIN PROGRAM -------------------
lib = Library()

while True:
    print("\n==== Library Menu ====")
    print("1. Add Book")
    print("2. View All Books")
    print("3. Search Book")
    print("4. Borrow Book")
    print("5. Return Book")
    print("6. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        title = input("Enter book title: ")
        author = input("Enter author name: ")
        lib.add_book(Book(title, author))

    elif choice == "2":
        lib.view_books()

    elif choice == "3":
        keyword = input("Enter title/author keyword: ")
        lib.search_book(keyword)

    elif choice == "4":
        title = input("Enter book title to borrow: ")
        lib.borrow_book(title)

    elif choice == "5":
        title = input("Enter book title to return: ")
        lib.return_book(title)

    elif choice == "6":
        print("Exiting...")
        break
    else:
        print("Invalid choice!")