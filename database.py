import sqlite3
from typing import Any, List, Tuple, Union, Optional


class SQLiteDatabase:
    def __init__(self, db_name: str):
        """
        Initialize the SQLiteDatabase instance with a database file name.
        If the database does not exist, it will create one.

        :param db_name: Name of the SQLite database file.
        """
        self.db_name = db_name
        self.connection = self._connect()

    def _connect(self) -> sqlite3.Connection:
        """
        Establish a connection to the SQLite database.

        :return: SQLite connection object.
        """
        try:
            return sqlite3.connect(self.db_name)
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def execute_query(self, query: str, params: Optional[Union[Tuple, List]] = None) -> None:
        """
        Execute a query that modifies the database (INSERT, UPDATE, DELETE).

        :param query: SQL query string.
        :param params: Optional parameters for the query.
        """
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            raise

    def execute_query_many(self, query: str, params_list: List[Tuple]) -> None:
        """
        Executes a batch of queries with the same SQL statement and different parameters.

        :param query: SQL query to execute.
        :param params_list: List of parameter tuples to bind for each execution.
        """
        try:
            cursor = self.connection.cursor()
            cursor.executemany(query, params_list)  # Use executemany for batch execution
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error while batch executing queries: {e}")
            raise

    def fetch_all(self, query: str, params: Optional[Union[Tuple, List]] = None) -> List[Tuple[Any, ...]]:
        """
        Execute a SELECT query and fetch all rows.

        :param query: SQL SELECT query string.
        :param params: Optional parameters for the query.
        :return: List of rows, where each row is a tuple.
        """
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            raise

    def fetch_one(self, query: str, params: Optional[Union[Tuple, List]] = None) -> Optional[Tuple[Any, ...]]:
        """
        Execute a SELECT query and fetch a single row.

        :param query: SQL SELECT query string.
        :param params: Optional parameters for the query.
        :return: A single row as a tuple, or None if no rows are found.
        """
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            raise

    def close_connection(self) -> None:
        """
        Close the connection to the database.
        """
        try:
            if self.connection:
                self.connection.close()
        except sqlite3.Error as e:
            print(f"Error closing the connection: {e}")
            raise