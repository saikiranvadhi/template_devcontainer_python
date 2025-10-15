# MySQL with Python - Complete Guide

This guide demonstrates how to use MySQL with Python using the `use_mysql.py` script.

## Prerequisites

1. MySQL server running (via docker-compose)
2. Python environment managed by `uv`
3. `mysql-connector-python` package installed

## Installation

The required package is already added to the project:

```bash
uv add mysql-connector-python
```

## Running the Examples

Execute the complete demonstration script:

```bash
uv run python src/app/use_mysql.py
```

## What the Script Demonstrates

### 1. **Schema/Database Management**
   - ✅ Create schema if it doesn't exist
   - ✅ Show all existing schemas
   - ✅ Change default schema (USE statement)

### 2. **Table Management**
   - ✅ Show existing tables in a database
   - ✅ Create new tables with proper constraints
   - ✅ Describe table structure (DESCRIBE command)
   - ✅ Tables created: `products`, `customers`, `orders`

### 3. **Data Insertion**
   - ✅ Single row insertion with parameterized queries
   - ✅ Bulk insertion using `executemany()`
   - ✅ Sample data for products, customers, and orders

### 4. **Querying Data**
   - ✅ Simple SELECT queries
   - ✅ SELECT with WHERE clause (filtering)
   - ✅ Aggregation functions (COUNT, AVG, SUM)
   - ✅ GROUP BY queries
   - ✅ JOIN queries (INNER JOIN across multiple tables)
   - ✅ Subqueries for complex data retrieval
   - ✅ Parameterized queries (SQL injection prevention)

### 5. **Data Modification**
   - ✅ UPDATE data in tables
   - ✅ DELETE data from tables
   - ✅ Conditional updates and deletions

### 6. **Transaction Management**
   - ✅ BEGIN transaction
   - ✅ COMMIT on success
   - ✅ ROLLBACK on failure
   - ✅ Atomic operations (create order + update stock)

### 7. **Advanced SQL Features**
   - ✅ Window functions (RANK, PARTITION BY)
   - ✅ Common Table Expressions (CTE/WITH clause)
   - ✅ Complex analytical queries

### 8. **Utility Functions**
   - ✅ Get row counts for tables
   - ✅ Table statistics
   - ✅ Backup table data
   - ✅ Context managers for connection handling

## Key Features of the Script

### Connection Management
```python
@contextmanager
def get_connection(database: Optional[str] = None):
    """Automatic connection cleanup with context manager"""
    connection = mysql.connector.connect(**DB_CONFIG)
    try:
        yield connection
    finally:
        if connection.is_connected():
            connection.close()
```

### Parameterized Queries (Security)
```python
# SAFE: Prevents SQL injection
query = "SELECT * FROM products WHERE category = %s"
results = fetch_query(conn, query, ("Electronics",))

# UNSAFE: Never do this!
# query = f"SELECT * FROM products WHERE category = '{category}'"
```

### Dictionary Results
```python
# Get results as list of dictionaries
cursor = connection.cursor(dictionary=True)
cursor.execute("SELECT * FROM products")
results = cursor.fetchall()
# Results: [{'id': 1, 'name': 'Laptop', ...}, ...]
```

### Transaction Example
```python
try:
    conn.start_transaction()
    # Multiple operations
    cursor.execute("UPDATE products SET stock = stock - 1 WHERE id = 1")
    cursor.execute("INSERT INTO orders (...) VALUES (...)")
    conn.commit()  # Success
except Error:
    conn.rollback()  # Failure - undo all changes
```

## Connection Configuration

Currently configured to use the existing MySQL service:

```python
DB_CONFIG = {
    'host': 'mysql',  # Use 'mysql_server' after docker-compose restart
    'port': 3306,
    'user': 'dev_user',
    'password': 'dev_password',
}
```

**Note**: After restarting docker-compose with the updated service name, change `'host': 'mysql'` to `'host': 'mysql_server'`.

## Sample Output

The script creates and populates these tables:

- **products**: 10 items across 3 categories (Electronics, Furniture, Stationery)
- **customers**: 5 customers with contact information
- **orders**: 8 orders linking customers to products

And demonstrates:
- Aggregated statistics by category
- Customer spending analysis
- Product rankings within categories
- High-value customer identification
- Transaction-safe order processing

## Best Practices Demonstrated

1. ✅ **Use context managers** for automatic resource cleanup
2. ✅ **Parameterized queries** to prevent SQL injection
3. ✅ **Transactions** for atomic operations
4. ✅ **Error handling** with try/except blocks
5. ✅ **Connection pooling** (can be added for production)
6. ✅ **Type hints** for better code documentation
7. ✅ **Cursor cleanup** in finally blocks

## Common Patterns

### Read Operation
```python
with get_connection(database="my_db") as conn:
    results = fetch_query(conn, "SELECT * FROM products WHERE price > %s", (100,))
    for row in results:
        print(row)
```

### Write Operation
```python
with get_connection(database="my_db") as conn:
    execute_query(conn, "INSERT INTO products (name, price) VALUES (%s, %s)", 
                  ("New Product", 99.99))
```

### Bulk Insert
```python
with get_connection(database="my_db") as conn:
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO products (name, price) VALUES (%s, %s)",
        [("Product 1", 10.0), ("Product 2", 20.0), ("Product 3", 30.0)]
    )
    conn.commit()
```

## Troubleshooting

### Connection Issues
- Verify MySQL server is running: `mysql -h mysql -u dev_user -pdev_password -e "SELECT 1"`
- Check service name matches docker-compose configuration
- Ensure network connectivity between containers

### Permission Errors
- `dev_user` has limited privileges (no CREATE DATABASE)
- Use `root` user for administrative tasks
- Grant specific privileges as needed

### Import Errors
- Ensure package is installed: `uv add mysql-connector-python`
- Check virtual environment is activated: `uv run python ...`

## Related Files

- `src/app/sql/example.sql` - SQL examples without Python
- `src/app/sql/README.md` - MySQL usage documentation
- `docker-compose.yml` - MySQL service configuration

## Further Reading

- [MySQL Connector/Python Documentation](https://dev.mysql.com/doc/connector-python/en/)
- [MySQL 8.0 Reference Manual](https://dev.mysql.com/doc/refman/8.0/en/)
- [Python Database API Specification (PEP 249)](https://peps.python.org/pep-0249/)
