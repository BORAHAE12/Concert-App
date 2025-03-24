import streamlit as st
from mysql.connector import Error
from database import * # Reusing existing query function

# 🟢 Concert Functions
def get_all_concerts(connection):
    """Fetch all concerts."""
    query = "SELECT * FROM concert"
    return execute_query(connection, query)

def insert_concert(connection, concert_id, concert_name, artist_id, date, venue_id, concert_group_id):
    """Insert a new concert into the database."""
    query = "INSERT INTO concert (concert_id, concert_name, artist_id, date, venue_id, concert_group_id) VALUES (%s, %s, %s, %s, %s, %s)"
    execute_query(connection, query, (concert_id, concert_name, artist_id, date, venue_id, concert_group_id))
    st.success("✅ Concert added successfully!")

def delete_concert(connection, concert_id):
    """Delete a concert by its ID."""
    query = "DELETE FROM concert WHERE concert_id = %s"
    execute_query(connection, query, (concert_id,))
    st.success(f"🗑️ Concert with ID {concert_id} deleted successfully!")

def update_concert(connection, concert_id, new_concert_name, new_artist_id, new_date, new_venue_id, new_concert_group_id):
    """Update an existing concert."""
    query = "UPDATE concert SET concert_name = %s, artist_id = %s, date = %s, venue_id = %s, concert_group_id = %s WHERE concert_id = %s"
    execute_query(connection, query, (new_concert_name, new_artist_id, new_date, new_venue_id, new_concert_group_id, concert_id))
    st.success("✅ Concert updated successfully!")

# 🟢 Concert Group Functions
def get_all_concert_groups(connection):
    """Fetch all concert groups."""
    query = "SELECT * FROM concert_group"
    return execute_query(connection, query)

def insert_concert_group(connection, concert_group_id, concert_group_name):
    """Insert a new concert group."""
    query = "INSERT INTO concert_group (concert_group_id, concert_group_name) VALUES (%s, %s)"
    execute_query(connection, query, (concert_group_id, concert_group_name))
    st.success("✅ Concert group added successfully!")

def delete_concert_group(connection, concert_group_id):
    """Delete a concert group by its ID."""
    query = "DELETE FROM concert_group WHERE concert_group_id = %s"
    execute_query(connection, query, (concert_group_id,))
    st.success(f"🗑️ Concert Group with ID {concert_group_id} deleted successfully!")

def update_concert_group(connection, concert_group_id, new_concert_group_name):
    """Update an existing concert group."""
    query = "UPDATE concert_group SET concert_group_name = %s WHERE concert_group_id = %s"
    execute_query(connection, query, (new_concert_group_name, concert_group_id))
    st.success("✅ Concert Group updated successfully!")

def get_available_concerts(connection):
    """Fetch all available concerts."""
    query = "SELECT concert_id, concert_name, date, venue_id FROM concert WHERE date >= CURDATE()"
    return execute_query(connection, query)
