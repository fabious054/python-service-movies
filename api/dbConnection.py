import mysql.connector as mysql 
from mysql.connector import Error

class DbConnection:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print(f"Conectado ao banco de dados {self.database} em {self.host}")

        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")


    def close(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            print("Conexão ao MySQL foi encerrada")


    def execute(self, query):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        print(f"Query executada com sucesso: {query}")
        return cursor.fetchall()
    
    def insert(self, query):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        self.connection.commit()
        return cursor.lastrowid
    
    def update(self, query):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        self.connection.commit()
        return cursor.rowcount
    
    def delete(self, query):

        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        self.connection.commit()
        return cursor.rowcount
    
    def truncate(self, table):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"TRUNCATE TABLE {table}")
        self.connection.commit()
        return cursor.rowcount
    
    def drop(self, table):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"DROP TABLE {table}")
        self.connection.commit()
        return cursor.rowcount
    
    def create(self, query):

        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        self.connection.commit()
        return cursor.rowcount
    
    