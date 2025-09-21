import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
import logging

# Public API exports
__all__ = ["DatabaseManager"]

DB_FILE = str(Path(__file__).resolve().parent / "text.db")


class DatabaseManager:
    """SQLite database manager providing standard database operation interface"""

    def __init__(self, db_path: str = DB_FILE):
        """
        Initialize database manager

        Args:
            db_path: Database file path, defaults to DB_FILE
        """
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self._ensure_db_directory()

    def _ensure_db_directory(self) -> None:
        """Ensure database directory exists"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def get_connection(self):
        """Context manager for database connection"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable dictionary-style access
            yield conn
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            self.logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Execute query and return results

        Args:
            query: SQL query statement
            params: Query parameters

        Returns:
            List of query results
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def execute_single(
        self, query: str, params: tuple = ()
    ) -> Optional[Dict[str, Any]]:
        """
        Execute query and return single result

        Args:
            query: SQL query statement
            params: Query parameters

        Returns:
            Single query result or None
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """
        Execute update operations (INSERT, UPDATE, DELETE)

        Args:
            query: SQL statement
            params: Parameters

        Returns:
            Number of affected rows
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount

    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """
        Execute batch update operations

        Args:
            query: SQL statement
            params_list: List of parameters

        Returns:
            Number of affected rows
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            return cursor.rowcount

    def create_table(self, table_name: str, columns: Dict[str, str]) -> bool:
        """
        Create table

        Args:
            table_name: Table name
            columns: Column definition dictionary, format: {'column_name': 'column_type'}

        Returns:
            Whether creation was successful
        """
        try:
            columns_def = ", ".join(
                [f"{name} {type_}" for name, type_ in columns.items()]
            )
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})"
            self.execute_update(query)
            return True
        except sqlite3.Error as e:
            self.logger.error(f"Failed to create table {table_name}: {e}")
            return False

    def table_exists(self, table_name: str) -> bool:
        """
        Check if table exists

        Args:
            table_name: Table name

        Returns:
            Whether table exists
        """
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        result = self.execute_single(query, (table_name,))
        return result is not None

    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Get table structure information

        Args:
            table_name: Table name

        Returns:
            List of table structure information
        """
        query = f"PRAGMA table_info({table_name})"
        return self.execute_query(query)


# Create default database manager instance
db_manager = DatabaseManager()


if __name__ == "__main__":
    # Test example for DatabaseManager class

    # print("=== Testing DatabaseManager Class ===")

    # Test 1: Using in-memory database for testing
    # print("\n--- Test 1: In-memory database ---")
    test_db = DatabaseManager(DB_FILE)  # Use in-memory database for testing

    # Create test table
    # columns = {
    #     "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    #     "name": "TEXT NOT NULL",
    #     "age": "INTEGER",
    #     "email": "TEXT UNIQUE",
    # }

    # success = test_db.create_table("users", columns)
    # print(f"Table creation successful: {success}")

    # Insert test data using class methods
    # insert_sql = "INSERT INTO users (name, age, email) VALUES (?, ?, ?)"
    # test_data = [
    #     ("Alice", 25, "alice@example.com"),
    #     ("Bob", 30, "bob@example.com"),
    #     ("Charlie", 35, "charlie@example.com"),
    # ]

    # affected_rows = test_db.execute_many(insert_sql, test_data)
    # print(f"Inserted {affected_rows} rows using execute_many")

    # Query all users using class method
    all_users = test_db.execute_query("SELECT * FROM documents ORDER BY id")
    # print(f"All users: {all_users}")

    # Query single user using class method
    single_user = test_db.execute_single("SELECT * FROM documents WHERE id = ?", (1,))
    print(f"Single user (Alice): {single_user}")

    # Check table info
    table_info = test_db.get_table_info("documents")
    print(f"Table info: {table_info}")

    # Test 2: Using default database file
    print("\n--- Test 2: Default database file ---")
    default_db = db_manager  # Use the default instance

    # # Create test table in default database
    # success = default_db.create_table(
    #     "products",
    #     {
    #         "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    #         "product_name": "TEXT NOT NULL",
    #         "price": "REAL",
    #         "created_at": "DATETIME DEFAULT CURRENT_TIMESTAMP",
    #     },
    # )
    # print(f"Products table creation successful: {success}")

    # # Insert sample data
    # products_data = [
    #     ("Laptop", 999.99),
    #     ("Mouse", 25.50),
    #     ("Keyboard", 75.00),
    # ]

    # for product_name, price in products_data:
    #     default_db.execute_update(
    #         "INSERT INTO products (product_name, price) VALUES (?, ?)",
    #         (product_name, price),
    #     )

    # print("Inserted sample products")

    # Query existing tables in default database (if any)
    existing_tables = default_db.execute_query(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )
    print(f"Existing tables in default database: {existing_tables}")

    # Test 3: Loading and querying existing database
    print("\n--- Test 3: Loading existing database file ---")

    # Create a custom database file for testing
    # custom_db_path = str(Path(__file__).resolve().parent / "test_custom.db")
    # custom_db = DatabaseManager(custom_db_path)

    # # Create and populate test data in custom database
    # custom_db.create_table(
    #     "orders",
    #     {
    #         "order_id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    #         "customer_name": "TEXT NOT NULL",
    #         "total_amount": "REAL",
    #         "order_date": "DATETIME DEFAULT CURRENT_TIMESTAMP",
    #     },
    # )

    # # Insert orders data
    # orders_data = [
    #     ("John Doe", 150.75),
    #     ("Jane Smith", 89.99),
    #     ("Mike Johnson", 245.50),
    # ]
    # custom_db.execute_many(
    #     "INSERT INTO orders (customer_name, total_amount) VALUES (?, ?)", orders_data
    # )

    # print(f"Created custom database at: {custom_db_path}")

    # Demonstrate loading existing database (if it exists)
    custom_db_path = str(Path(__file__).resolve().parent / "text.db")
    existing_db = DatabaseManager(custom_db_path)  # Load the existing database

    # Check what tables exist in the database
    all_tables = existing_db.execute_query(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )
    print(f"All tables in existing database: {all_tables}")

    # Query existing data (if tables exist)
    # if all_tables:
    #     for table in all_tables:
    #         table_name = table["name"]
    #         print(f"\n--- Querying table: {table_name} ---")

    #         # Check if table exists
    #         has_table = existing_db.table_exists(table_name)
    #         print(f"Table '{table_name}' exists: {has_table}")

    #         # Get table structure
    #         table_info = existing_db.get_table_info(table_name)
    #         print(f"Table structure: {table_info}")

    #         # Query all records from the table
    #         try:
    #             all_records = existing_db.execute_query(
    #                 f"SELECT * FROM {table_name} LIMIT 5"
    #             )
    #             print(f"Sample records (first 5): {all_records}")

    #             # Count total records
    #             count_result = existing_db.execute_single(
    #                 f"SELECT COUNT(*) as count FROM {table_name}"
    #             )
    #             print(f"Total records: {count_result}")

    #         except sqlite3.Error as e:
    #             print(f"Error querying table {table_name}: {e}")

    # # Update existing record
    # updated_rows = existing_db.execute_update(
    #     "UPDATE orders SET total_amount = ? WHERE customer_name = ?",
    #     (95.99, "Jane Smith"),
    # )
    # print(f"Updated {updated_rows} orders")

    # # Verify update
    # updated_order = existing_db.execute_single(
    #     "SELECT * FROM orders WHERE customer_name = ?", ("Jane Smith",)
    # )
    # print(f"Jane Smith's updated order: {updated_order}")

    # # Clean up - remove test database file
    # try:
    #     Path(custom_db_path).unlink()
    #     print("Cleaned up test database file")
    # except FileNotFoundError:
    #     pass

    print("\nTest completed successfully!")
    print("\n=== Usage Examples ===")
    print("# To use in your code:")
    print("from src.backend.database.sqlite import DatabaseManager, db_manager")
    print("")
    print("# Use default database:")
    print("users = db_manager.execute_query('SELECT * FROM users')")
    print("")
    print("# Use custom database:")
    print("custom_db = DatabaseManager('/path/to/your/database.db')")
    print("data = custom_db.execute_query('SELECT * FROM your_table')")
