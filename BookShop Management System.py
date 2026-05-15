import mysql.connector
from datetime import datetime

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YourPasswordHere"
)

cursor = db_connection.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS bookshop_db")
print("Database created successfully")

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YourPasswordHere",
    database="bookshop_db"
)
cursor = db_connection.cursor()

print("Connected to bookshop_db successfully")

def create_tables():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_code VARCHAR(50) PRIMARY KEY,
            title VARCHAR(255),
            author VARCHAR(255),
            price FLOAT,
            quantity INT
        )
    """)
 
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS purchases (
           id INT AUTO_INCREMENT PRIMARY KEY,
           customer_name VARCHAR(255),
           phone_number VARCHAR(20),
           book_code VARCHAR(50),
           quantity INT,
           purchase_date DATETIME,
           payment_method VARCHAR(255),
           discount FLOAT,
           FOREIGN KEY (book_code) REFERENCES books(book_code)
         )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            position VARCHAR(255),
            salary DECIMAL(10,2),
            mobile_number VARCHAR(15) UNIQUE
        )
    """)

def add_book(book_code, title, author, price, quantity):
    query = "INSERT INTO books (book_code, title, author, price, quantity) VALUES (%s, %s, %s, %s, %s)"
    values = (book_code, title, author, price, quantity)
    cursor.execute(query, values)
    db_connection.commit()
    print("New book added successfully!")

def view_books():
    query = "SELECT * FROM books"
    cursor.execute(query)
    books = cursor.fetchall()

    if not books:
        print("No books available.")
    else:
        for book in books:
            print(f"Book Code: {book[0]}, Title: {book[1]}, Author: {book[2]}, Price: {book[3]}, Quantity: {book[4]}")
            
def update_book_quantity(book_code, quantity_to_add):
    # Check if the book exists
    query_select_book = "SELECT * FROM books WHERE book_code=%s"
    value_select_book = (book_code,)
    cursor.execute(query_select_book, value_select_book)
    book = cursor.fetchone()

    if not book:
        print("Book not found.")
        return

    # Update the book quantity
    new_quantity = book[4] + quantity_to_add
    query_update_book = "UPDATE books SET quantity=%s WHERE book_code=%s"
    values_update_book = (new_quantity, book_code)
    cursor.execute(query_update_book, values_update_book)
    db_connection.commit()

    print(f"Quantity updated successfully. New quantity for book {book_code}: {new_quantity}")

def purchase_book(customer_name, phone_number, book_code, payment_method, quantity=1, discount=0):
    # Check if the book with the specified CODE exists
    cursor.execute("SELECT quantity, price FROM books WHERE book_code = %s", (book_code,))
    book_info = cursor.fetchone()

    if not book_info:
        print(f"No book available with CODE {book_code}. Purchase will not be recorded.")
        return None

    existing_quantity, book_price = book_info

    try:
        quantity = int(quantity)
        discount = float(discount)
    except ValueError:
        print("Invalid input. Please enter valid values.")
        return None

    if quantity > existing_quantity:
        print(f"Error: Not enough stock available for the selected book. Available Quantity: {existing_quantity}")
        return None

    total_amount = (float(book_price) - (float(book_price) * discount)) * quantity

    cursor.execute("""
    INSERT INTO purchases (customer_name, book_code, payment_method, quantity, purchase_date, discount)
    VALUES (%s, %s, %s, %s, NOW(), %s)
    """, (customer_name, book_code, payment_method, quantity, discount))

    purchase_id = cursor.lastrowid

    db_connection.commit()
    print(f"Purchase recorded successfully! Total Amount: ₹{total_amount:.2f}")

    # Update the book's quantity in the books table
    updated_quantity = existing_quantity - quantity
    cursor.execute("UPDATE books SET quantity = %s WHERE book_code = %s", (updated_quantity, book_code))

    db_connection.commit()
    print("Book quantity updated successfully!")

    return purchase_id


def generate_bill(purchase_id):
    cursor.execute("""
    SELECT p.id, p.customer_name, p.phone_number, b.title, b.price, p.quantity, p.discount, p.purchase_date, p.payment_method
    FROM purchases p
    JOIN books b ON p.book_code = b.book_code
    WHERE p.id = %s
    """, (purchase_id,))
    purchase_info = cursor.fetchone()

    if purchase_info:
        purchase_id, customer_name, phone_number, book_title, book_price, quantity, discount, purchase_date, payment_method = purchase_info
        actual_price = book_price * quantity
        discounted_amount = actual_price * discount
        total_amount = actual_price - discounted_amount

        print(f"\n--- Bill for Purchase ID {purchase_id} ---")
        print(f"Customer: {customer_name}")
        print(f"Phone Number: {phone_number}")
        print(f"Book Title: {book_title}")
        print(f"Quantity: {quantity}")
        print(f"Price per unit: ₹{book_price:.2f}")
        print(f"Actual Price (for {quantity} units): ₹{actual_price:.2f}")
        print(f"Discount ({discount * 100}%): -₹{discounted_amount:.2f}")
        print(f"Total Price: ₹{total_amount:.2f}")
        print(f"Purchase Date: {purchase_date}")
        print(f"Payment Method: {payment_method}")
        print("--- Thank you for your purchase! ---")
    else:
        print("Purchase not found.")

def view_purchases():
    cursor.execute("""
    SELECT p.id, p.customer_name, p.phone_number, b.title, b.author, b.price, p.quantity, p.discount, p.purchase_date, p.payment_method
    FROM purchases p
    JOIN books b ON p.book_code = b.book_code
    """)
    purchases = cursor.fetchall()
    for purchase in purchases:
        purchase_id, customer_name, phone_number, book_title, book_author, book_price, purchase_quantity, discount, purchase_date, payment_method = purchase
        print(f"ID: {purchase_id}, Customer: {customer_name}, Phone Number: {phone_number}, Book: {book_title} by {book_author}, "
              f"Price: ${book_price:.2f}, Quantity: {purchase_quantity}, Discount: {discount * 100}%, Purchase Date: {purchase_date}, Payment Method: {payment_method}")
        print()
def add_worker(name, position, salary, mobile_number):
    query = "INSERT INTO workers (name, position, salary, mobile_number) VALUES (%s, %s, %s, %s)"
    values = (name, position, salary, mobile_number)
    cursor.execute(query, values)
    db_connection.commit()
    print("Worker added successfully!")
    
def remove_worker(worker_id):
    # Check if the worker with the specified ID exists
    cursor.execute("SELECT id FROM workers WHERE id = %s", (worker_id,))
    existing_worker = cursor.fetchone()

    if existing_worker:
        cursor.execute("DELETE FROM workers WHERE id = %s", (worker_id,))
        db_connection.commit()
        print(f"Worker with ID {worker_id} has been removed.")
    else:
        print(f"No worker found with ID {worker_id}. No changes made.")

def view_workers():
    query = "SELECT * FROM workers"
    cursor.execute(query)
    workers = cursor.fetchall()

    if not workers:
        print("No workers found.")
    else:
        for worker in workers:
            print(f"ID: {worker[0]}, Name: {worker[1]}, Position: {worker[2]}, salary:₹{worker[3]:.2f}Mobile Number: {worker[4]}")

def main():
    create_tables()

    while True:
        print("\nBookshop Management System")
        print("1. Add Book")
        print("2. View Books")
        print("3. Update Stock:")
        print("4. Purchase Book")
        print("5. Generate Bill")
        print("6. View Purchases")
        print("7. Add Worker")
        print("8. Remove Worker")
        print("9. View Workers")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # Add Book
            book_code = input("Enter book code: ")
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            price = float(input("Enter book price: "))
            quantity = int(input("Enter book quantity: "))
            add_book(book_code, title, author, price, quantity)

        elif choice == "2":
            # View Books
            view_books()
            
        elif choice == "3":
            # Update Book Quantity
            view_books()
            book_code = input("Enter book code to update quantity: ")
            new_quantity = int(input("Enter new quantity: "))
            update_book_quantity(book_code, new_quantity)
            
        elif choice == "4":
            # Purchase Book
            purchase_books()
            
        elif choice == "5":
            #Generate Bill
            purchase_id = int(input("Enter the ID of the purchase for which you want to generate a bill: "))
            generate_bill(purchase_id)

        elif choice == "6":
            # View Purchases
            view_purchases()

        elif choice == "7":
            # Add Worker
            name = input("Enter worker name: ")
            position = input("Enter worker position: ")
            salary = float(input("Enter the worker's salary: "))
            mobile_number = input("Enter worker mobile number: ")
            add_worker(name, position, salary, mobile_number)

        elif choice == "8":
            # Remove Worker
            view_workers()
            worker_id = int(input("Enter worker ID to remove: "))
            remove_worker(worker_id)
          
        elif choice == "9":
            # View Workers
            view_workers()
            
        elif choice == "0":
            # Exit the program
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")

    cursor.close()
    db_connection.close()

def purchase_books():
    view_books()
    book_code = input("Enter the CODE of the book you want to purchase: ")

    # Check if the book with the specified CODE exists
    cursor.execute("SELECT book_code, quantity, price FROM books WHERE book_code = %s", (book_code,))
    book_info = cursor.fetchone()

    if not book_info:
        print(f"No book available with CODE {book_code}. Purchase will not be recorded.")
        return None

    _, existing_quantity, book_price = book_info

    if existing_quantity == 0:
        print(f"Error: The selected book is out of stock. Purchase will not be recorded.")
        return None

    quantity_to_purchase = int(input("Enter the quantity of books you want to purchase: "))
    if quantity_to_purchase > existing_quantity:
        print(f"Error: Not enough stock available for the selected book. Available Quantity: {existing_quantity}")
        return None

    customer_name = input("Enter your name: ")
    phone_number = input("Enter your phone number: ")
    
    discount = float(input("Enter the discount percentage (0 for no discount): ")) / 100.0

    print("Select Payment Method:")
    print("1. Cash")
    print("2. Credit Card")
    print("3. Online Payment")
    payment_choice = input("Enter your choice (1/2/3): ")

    if payment_choice == "1":
        payment_method = "Cash"
    elif payment_choice == "2":
        payment_method = "Credit Card"
    elif payment_choice == "3":
        payment_method = "Online Payment"
    else:
        print("Invalid payment method.")

    try:
        purchase_id = purchase_book(customer_name, phone_number, book_code, payment_method, quantity_to_purchase, discount)
        print(f"Purchase ID: {purchase_id}")
    except ValueError:
        print("Invalid input. Please enter valid values.")

if __name__ == "__main__":
    main()
