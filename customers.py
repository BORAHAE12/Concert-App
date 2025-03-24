import streamlit as st
from mysql.connector import Error
from database import *
from testing_security import *

# 🟢 Customer Functions
def get_all_customers(connection):
    """Fetch all customers from the database."""
    query = "SELECT * FROM customer"
    return execute_query(connection, query)

def insert_customer(connection, customer_id, customer_name, email, user_name, password):
    """Insert a new customer into the database."""
    if not connection:
        st.error("❌ Database connection not established.")
        return
    
    query = "INSERT INTO customer (customer_id, customer_name, email, user_name, password) VALUES (%s, %s, %s, %s, %s)"
    execute_query(connection, query, (customer_id, customer_name, email, user_name, password))
    st.success("👤 Customer added successfully!")
    print("✅ Customer inserted successfully.")  # Debug message

def delete_customer(connection, customer_id):
    """Delete a customer by their ID."""
    query = "DELETE FROM customer WHERE customer_id = %s"
    execute_query(connection, query, (customer_id,))
    st.success(f"🗑️ Customer with ID {customer_id} deleted successfully!")

def update_customer(connection, customer_id, new_customer_name, new_email, new_user_name, new_password):
    """Update an existing customer record."""
    query = "UPDATE customer SET customer_name = %s, email = %s, user_name = %s, password = %s WHERE customer_id = %s"
    execute_query(connection, query, (new_customer_name, new_email, new_user_name, new_password, customer_id))
    st.success("✅ Customer updated successfully!")

# 🟢 Customer Order Functions
def get_all_customer_orders(connection):
    """Fetch all customer orders from the database."""
    query = "SELECT * FROM customer_order"
    return execute_query(connection, query)

def insert_customer_order(connection, customer_order_id, customer_id, registered_email_address, total_price, discount, final_price):
    """Insert a new customer order."""
    query = "INSERT INTO customer_order (customer_order_id, customer_id, registered_email_address, total_price, discount, final_price) VALUES (%s, %s, %s, %s, %s, %s)"
    execute_query(connection, query, (customer_order_id, customer_id, registered_email_address, total_price, discount, final_price))
    st.success("🛒 Customer order added successfully!")

def delete_customer_order(connection, customer_order_id):
    """Delete a customer order by its ID."""
    query = "DELETE FROM customer_order WHERE customer_order_id = %s"
    execute_query(connection, query, (customer_order_id,))
    st.success(f"🗑️ Customer Order with ID {customer_order_id} deleted successfully!")

def update_customer_order(connection, customer_order_id, new_customer_id, new_registered_email_address, new_total_price, new_discount, new_final_price):
    """Update an existing customer order."""
    query = "UPDATE customer_order SET customer_id = %s, registered_email_address = %s, total_price = %s, discount = %s, final_price = %s WHERE customer_order_id = %s"
    execute_query(connection, query, (new_customer_id, new_registered_email_address, new_total_price, new_discount, new_final_price, customer_order_id))
    st.success("✅ Customer Order updated successfully!")

def get_user_details(connection, user_id):
    """Fetch user details from the database."""
    query = "SELECT user_name, email FROM customer WHERE customer_id = %s"
    result = execute_query(connection, query, (user_id,), fetch_one=True)

    if result:
        return {"user_name": result[0], "email": result[1]}
    return None

def update_own_profile(connection, user_id, new_email, new_password):
    """Allows users to update their email and password."""
    hashed_password = hash_password(new_password)  # Ensure you have a function to hash passwords
    query = "UPDATE customer SET email = %s, password = %s WHERE customer_id = %s"
    execute_query(connection, query, (new_email, hashed_password, user_id))
    return True
