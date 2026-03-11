import sqlite3
from typing import Optional

class DBManager:
    def __init__(self, dbPath: str = "database.db"):
        self.dbPath = dbPath
        self.connection = self.connect()
    
    def __exit__(self):
        if self.connection:
            self.close()
    
    def connect(self):
        self.connection = sqlite3.connect(self.dbPath)
        self.connection.row_factory = sqlite3.Row
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
        
    def execute(self, query, params) -> sqlite3.Cursor:
        """
        Execute INSERT/UPDATE/DELETE queries
        Returns cursor to access lastrowid and rowcount
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor
        
        except sqlite3.Error as err:
            self.connection.rollback()
            print("Query failed:", err)
            print("Quary:", query)
            print("Parameters: params")
            raise 
    
    def fetchOneRow(self, query: str, params: tuple = ()) -> Optional[dict]:
        """Fetch a single row as a dictionary"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None
        
        except sqlite3.Error as err:
            self.connection.rollback()
            print("Query failed:", err)
            print("Quary:", query)
            print("Parameters:", params)
            raise 
    
    def fetchAllRows(self, query: str, params: tuple = ()) -> list[dict]:
        """Fetch all rows as a list of dictionaries"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
        
        except sqlite3.Error as err:
            self.connection.rollback()
            print("Query failed:", err)
            print("Quary:", query)
            print("Parameters:", params)
            raise 

