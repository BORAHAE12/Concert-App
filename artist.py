import streamlit as st
from mysql.connector import Error
from database import *  # Reusing existing query function

# 🎨 Artist Functions
def get_all_artists(connection):
    """Fetch all artists from the database."""
    query = "SELECT * FROM artist"
    return execute_query(connection, query)

def insert_artist(connection, artist_id, artist_name, genre_id):
    """Insert a new artist into the database."""
    if not connection or not connection.is_connected():
        st.error("❌ MySQL Connection is not available. Cannot insert artist.")
        print("❌ DEBUG: Connection is closed before insert operation.")
        return
    
    query = "INSERT INTO artist (artist_id, artist_name, genre_id) VALUES (%s, %s, %s)"
    execute_query(connection, query, (artist_id, artist_name, genre_id))
    st.success("✅ Artist added successfully!")
    print("✅ Artist inserted successfully.")

def delete_artist(connection, artist_id):
    """Delete an artist by their ID."""
    query = "DELETE FROM artist WHERE artist_id = %s"
    execute_query(connection, query, (artist_id,))
    st.success(f"🗑️ Artist with ID {artist_id} deleted successfully!")

def update_artist(connection, artist_id, new_artist_name, new_genre_id):
    """Update an existing artist."""
    query = "UPDATE artist SET artist_name = %s, genre_id = %s WHERE artist_id = %s"
    execute_query(connection, query, (new_artist_name, new_genre_id, artist_id))
    st.success("✅ Artist updated successfully!")
