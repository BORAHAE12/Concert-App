import streamlit as st
from mysql.connector import Error
from database import *
# 🎵 Genre Functions
def get_all_genres(connection):
    """Fetch all genres from the database."""
    query = "SELECT * FROM genre"
    return execute_query(connection, query)

def insert_genre(connection, genre_id, genre_name):
    """Insert a new genre into the database."""
    query = "INSERT INTO genre (genre_id, genre_name) VALUES (%s, %s)"
    execute_query(connection, query, (genre_id, genre_name))
    st.success("✅ Genre added successfully!")

def delete_genre(connection, genre_id):
    """Delete a genre by its ID."""
    query = "DELETE FROM genre WHERE genre_id = %s"
    execute_query(connection, query, (genre_id,))
    st.success(f"🗑️ Genre with ID {genre_id} deleted successfully!")

def update_genre(connection, genre_id, new_genre_name):
    """Update an existing genre."""
    query = "UPDATE genre SET genre_name = %s WHERE genre_id = %s"
    execute_query(connection, query, (new_genre_name, genre_id))
    st.success("✅ Genre updated successfully!")
