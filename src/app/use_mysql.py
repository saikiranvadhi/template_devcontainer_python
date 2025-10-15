"""
MySQL Usage Examples with Python

This script demonstrates common MySQL database operations using mysql-connector-python.
It covers schema management, table operations, data manipulation, and various query patterns.

Requirements:
    pip install mysql-connector-python

Usage:
    python src/app/use_mysql.py
"""

import mysql.connector
from mysql.connector import Error
from typing import Optional, List, Tuple, Dict, Any
from contextlib import contextmanager


# Connection configuration
DB_CONFIG = {
    'host': 'mysql',  # Use 'mysql_server' after docker-compose restart
    'port': 3306,
    'user': 'dev_user',
    'password': 'dev_password',
}


@contextmanager
def get_connection(database: Optional[str] = None):
    """
    Context manager for database connections.
    Automatically handles connection cleanup.
    
    Args:
        database: Optional database name to connect to
    """
    config = DB_CONFIG.copy()
    if database:
        config['database'] = database
    
    connection = None
    try:
        connection = mysql.connector.connect(**config)
        yield connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise
    finally:
        if connection and connection.is_connected():
            connection.close()


def execute_query(connection, query: str, params: Optional[Tuple] = None) -> None:
    """
    Execute a query that doesn't return results (INSERT, UPDATE, DELETE, CREATE, etc.)
    
    Args:
        connection: MySQL connection object
        query: SQL query to execute
        params: Optional parameters for parameterized queries
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query, params or ())
        connection.commit()
        print(f"✓ Query executed successfully. Rows affected: {cursor.rowcount}")
    except Error as e:
        print(f"✗ Error executing query: {e}")
        connection.rollback()
        raise
    finally:
        cursor.close()


def fetch_query(connection, query: str, params: Optional[Tuple] = None) -> List[Tuple]:
    """
    Execute a query and return results (SELECT queries)
    
    Args:
        connection: MySQL connection object
        query: SQL query to execute
        params: Optional parameters for parameterized queries
        
    Returns:
        List of tuples containing query results
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"✗ Error fetching query: {e}")
        raise
    finally:
        cursor.close()


def fetch_query_as_dict(connection, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
    """
    Execute a query and return results as list of dictionaries
    
    Args:
        connection: MySQL connection object
        query: SQL query to execute
        params: Optional parameters for parameterized queries
        
    Returns:
        List of dictionaries containing query results
    """
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"✗ Error fetching query: {e}")
        raise
    finally:
        cursor.close()


# ============================================
# 1. SCHEMA/DATABASE MANAGEMENT
# ============================================

def create_schema_if_not_exists(schema_name: str) -> None:
    """Create a new schema (database) if it doesn't exist"""
    print(f"\n{'='*60}")
    print(f"1. Creating schema '{schema_name}' if it doesn't exist")
    print('='*60)
    
    with get_connection() as conn:
        query = f"CREATE DATABASE IF NOT EXISTS {schema_name}"
        execute_query(conn, query)
        print(f"✓ Schema '{schema_name}' is ready")


def show_schemas() -> None:
    """Show all existing schemas (databases)"""
    print(f"\n{'='*60}")
    print("2. Showing all existing schemas")
    print('='*60)
    
    with get_connection() as conn:
        query = "SHOW DATABASES"
        results = fetch_query(conn, query)
        
        print("\nAvailable Databases:")
        for (db_name,) in results:
            print(f"  • {db_name}")


def get_current_schema(connection) -> str:
    """Get the currently selected schema"""
    query = "SELECT DATABASE()"
    result = fetch_query(connection, query)
    return result[0][0] if result and result[0][0] else "None"


def change_schema(schema_name: str) -> None:
    """Change the default schema (USE statement)"""
    print(f"\n{'='*60}")
    print(f"3. Changing to schema '{schema_name}'")
    print('='*60)
    
    with get_connection() as conn:
        current = get_current_schema(conn)
        print(f"Current schema: {current}")
        
        query = f"USE {schema_name}"
        execute_query(conn, query)
        
        new_current = get_current_schema(conn)
        print(f"New schema: {new_current}")


# ============================================
# 2. TABLE MANAGEMENT
# ============================================

def show_tables(database: str) -> None:
    """Show all tables in the specified database"""
    print(f"\n{'='*60}")
    print(f"4. Showing all tables in '{database}' database")
    print('='*60)
    
    with get_connection(database=database) as conn:
        query = "SHOW TABLES"
        results = fetch_query(conn, query)
        
        if results:
            print(f"\nTables in '{database}':")
            for (table_name,) in results:
                print(f"  • {table_name}")
        else:
            print(f"\nNo tables found in '{database}'")


def create_example_tables(database: str) -> None:
    """Create example tables for demonstration"""
    print(f"\n{'='*60}")
    print(f"5. Creating example tables in '{database}'")
    print('='*60)
    
    with get_connection(database=database) as conn:
        # Create products table
        products_table = """
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            category VARCHAR(50),
            price DECIMAL(10, 2) NOT NULL,
            stock INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_category (category),
            INDEX idx_price (price)
        )
        """
        execute_query(conn, products_table)
        print("✓ Created 'products' table")
        
        # Create customers table
        customers_table = """
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(20),
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_email (email)
        )
        """
        execute_query(conn, customers_table)
        print("✓ Created 'customers' table")
        
        # Create orders table
        orders_table = """
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL,
            total_amount DECIMAL(10, 2) NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
            FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            INDEX idx_customer (customer_id),
            INDEX idx_status (status),
            INDEX idx_order_date (order_date)
        )
        """
        execute_query(conn, orders_table)
        print("✓ Created 'orders' table")


def describe_table(database: str, table_name: str) -> None:
    """Show the structure of a table"""
    print(f"\n{'='*60}")
    print(f"6. Describing table '{table_name}'")
    print('='*60)
    
    with get_connection(database=database) as conn:
        query = f"DESCRIBE {table_name}"
        results = fetch_query(conn, query)
        
        print(f"\nStructure of '{table_name}':")
        print(f"{'Field':<20} {'Type':<20} {'Null':<8} {'Key':<8} {'Default':<15} {'Extra':<20}")
        print("-" * 100)
        for row in results:
            field, type_, null, key, default, extra = row
            default = str(default) if default is not None else 'NULL'
            print(f"{field:<20} {type_:<20} {null:<8} {key:<8} {default:<15} {extra:<20}")


# ============================================
# 3. DATA INSERTION
# ============================================

def insert_sample_data(database: str) -> None:
    """Insert sample data into tables"""
    print(f"\n{'='*60}")
    print(f"7. Inserting sample data into tables")
    print('='*60)
    
    with get_connection(database=database) as conn:
        # Insert products
        products_query = """
        INSERT INTO products (name, category, price, stock) VALUES
        (%s, %s, %s, %s)
        """
        products_data = [
            ("Laptop", "Electronics", 999.99, 50),
            ("Mouse", "Electronics", 29.99, 200),
            ("Keyboard", "Electronics", 79.99, 150),
            ("Desk Chair", "Furniture", 249.99, 30),
            ("Standing Desk", "Furniture", 599.99, 20),
            ("Monitor", "Electronics", 299.99, 75),
            ("Webcam", "Electronics", 89.99, 100),
            ("Notebook", "Stationery", 5.99, 500),
            ("Pen Set", "Stationery", 12.99, 300),
            ("Bookshelf", "Furniture", 149.99, 25),
        ]
        
        cursor = conn.cursor()
        try:
            cursor.executemany(products_query, products_data)
            conn.commit()
            print(f"✓ Inserted {cursor.rowcount} products")
        except Error as e:
            print(f"Note: Some products may already exist: {e}")
            conn.rollback()
        finally:
            cursor.close()
        
        # Insert customers
        customers_query = """
        INSERT INTO customers (name, email, phone, address) VALUES
        (%s, %s, %s, %s)
        """
        customers_data = [
            ("Alice Johnson", "alice@example.com", "555-0101", "123 Main St, City A"),
            ("Bob Smith", "bob@example.com", "555-0102", "456 Oak Ave, City B"),
            ("Carol White", "carol@example.com", "555-0103", "789 Pine Rd, City C"),
            ("David Brown", "david@example.com", "555-0104", "321 Elm St, City D"),
            ("Eve Davis", "eve@example.com", "555-0105", "654 Maple Dr, City E"),
        ]
        
        cursor = conn.cursor()
        try:
            cursor.executemany(customers_query, customers_data)
            conn.commit()
            print(f"✓ Inserted {cursor.rowcount} customers")
        except Error as e:
            print(f"Note: Some customers may already exist: {e}")
            conn.rollback()
        finally:
            cursor.close()
        
        # Insert orders
        orders_query = """
        INSERT INTO orders (customer_id, product_id, quantity, total_amount, status) VALUES
        (%s, %s, %s, %s, %s)
        """
        orders_data = [
            (1, 1, 1, 999.99, "delivered"),
            (1, 2, 2, 59.98, "delivered"),
            (2, 4, 1, 249.99, "shipped"),
            (3, 5, 1, 599.99, "processing"),
            (4, 6, 2, 599.98, "delivered"),
            (5, 8, 10, 59.90, "pending"),
            (2, 3, 1, 79.99, "delivered"),
            (1, 7, 1, 89.99, "cancelled"),
        ]
        
        cursor = conn.cursor()
        try:
            cursor.executemany(orders_query, orders_data)
            conn.commit()
            print(f"✓ Inserted {cursor.rowcount} orders")
        except Error as e:
            print(f"Note: Some orders may already exist: {e}")
            conn.rollback()
        finally:
            cursor.close()


# ============================================
# 4. QUERYING DATA
# ============================================

def simple_select_query(database: str) -> None:
    """Simple SELECT query - fetch all records"""
    print(f"\n{'='*60}")
    print("8. Simple SELECT query - All products")
    print('='*60)
    
    with get_connection(database=database) as conn:
        query = "SELECT * FROM products LIMIT 5"
        results = fetch_query_as_dict(conn, query)
        
        print(f"\nFirst 5 products:")
        for product in results:
            print(f"  • {product['name']} - ${product['price']} (Stock: {product['stock']})")


def select_with_where_clause(database: str) -> None:
    """SELECT with WHERE clause - filtering"""
    print(f"\n{'='*60}")
    print("9. SELECT with WHERE clause - Electronics products")
    print('='*60)
    
    with get_connection(database=database) as conn:
        query = "SELECT name, price, stock FROM products WHERE category = %s"
        results = fetch_query(conn, query, ("Electronics",))
        
        print(f"\nElectronics products:")
        for name, price, stock in results:
            print(f"  • {name}: ${price} (Stock: {stock})")


def select_with_aggregation(database: str) -> None:
    """SELECT with aggregation functions"""
    print(f"\n{'='*60}")
    print("10. Aggregation queries - Statistics")
    print('='*60)
    
    with get_connection(database=database) as conn:
        # Count products by category
        query = """
        SELECT category, COUNT(*) as count, AVG(price) as avg_price, SUM(stock) as total_stock
        FROM products
        GROUP BY category
        ORDER BY count DESC
        """
        results = fetch_query(conn, query)
        
        print("\nProducts by category:")
        print(f"{'Category':<20} {'Count':<10} {'Avg Price':<15} {'Total Stock':<15}")
        print("-" * 60)
        for category, count, avg_price, total_stock in results:
            print(f"{category:<20} {count:<10} ${avg_price:<14.2f} {total_stock:<15}")


def select_with_join(database: str) -> None:
    """SELECT with JOIN - combining tables"""
    print(f"\n{'='*60}")
    print("11. JOIN query - Orders with customer and product details")
    print('='*60)
    
    with get_connection(database=database) as conn:
        query = """
        SELECT 
            o.id as order_id,
            c.name as customer_name,
            p.name as product_name,
            o.quantity,
            o.total_amount,
            o.status,
            o.order_date
        FROM orders o
        INNER JOIN customers c ON o.customer_id = c.id
        INNER JOIN products p ON o.product_id = p.id
        ORDER BY o.order_date DESC
        LIMIT 5
        """
        results = fetch_query_as_dict(conn, query)
        
        print("\nRecent orders:")
        for order in results:
            print(f"  Order #{order['order_id']}: {order['customer_name']} ordered {order['quantity']}x "
                  f"{order['product_name']} - ${order['total_amount']} [{order['status']}]")


def select_with_subquery(database: str) -> None:
    """SELECT with subquery"""
    print(f"\n{'='*60}")
    print("12. Subquery - Customers with orders")
    print('='*60)
    
    with get_connection(database=database) as conn:
        query = """
        SELECT name, email,
               (SELECT COUNT(*) FROM orders WHERE customer_id = customers.id) as order_count,
               (SELECT SUM(total_amount) FROM orders WHERE customer_id = customers.id) as total_spent
        FROM customers
        WHERE id IN (SELECT DISTINCT customer_id FROM orders)
        ORDER BY total_spent DESC
        """
        results = fetch_query(conn, query)
        
        print("\nCustomer order statistics:")
        print(f"{'Name':<20} {'Email':<25} {'Orders':<10} {'Total Spent':<15}")
        print("-" * 70)
        for name, email, order_count, total_spent in results:
            spent = f"${total_spent:.2f}" if total_spent else "$0.00"
            print(f"{name:<20} {email:<25} {order_count:<10} {spent:<15}")


def parameterized_query(database: str) -> None:
    """Parameterized queries for security (SQL injection prevention)"""
    print(f"\n{'='*60}")
    print("13. Parameterized query - Safe searching")
    print('='*60)
    
    with get_connection(database=database) as conn:
        # Search for products within a price range
        min_price = 50.00
        max_price = 300.00
        
        query = """
        SELECT name, category, price, stock
        FROM products
        WHERE price BETWEEN %s AND %s
        ORDER BY price ASC
        """
        results = fetch_query(conn, query, (min_price, max_price))
        
        print(f"\nProducts between ${min_price} and ${max_price}:")
        for name, category, price, stock in results:
            print(f"  • {name} ({category}): ${price}")


# ============================================
# 5. DATA UPDATES AND DELETIONS
# ============================================

def update_data(database: str) -> None:
    """UPDATE data in tables"""
    print(f"\n{'='*60}")
    print("14. UPDATE data - Increase product prices")
    print('='*60)
    
    with get_connection(database=database) as conn:
        # Update prices for a specific category
        query = """
        UPDATE products
        SET price = price * 1.10
        WHERE category = %s
        """
        execute_query(conn, query, ("Electronics",))
        print("✓ Increased Electronics prices by 10%")


def delete_data(database: str) -> None:
    """DELETE data from tables"""
    print(f"\n{'='*60}")
    print("15. DELETE data - Remove cancelled orders")
    print('='*60)
    
    with get_connection(database=database) as conn:
        query = "DELETE FROM orders WHERE status = %s"
        execute_query(conn, query, ("cancelled",))
        print("✓ Removed cancelled orders")


# ============================================
# 6. TRANSACTIONS
# ============================================

def transaction_example(database: str) -> None:
    """Demonstrate transaction handling"""
    print(f"\n{'='*60}")
    print("16. Transaction example - Create order with stock update")
    print('='*60)
    
    with get_connection(database=database) as conn:
        cursor = conn.cursor()
        try:
            # Start transaction (auto-commit is disabled)
            conn.start_transaction()
            
            # Check product stock
            cursor.execute("SELECT stock FROM products WHERE id = %s", (1,))
            stock = cursor.fetchone()[0]
            
            if stock >= 1:
                # Decrease stock
                cursor.execute("UPDATE products SET stock = stock - 1 WHERE id = %s", (1,))
                
                # Create order
                cursor.execute(
                    "INSERT INTO orders (customer_id, product_id, quantity, total_amount, status) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (1, 1, 1, 999.99, "pending")
                )
                
                # Commit transaction
                conn.commit()
                print("✓ Transaction completed: Order created and stock updated")
            else:
                conn.rollback()
                print("✗ Transaction rolled back: Insufficient stock")
                
        except Error as e:
            conn.rollback()
            print(f"✗ Transaction rolled back due to error: {e}")
        finally:
            cursor.close()


# ============================================
# 7. ADVANCED QUERIES
# ============================================

def window_function_example(database: str) -> None:
    """Example using window functions (MySQL 8.0+)"""
    print(f"\n{'='*60}")
    print("17. Window function - Rank products by price within category")
    print('='*60)
    
    with get_connection(database=database) as conn:
        query = """
        SELECT 
            name,
            category,
            price,
            RANK() OVER (PARTITION BY category ORDER BY price DESC) as price_rank
        FROM products
        ORDER BY category, price_rank
        """
        results = fetch_query(conn, query)
        
        print("\nProduct ranking by price within category:")
        current_category = None
        for name, category, price, rank in results:
            if category != current_category:
                print(f"\n{category}:")
                current_category = category
            print(f"  {rank}. {name} - ${price}")


def common_table_expression(database: str) -> None:
    """Example using Common Table Expressions (CTE)"""
    print(f"\n{'='*60}")
    print("18. CTE - High-value customers")
    print('='*60)
    
    with get_connection(database=database) as conn:
        query = """
        WITH customer_stats AS (
            SELECT 
                c.id,
                c.name,
                c.email,
                COUNT(o.id) as order_count,
                SUM(o.total_amount) as total_spent
            FROM customers c
            LEFT JOIN orders o ON c.id = o.customer_id
            GROUP BY c.id, c.name, c.email
        )
        SELECT name, email, order_count, total_spent
        FROM customer_stats
        WHERE total_spent > 100
        ORDER BY total_spent DESC
        """
        results = fetch_query(conn, query)
        
        print("\nHigh-value customers (>$100 spent):")
        for name, email, order_count, total_spent in results:
            print(f"  • {name}: {order_count} orders, ${total_spent:.2f} total")


# ============================================
# 8. UTILITY FUNCTIONS
# ============================================

def get_table_row_count(database: str, table_name: str) -> int:
    """Get the number of rows in a table"""
    with get_connection(database=database) as conn:
        query = f"SELECT COUNT(*) FROM {table_name}"
        result = fetch_query(conn, query)
        return result[0][0]


def show_table_statistics(database: str) -> None:
    """Show statistics for all tables"""
    print(f"\n{'='*60}")
    print("19. Table statistics")
    print('='*60)
    
    with get_connection(database=database) as conn:
        # Get all tables
        tables = fetch_query(conn, "SHOW TABLES")
        
        print("\nRow counts:")
        for (table_name,) in tables:
            count = get_table_row_count(database, table_name)
            print(f"  • {table_name}: {count} rows")


def backup_table_data(database: str, table_name: str, backup_table_name: str) -> None:
    """Create a backup of a table"""
    print(f"\n{'='*60}")
    print(f"20. Backup table '{table_name}' to '{backup_table_name}'")
    print('='*60)
    
    with get_connection(database=database) as conn:
        query = f"CREATE TABLE IF NOT EXISTS {backup_table_name} LIKE {table_name}"
        execute_query(conn, query)
        
        query = f"INSERT INTO {backup_table_name} SELECT * FROM {table_name}"
        execute_query(conn, query)
        print(f"✓ Backed up {table_name} to {backup_table_name}")


# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """Main function to run all examples"""
    print("\n" + "="*60)
    print("MySQL Usage Examples with Python")
    print("="*60)
    
    # Database name for examples
    # Note: Using existing 'my_db' as dev_user doesn't have CREATE DATABASE privileges
    example_db = "my_db"
    
    try:
        # 1. Schema Management
        create_schema_if_not_exists(example_db)
        show_schemas()
        change_schema(example_db)
        
        # 2. Table Management
        show_tables(example_db)
        create_example_tables(example_db)
        show_tables(example_db)
        describe_table(example_db, "products")
        
        # 3. Data Insertion
        insert_sample_data(example_db)
        
        # 4. Querying Data
        simple_select_query(example_db)
        select_with_where_clause(example_db)
        select_with_aggregation(example_db)
        select_with_join(example_db)
        select_with_subquery(example_db)
        parameterized_query(example_db)
        
        # 5. Updates and Deletions
        update_data(example_db)
        delete_data(example_db)
        
        # 6. Transactions
        transaction_example(example_db)
        
        # 7. Advanced Queries
        window_function_example(example_db)
        common_table_expression(example_db)
        
        # 8. Utility Functions
        show_table_statistics(example_db)
        backup_table_data(example_db, "products", "products_backup")
        
        print("\n" + "="*60)
        print("✓ All examples completed successfully!")
        print("="*60)
        
    except Error as e:
        print(f"\n✗ An error occurred: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
