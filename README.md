# 📚 Bookstore Management System

A web-based Bookstore Management System developed using Python Flask and MySQL to simplify bookstore operations, including inventory management, customer records, and order processing.

## Features

- **Book Inventory Management** to manage and maintain book records
- **Customer Management** to store and manage customer information
- **Order Processing** to handle customer orders
- **CRUD Operations** to create, read, update, and delete records
- **Database Management** using MySQL for structured data storage
- **SQL Queries** for efficient data retrieval, sales reporting, and inventory analysis
- **Flask Backend** for handling application logic and database operations

## Tech Stack

- **Backend:** Python Flask
- **Database:** MySQL
- **Database Language:** SQL
- **Frontend:** HTML, CSS, JavaScript
- **Tools:** VS Code, MySQL Workbench

## Project Structure

```text
DBMS-project/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── index.html
│   └── ...
│
├── app.py
│
├── ER DIAGRAM
│
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/hankareriya/Bookstore-Management-System.git
```

### 2. Navigate to the Project Directory

```bash
cd Bookstore-Management-System
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install flask mysql-connector-python
```

Install any additional packages required by the application.

### 6. Database Configuration

- Start your MySQL server.
- Create the required database.
- Configure the MySQL connection in the application.
- Create the necessary tables using the database schema.

### 7. Run the Application

```bash
python app.py
```

Open the local URL displayed in the terminal to access the application.

## Database Design

The project uses a relational MySQL database to manage bookstore information.

The Entity Relationship (ER) Diagram illustrates the database structure and relationships between entities.

## Learning Outcomes

- Understanding relational database management systems.
- Implementing CRUD operations using Flask and MySQL.
- Designing normalized database schemas.
- Writing SQL queries for data retrieval and reporting.
- Integrating Python applications with relational databases.

## Author

**Riya Hankare**

GitHub: [hankareriya](https://github.com/hankareriya)
