# Bookshop Management System
````md
# Bookshop Management System

A Python-based Bookshop Management System using MySQL for database management.  
This project helps manage books, purchases, billing, stock updates, and workers in a bookshop.

---

## Features

- Add new books
- View available books
- Update book stock quantity
- Purchase books
- Generate customer bills
- View purchase history
- Add workers
- Remove workers
- View workers details
- MySQL database integration

---

## Technologies Used

- Python
- MySQL
- mysql-connector-python

---

## Database Tables

### Books Table
Stores information about books:
- Book Code
- Title
- Author
- Price
- Quantity

### Purchases Table
Stores customer purchase records:
- Customer Name
- Phone Number
- Book Purchased
- Quantity
- Purchase Date
- Payment Method
- Discount

### Workers Table
Stores worker information:
- Worker Name
- Position
- Salary
- Mobile Number

---

## Installation
````
### 1. Clone the Repository

```bash
git clone https://github.com/jasika03/Bookshop-Management-System.git
````

### 2. Open Project Folder

```bash
cd Bookshop-Management-System
```

### 3. Install MySQL Connector

```bash
pip install mysql-connector-python
```

### 4. Configure MySQL

Update your MySQL password in the Python file:

```python
password="YourPasswordHere"
```

### 5. Run the Project

```bash
python "BookShop Management System.py"
```

---

## Requirements

* Python 3.x
* MySQL Server
* mysql-connector-python library

---

## Project Structure

```text
Bookshop-Management-System/
│
├── BookShop Management System.py
└── README.md
```

---

## Sample Menu

```text
1. Add Book
2. View Books
3. Update Stock
4. Purchase Book
5. Generate Bill
6. View Purchases
7. Add Worker
8. Remove Worker
9. View Workers
0. Exit
```

---

## Author

Jasika
B.Tech CSE Student at Maharishi Markandeshwar University (MMDU)

---

## Future Improvements

* GUI using Tkinter
* Admin Login System
* Search Books Feature
* Sales Reports
* PDF Bill Generation
* Barcode Scanner Integration

---

## License

This project is created for educational purposes.

```
```
