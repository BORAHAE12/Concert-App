import os
import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# @st.cache_resource
def create_connection():
    try:
        host = os.getenv("MYSQL_HOST")
        user = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASSWORD")
        database = os.getenv("MYSQL_DATABASE")

        if not host or not user or not database:
            print("❌ DEBUG: Missing MySQL credentials in .env file!")
            return None

        print(f"🔍 DEBUG: Connecting to MySQL -> Host: {host}, User: {user}, Database: {database}")

        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            print("✅ MySQL Connection Successful!")
            return connection

    except Error as e:
        print(f"❌ MySQL Connection Error: {e}")
        st.error("❌ Database Connection Error! Check credentials or server.")

    return None


def execute_query(connection, query, params=None, fetch_one=False):
    if not connection or not connection.is_connected():
        print("❌ DEBUG: Attempting to execute query on a closed connection.")
        return None

    try:
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        
        if query.strip().lower().startswith(("select", "insert", "delete", "update")):
            result = cursor.fetchone() if fetch_one else cursor.fetchall()
            cursor.close()  
            return result

        connection.commit()
        cursor.close()
        return None

    except Error as e:
        st.error(f"Database Error: {e}")
        return None
