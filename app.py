from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'yourpassword'
app.config['MYSQL_DB'] = 'store'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

# Book Management
@app.route('/books')
def books():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Book_info")
    books = cur.fetchall()
    cur.close()
    return render_template('books.html', books=books)

@app.route('/add_book', methods=['POST'])
def add_book():
    book_name = request.form['book_name']
    price = request.form['price']
    release_date = request.form['release_date']
    stock = request.form['stock']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Book_info (BookName, Price, ReleaseDate, Stock) VALUES (%s, %s, %s, %s)",
                (book_name, price, release_date, stock))
    mysql.connection.commit()
    flash('Book added successfully!')
    return redirect(url_for('books'))

@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Book_info WHERE BookID = %s", [book_id])
    mysql.connection.commit()
    flash('Book deleted successfully!')
    return redirect(url_for('books'))

# Category Management
@app.route('/categories')
def categories():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Category_info")
    categories = cur.fetchall()
    cur.execute("SELECT BookID, BookName FROM Book_info")
    books = cur.fetchall()
    cur.close()
    return render_template('categories.html', categories=categories, books=books)

@app.route('/add_category', methods=['POST'])
def add_category():
    book_id = request.form['book_id']
    category_name = request.form['category_name']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Category_info (BookID, CategoryName) VALUES (%s, %s)", (book_id, category_name))
    mysql.connection.commit()
    flash('Category added successfully!')
    return redirect(url_for('categories'))

@app.route('/delete_category/<int:category_id>')
def delete_category(category_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Category_info WHERE CategoryID = %s", [category_id])
    mysql.connection.commit()
    flash('Category deleted successfully!')
    return redirect(url_for('categories'))

# Customer Management
@app.route('/customers')
def customers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Customer_info")
    customers = cur.fetchall()
    cur.close()
    return render_template('customers.html', customers=customers)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    name = request.form['customer_name']
    email = request.form['email']
    address = request.form['address']
    phone = request.form['phone']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Customer_info (CustomerName, Email, Address, PhoneNumber) VALUES (%s, %s, %s, %s)",
                (name, email, address, phone))
    mysql.connection.commit()
    flash('Customer added successfully!')
    return redirect(url_for('customers'))

@app.route('/delete_customer/<int:customer_id>')
def delete_customer(customer_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Customer_info WHERE CustomerID = %s", [customer_id])
    mysql.connection.commit()
    flash('Customer deleted successfully!')
    return redirect(url_for('customers'))

# Order Management
@app.route('/orders')
def orders():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Order_info")
    orders = cur.fetchall()
    cur.execute("SELECT CustomerID, CustomerName FROM Customer_info")
    customers = cur.fetchall()
    cur.execute("SELECT BookID, BookName FROM Book_info")
    books = cur.fetchall()
    cur.close()
    return render_template('orders.html', orders=orders, customers=customers, books=books)

@app.route('/add_order', methods=['POST'])
def add_order():
    customer_id = request.form['customer_id']
    book_id = request.form['book_id']
    order_date = request.form['order_date']
    
    # Fetch the price of the selected book from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT Price FROM Book_info WHERE BookID = %s", [book_id])
    book_price = cur.fetchone()[0]  # Assuming the price is in the first column
    cur.close()
    
    # Set the total amount as the book price
    total_amount = book_price
    
    # Insert the order into the database
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Order_info (CustomerID, BookID, OrderDate, TotalAmount) VALUES (%s, %s, %s, %s)",
                (customer_id, book_id, order_date, total_amount))
    mysql.connection.commit()
    flash('Order added successfully!')
    return redirect(url_for('orders'))

@app.route('/delete_order/<int:order_id>')
def delete_order(order_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Order_info WHERE OrderID = %s", [order_id])
    mysql.connection.commit()
    flash('Order deleted successfully!')
    return redirect(url_for('orders'))



# Route for displaying reviews and the review form
@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        # Getting data from the form
        customer_id = request.form['customer_id']
        book_id = request.form['book_id']
        rating = request.form['rating']
        comments = request.form['comments']
        review_date = request.form['review_date']

        # Inserting the review into the database
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO Review_info (CustomerID, BookID, ReviewDate, Rating, Comments) 
            VALUES (%s, %s, %s, %s, %s)
        """, (customer_id, book_id, review_date, rating, comments))
        mysql.connection.commit()
        flash('Review added successfully!')
        return redirect(url_for('reviews'))

    # Fetching all customers and books for the form
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Customer_info")
    customers = cur.fetchall()
    
    cur.execute("SELECT * FROM Book_info")
    books = cur.fetchall()
    
    # Fetching all reviews and joining with customer and book details
    cur.execute("""
        SELECT r.CustomerID, r.BookID, r.ReviewDate, r.Rating, r.Comments, 
               c.CustomerName, b.BookName 
        FROM Review_info r
        JOIN Customer_info c ON r.CustomerID = c.CustomerID
        JOIN Book_info b ON r.BookID = b.BookID
    """)
    reviews = cur.fetchall()

    # Modify reviews to include customer_name and book_name for template use
    reviews_data = []
    for review in reviews:
        reviews_data.append({
            'customer_name': review[5],
            'book_name': review[6],
            'rating': review[3],
            'comments': review[4],
            'review_date': review[2]
        })

    return render_template('reviews.html', customers=customers, books=books, reviews=reviews_data)


@app.route('/shipping', methods=['GET', 'POST'])
def shipping():
    if request.method == 'POST':
        # Getting data from the form
        order_id = request.form['order_id']
        shipping_date = request.form['shipping_date']
        delivery_date = request.form['delivery_date']
        shipping_address = request.form['shipping_address']
        shipping_id = request.form['shipping_id']

        # Inserting shipping details into the database
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO Shipping_info (ShippingID, OrderID, ShippingDate, DeliveryDate, ShippingAddress) 
            VALUES (%s, %s, %s, %s, %s)
        """, (shipping_id, order_id, shipping_date, delivery_date, shipping_address))
        mysql.connection.commit()
        flash('Shipping details added successfully!')
        return redirect(url_for('shipping'))

    # Fetching orders and shipping details
    cur = mysql.connection.cursor()
    
    # Fetch orders to populate the dropdown
    cur.execute("SELECT OrderID, OrderDate FROM Order_info")
    orders = cur.fetchall()

    # Fetch shipping details
    cur.execute("""
        SELECT s.ShippingID, s.OrderID, s.ShippingDate, s.DeliveryDate, s.ShippingAddress, o.OrderDate 
        FROM Shipping_info s
        JOIN Order_info o ON s.OrderID = o.OrderID
    """)
    shippings = cur.fetchall()

    return render_template('shipping.html', shippings=shippings, orders=orders)



if __name__ == "__main__":
    app.run(debug=True)
