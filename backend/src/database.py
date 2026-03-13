import sqlite3
from typing import Optional, Any
from random import randint

class DBManager:
    def __init__(self, dbPath: str = "database.db"):
        self.dbPath = dbPath
        self.connection = self.connect()
    
    def __exit__(self):
        if self.connection:
            self.close()
    
    def connect(self):
        self.connection = sqlite3.connect(self.dbPath, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        print("Connected to ", self.dbPath)
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
        
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
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
    
    def fetchAllRows(self, query: str, params: tuple = ()) -> Optional[list[dict]]:
        """Fetch all rows as a list of dictionaries"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows] if rows else None 
        
        except sqlite3.Error as err:
            self.connection.rollback()
            print("Query failed:", err)
            print("Quary:", query)
            print("Parameters:", params)
            raise 
    
    def getRandomGame(self) -> Optional[dict]:
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT count(*) FROM games")
            result = cursor.fetchone()
            
            query = """SELECT * FROM games WHERE id= ?"""
            params = (randint(1, result[0]),)
            row = self.fetchOneRow(query, params)
            
            return dict(row) if row else None
        
        except sqlite3.Error as err:
            self.connection.rollback()
            print("Query failed:", err)
            raise
    
    def getTitles(self) -> Optional[list]:
        try:
            query = """SELECT title FROM games"""
            return self.fetchAllRows(query)
                    
        except sqlite3.Error as err:
            self.connection.rollback()
            print("Query failed:", err)
            print("Query:", query)
            raise
    