import streamlit as st
import bcrypt
from mysql.connector import Error
from testing_app import execute_query  # Reusing existing query function

# 🔐 Hash Password
def hash_password(password):
    """Hashes a password for secure storage."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# 🔑 Verify Password
def check_password(stored_password, provided_password):
    """Compares stored hashed password with user input."""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

# 🟢 Create New User (For Users)
def register_user(connection, username, password):
    """Registers a new user with hashed password (Default role: user)."""
    hashed_pw = hash_password(password)
    query = "INSERT INTO users (username, password, role) VALUES (%s, %s, 'user')"
    execute_query(connection, query, (username, hashed_pw))
    st.success(f"✅ User '{username}' registered successfully!")

# 🔍 Authenticate User
def authenticate_user(connection, username, password):
    """Verifies login credentials and returns user details if valid."""
    query = "SELECT id, password, role FROM users WHERE username = %s"
    result = execute_query(connection, query, (username,), fetch_one=True)

    if result:
        user_id, stored_password, role = result
        if check_password(stored_password, password):
            return {"id": user_id, "username": username, "role": role}
    return None

# 📄 Get All Users (Admin Only)
def get_all_users(connection):
    """Fetch all users (Admin access required)."""
    query = "SELECT id, username, role FROM users"
    return execute_query(connection, query)

# 🔄 Update User Role (Admin Only)
def update_user_role(connection, user_id, new_role):
    """Update a user's role (Admin access required)."""
    query = "UPDATE users SET role = %s WHERE id = %s"
    execute_query(connection, query, (new_role, user_id))
    st.success(f"🔄 User ID {user_id} role updated to '{new_role}'.")

# ❌ Delete User (Admin Only)
def delete_user(connection, user_id):
    """Delete a user securely (Admin access required)."""
    query = "DELETE FROM users WHERE id = %s"
    execute_query(connection, query, (user_id,))
    st.success(f"🗑️ User ID {user_id} deleted successfully!")

# 🔄 Update User Profile (Users Only)
def update_user_profile(connection, user_id, new_password):
    """Allow users to update their own password."""
    hashed_pw = hash_password(new_password)
    query = "UPDATE users SET password = %s WHERE id = %s"
    execute_query(connection, query, (hashed_pw, user_id))
    st.success("🔄 Password updated successfully!")
