import sqlite3
class SQLiteasy:
    def __init__(self, database_name: str, database_entries: dict):
        self.database_name = database_name
        if self.database_name.endswith(".db"):
            raise ValueError("SQLiteasy: You must pass the database name without .db")
        self.database_pre_query = []
        self.database_entries = database_entries
        self.database_final_query = f"ID INTEGER PRIMARY KEY AUTOINCREMENT, {self.database_create_final_query()}"
        self.database_values = f"({",".join(("?" for x in range(len(self.database_pre_query))))})"
        self.database_inserts = f"({", ".join([key for key, item in self.database_entries.items()])})"
    def database_create_final_query(self):
        for key, value in self.database_entries.items():
            type_value = value["type"]
            notnull = value["notnull"]
            column_name = key
            match type_value, notnull:
                case ("string", True):
                    self.database_pre_query.append(f"{column_name} TEXT NOT NULL")
                case ("string", False):
                    self.database_pre_query.append(f"{column_name} TEXT")
                case ("integer", True):
                    self.database_pre_query.append(f"{column_name} INTEGER NOT NULL")
                case ("integer", False):
                    self.database_pre_query.append(f"{column_name} INTEGER")
                case ("binary", True):
                    self.database_pre_query.append(f"{column_name} BLOB NOT NULL")
                case ("binary", False):
                    self.database_pre_query.append(f"{column_name} BLOB")
                case ("float", True):
                    self.database_pre_query.append(f"{column_name} REAL NOT NULL")
                case ("float", False):
                    self.database_pre_query.append(f"{column_name} REAL")
                case ("boolean", True):
                    self.database_pre_query.append(f"{column_name} BOOLEAN NOT NULL")
                case ("boolean", False):
                    self.database_pre_query.append(f"{column_name} BOOLEAN")
        return ", ".join(self.database_pre_query)
    
    def fetch_database(self, indent=True): # See the query that will be executed
        conn = sqlite3.connect(f"{self.database_name}.db")
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self.database_name}")
            data = cursor.fetchall()
            conn.close()
            if indent:
                for item in data:
                    print(f"{item}\n")
            else:
                print(data)
            return data
        except Exception as e:
            print("SQLiteasy: Something we  nt wrong")
            print(e)
            conn.close()
    def fetch_database_by(self, where: str, by: str, indent=True):
        conn = sqlite3.connect(f"{self.database_name}.db")
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self.database_name} WHERE {where} = ?", (by,))
            data = cursor.fetchall()
            conn.close()
            if data and indent:
                for item in data:
                    print(f"{item}\n")
            elif data and not indent:
                pass
            else:
                print("SQLiteasy: No data found with those parameters 12")
            conn.close()
            return data if data else None
        except Exception as e:
            print("Something went wrong")
            print(e)
            conn.close()
            raise ValueError("SQLiteasy: You must pass the same keys as the database entries")
    def fetch_database_by_and(self, where: str, by: str, and_where: str, and_by: str, indent=True):
        conn = sqlite3.connect(f"{self.database_name}.db")
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self.database_name} WHERE {where} = ? AND {and_where} = ?", (by, and_by))
            data = cursor.fetchall()
            conn.close()
            if data and indent:
                for item in data:
                    print(f"{item}\n")
            elif data and not indent:
                print(data)
            else:
                print("SQLiteasy: No data found with those parameters")
            conn.close()
            return data if data else None
        except Exception as e:
            print("Something went wrong")
            print(e)
            conn.close()
    def fetch_database_by_or(self, where: str, by: str, or_where: str, or_by: str, indent=True):
        conn = sqlite3.connect(f"{self.database_name}.db")
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self.database_name} WHERE {where} = ? OR {or_where} = ?", (by, or_by))
            data = cursor.fetchall()
            conn.close()
            if data and indent:
                for item in data:
                    print(f"{item}\n")
            elif data and not indent:
                print(data)
            else:
                print("SQLiteasy: No data found with those parameters")
            conn.close()
            return data if data else None
        except Exception as e:
            print("Something went wrong")
            print(e)
            conn.close()

    def create_database(self):
        if ".db" in self.database_name:
            raise ValueError("SQLiteasy: You must pass the database name without .db")
        conn = sqlite3.connect(f"{self.database_name}.db")
        cursor = conn.cursor()
        try:
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.database_name} ({self.database_final_query})")
        except Exception as e:
            print("SQLiteasy: Something went wrong")
            print(e)
        conn.close()
        
    def insert_database(self, **kwargs):
        from collections import Counter
        verify = list(self.database_entries.keys())
        sended_keys = list(kwargs.keys())
        if Counter(verify) == Counter(sended_keys):
            try:
                conn = sqlite3.connect(f"{self.database_name}.db")
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO {self.database_name} {self.database_inserts} VALUES {self.database_values}", tuple(kwargs.values()))
                conn.commit()
                conn.close()
                print("SQLiteasy: Values inserted")
            except:
                raise TypeError("SQLiteasy: You have inserted the correct values, but there is a problem with the database, check if the database exists, try with .create_database()") 
        else:
            raise ValueError("SQLiteasy: You must pass the same keys as the database entries")
        
    def update_database_by(self, column_to_update: str, condition_column: str, condition_value, new_value: str):
        conn = sqlite3.connect(f"{self.database_name}.db")
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"UPDATE {self.database_name} SET {column_to_update} = ? WHERE {condition_column} = ?", 
                (new_value, condition_value)
            )
            conn.commit()
            print("Values updated")
        except sqlite3.Error as e:
            print("An error occurred:", e)
        finally:
            conn.close()
    def delete_database_row_by(self, condition_column, condition_value):
        conn = sqlite3.connect(f"{self.database_name}.db")
        cursor = conn.cursor()
        try:
            cursor.execute(f"DELETE FROM {self.database_name} WHERE {condition_column} = ?", (condition_value,))
        except:
            print("SQLiteasy: Something went wrong, check if the column exists, or if the condition exists on the given column")
        conn.commit()
        conn.close()



""" entries_to_test = {
    "user_name": {"type": "string", "notnull": True},
    "user_email": {"type": "string", "notnull": True},
    "user_isregistered": {"type": "boolean", "notnull": False},
} """

""" test_db = SQLiteasy("test", entries_to_test)
test_db.create_database()
#test_db.insert_database(user_name="josue", user_email="a@gmail.com", user_isregistered="0")
#test_db.insert_database(user_name="arias", user_email="b@gmail.com", user_isregistered="1")
#test_db.insert_database(user_name="gauna", user_email="c@gmail.com", user_isregistered="2")
#test_db.insert_database(user_name="aborrar", user_email="d@gmail.com", user_isregistered="3")
test_db.delete_database_row_by("user_name", "arias")
test_db.fetch_database(indent=True) """