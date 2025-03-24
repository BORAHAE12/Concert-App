import streamlit as st
from mysql.connector import Error
from database import *

# 🟢 Order Ticket Functions
def get_all_order_tickets(connection):
    query = "SELECT * FROM order_ticket"
    return execute_query(connection, query)

def insert_order_ticket(connection, order_ticket_id, customer_order_id, ticket_id):
    query = "INSERT INTO order_ticket (order_ticket_id, customer_order_id, ticket_id) VALUES (%s, %s, %s)"
    execute_query(connection, query, (order_ticket_id, customer_order_id, ticket_id))
    st.success("✅ Order ticket added successfully!")

def delete_order_ticket(connection, order_ticket_id):
    query = "DELETE FROM order_ticket WHERE order_ticket_id = %s"
    execute_query(connection, query, (order_ticket_id,))  # Tuple should be (order_ticket_id,)
    st.success(f"🗑️ Order Ticket with ID {order_ticket_id} deleted successfully!")

def update_order_ticket(connection, order_ticket_id, new_customer_order_id, new_ticket_id):
    query = "UPDATE order_ticket SET customer_order_id = %s, ticket_id = %s WHERE order_ticket_id = %s"
    execute_query(connection, query, (new_customer_order_id, new_ticket_id, order_ticket_id))
    st.success("✅ Order Ticket updated successfully!")

# 🟢 Ticket Functions
def get_all_tickets(connection):
    query = "SELECT * FROM ticket"
    return execute_query(connection, query)

def insert_ticket(connection, ticket_id, serial_number, concert_id, ticket_category_id, seat, purchase_date):
    query = "INSERT INTO ticket (ticket_id, serial_number, concert_id, ticket_category_id, seat, purchase_date) VALUES (%s, %s, %s, %s, %s, %s)"
    execute_query(connection, query, (ticket_id, serial_number, concert_id, ticket_category_id, seat, purchase_date))
    st.success("✅ Ticket added successfully!")

def delete_ticket(connection, ticket_id):
    query = "DELETE FROM ticket WHERE ticket_id = %s"
    execute_query(connection, query, (ticket_id,))
    st.success(f"🗑️ Ticket with ID {ticket_id} deleted successfully!")

def update_ticket(connection, ticket_id, new_serial_number, new_concert_id, new_ticket_category_id, new_seat, new_purchase_date):
    query = "UPDATE ticket SET serial_number = %s, concert_id = %s, ticket_category_id = %s, seat = %s, purchase_date = %s WHERE ticket_id = %s"
    execute_query(connection, query, (new_serial_number, new_concert_id, new_ticket_category_id, new_seat, new_purchase_date, ticket_id))
    st.success("✅ Ticket updated successfully!")

def get_user_tickets(connection, user_id):
    """Fetch all tickets booked by a user."""
    query = """
        SELECT t.ticket_id, c.concert_name, t.seat, t.purchase_date
        FROM ticket t
        JOIN concert c ON t.concert_id = c.concert_id
        WHERE t.customer_id = %s
    """
    return execute_query(connection, query, (user_id,))

def book_ticket(connection, user_id, concert_id, ticket_category, seat):
    """Book a new ticket for a user."""
    
    query = """
        INSERT INTO ticket (customer_id, concert_id, ticket_category_id, seat, purchase_date)
        VALUES (%s, %s, (SELECT ticket_category_id FROM ticket_category WHERE description = %s LIMIT 1), %s, NOW())
    """
    
    return execute_query(connection, query, (user_id, concert_id, ticket_category, seat))

def cancel_ticket(connection, ticket_id):
    """Cancel a booked ticket and remove it from the system."""
    
    query = "DELETE FROM ticket WHERE ticket_id = %s"
    
    return execute_query(connection, query, (ticket_id,))


# 🟢 Ticket Category Functions
def get_all_ticket_categories(connection):
    query = "SELECT * FROM ticket_category"
    return execute_query(connection, query)

def insert_ticket_category(connection, ticket_category_id, description, price, start_date, end_date, area, concert_id):
    query = "INSERT INTO ticket_category (ticket_category_id, description, price, start_date, end_date, area, concert_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    execute_query(connection, query, (ticket_category_id, description, price, start_date, end_date, area, concert_id))
    st.success("✅ Ticket category added successfully!")

def delete_ticket_category(connection, ticket_category_id):
    query = "DELETE FROM ticket_category WHERE ticket_category_id = %s"
    execute_query(connection, query, (ticket_category_id,))
    st.success(f"🗑️ Ticket Category with ID {ticket_category_id} deleted successfully!")

def update_ticket_category(connection, ticket_category_id, new_description, new_price, new_start_date, new_end_date, new_area, new_concert_id):
    query = "UPDATE ticket_category SET description = %s, price = %s, start_date = %s, end_date = %s, area = %s, concert_id = %s WHERE ticket_category_id = %s"
    execute_query(connection, query, (new_description, new_price, new_start_date, new_end_date, new_area, new_concert_id, ticket_category_id))
    st.success("✅ Ticket Category updated successfully!")

