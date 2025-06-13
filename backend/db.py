import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="hariharan16!",
        database="voting_system"
    )
