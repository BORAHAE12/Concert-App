import streamlit as st
from Venue import *
from artist import *
from concert import *
from customers import *
from tickets import *
from testing_security import *
from database import *


#Function to join two tables
def join_tables(connection, table1, table2, join_condition, columns):
    columns_str = ', '.join(columns)
    query = f"""
    SELECT {columns_str}
    FROM {table1} t1
    INNER JOIN {table2} t2 ON {join_condition}
    """
    return execute_query(connection, query)

        
def join_artist_genre(connection):
    query = """
    SELECT artist.artist_name, genre.genre_name
    FROM artist
    INNER JOIN genre ON artist.genre_id = genre.genre_id
    """
    return execute_query(connection, query)

#  Login System
def login():
    st.subheader("Login")
    username = st.text_input("Username", placeholder="Enter your uswrname")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    if st.button("Login", use_container_width=True):
        connection = create_connection()
        if connection:
            query = "SELECT username, password, role FROM users WHERE username = %s"
            user = execute_query(connection, query, (username,))
            
            if user and check_password(password, user[0][1]):
                token = create_jwt_token(username, user[0][2])
                st.session_state["jwt_token"] = token
                st.session_state["authenticated"] = True
                st.success("Login successful! Reloading...")
                st.rerun()
                st.stop()
            else:
                st.error("Invalid credentials")

# Signup System
def signup():
    st.subheader("Signup")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    role = st.selectbox("Role", ["user", "admin"])
    
    if st.button("Register"):
        connection = create_connection()
        if connection:
            hashed_password = hash_password(new_password)
            query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
            execute_query(connection, query, (new_username, hashed_password, role))
            st.success("Registration successful! Please log in.")

