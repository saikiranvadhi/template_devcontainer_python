# SQL Examples

This folder contains SQL examples that demonstrate various database operations.

## Files

- `example.sql` - Comprehensive SQL examples including table creation, data insertion, and queries

## How to Use

### Method 1: Execute SQL file directly

From inside the container, run:

```bash
mysql -h mysql_server -u dev_user -pdev_password my_db < src/app/sql/example.sql
```

Or connect as root:

```bash
mysql -h mysql_server -u root -proot my_db < src/app/sql/example.sql
```

### Method 2: Interactive MySQL session

Connect to MySQL interactively:

```bash
mysql -h mysql_server -u dev_user -pdev_password my_db
```

Then source the SQL file:

```sql
source src/app/sql/example.sql;
```

### Method 3: Execute specific queries

Run a single query:

```bash
mysql -h mysql_server -u dev_user -pdev_password my_db -e "SELECT * FROM users;"
```

### Connection Details

- **Host**: `mysql_server` (service name from docker-compose)
- **Port**: `3306` (inside container) / `3306` (from host machine)
- **Database**: `my_db`
- **User**: `dev_user`
- **Password**: `dev_password`
- **Root Password**: `root`

### From Host Machine

To connect from your host machine:

```bash
mysql -h 127.0.0.1 -P 3306 -u dev_user -pdev_password my_db
```

Note: Port 3306 is mapped from the container to the host machine.

## Example Queries

The `example.sql` file includes:

- **Table Creation**: Users, Posts, and Comments tables with relationships
- **Sample Data**: Pre-populated data for testing
- **Basic Queries**: SELECT, INSERT, UPDATE, DELETE operations
- **Advanced Queries**: JOINs, aggregations, and complex queries
- **Utility Commands**: DESCRIBE, SHOW TABLES, row counts

## Testing the Setup

After executing `example.sql`, verify everything works:

```bash
# Check tables were created
mysql -h mysql_server -u dev_user -pdev_password my_db -e "SHOW TABLES;"

# Check sample data
mysql -h mysql_server -u dev_user -pdev_password my_db -e "SELECT COUNT(*) FROM users;"

# Test a JOIN query
mysql -h mysql_server -u dev_user -pdev_password my_db -e "
SELECT p.title, u.username 
FROM posts p 
INNER JOIN users u ON p.user_id = u.id 
LIMIT 5;"
```

## Tips

- The SQL file uses `ON DUPLICATE KEY UPDATE` for idempotent inserts
- Destructive operations (DELETE, DROP) are commented out for safety
- Foreign key constraints ensure data integrity
- Indexes are added for common query patterns

## Python Integration

To use these tables with Python, install `mysql-connector-python` or `pymysql`:

```python
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host='mysql_server',
    port=3306,
    user='dev_user',
    password='dev_password',
    database='my_db'
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
results = cursor.fetchall()

for row in results:
    print(row)

conn.close()
```
