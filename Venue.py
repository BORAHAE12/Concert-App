import streamlit as st
from mysql.connector import Error
from database import *

# 🏟️ Venue Functions
def get_all_venues(connection):
    """Fetch all venues from the database."""
    query = "SELECT * FROM venue"
    return execute_query(connection, query)

def insert_venue(connection, venue_id, venue_name, location, venue_type, capacity):
    """Insert a new venue into the database."""
    query = "INSERT INTO venue (venue_id, venue_name, location, type, capacity) VALUES (%s, %s, %s, %s, %s)"
    execute_query(connection, query, (venue_id, venue_name, location, venue_type, capacity))
    st.success("✅ Venue added successfully!")

def delete_venue(connection, venue_id):
    """Delete a venue by its ID."""
    query = "DELETE FROM venue WHERE venue_id = %s"
    execute_query(connection, query, (venue_id,))
    st.success("🗑️ Venue deleted successfully!")

def update_venue(connection, venue_id, new_venue_name, new_location, new_type, new_capacity):
    """Update an existing venue."""
    query = "UPDATE venue SET venue_name = %s, location = %s, type = %s, capacity = %s WHERE venue_id = %s"
    execute_query(connection, query, (new_venue_name, new_location, new_type, new_capacity, venue_id))
    st.success("✅ Venue updated successfully!")
