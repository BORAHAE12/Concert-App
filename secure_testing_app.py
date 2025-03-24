import streamlit as st

import pandas as pd
import plotly.express as px
import mysql.connector
from mysql.connector import Error
from Venue import *
from artist import *
from concert import *
from customers import *
from tickets import *
from testing_security import *
from Admin_dashboard import *
from User_dashboard import *
from testing_app import *


# Custom Styling
st.set_page_config(page_title="Concert Management", page_icon= "🎵", layout="wide")
st.markdown(""" 
        <style> 
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: White;
            font-size: 16px;
            border-radius: 10px;
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
            border: 1px solid #ddd;
            padding: 10px
        }
        </style>
            """, unsafe_allow_html=True)


# Streamlit app
def main():
    st.title("🎵 Concert Management Web App")
    #st.set_page_config(page_title= "Concert Management Web App", page_icon= "🎵", layout= "wide")
    
    if "jwt_token" in st.session_state:
        user_data = decode_jwt_token(st.session_state["jwt_token"])
        if user_data:
            st.sidebar.success(f"Welcome, {user_data['username']} (Role: {user_data['role']})")
            
            tab1, tab2 = st.tabs(["Home", "Dashboard"])
            with tab1:
                st.title(" Welcome to Concert Management")
                st.write("Book and Mange Concerts with ease")
            
            with tab2:
                if user_data["role"] == "admin":
                    show_admin_dashboard()
                else:
                    show_user_dashboard()
                    
            if st.sidebar.button("Logout", use_container_width=True):
                del st.session_state["jwt_token"]
                st.session_state["authenticated"] = False
                st.rerun()
                st.stop()
        else:
            st.warning("Session expired. Please log in again.")
            del st.session_state["jwt_token"]
            st.session_state["authenticated"] = False
    else:
        choice = st.radio("Choose an option", ["Login", "Signup"], horizontal=True)
        if choice == "Login":
            login()
        else:
            signup()

# Admin Dashboard
# def show_admin_dashboard():
#     st.subheader("Admin Dashboard 🛠️")
#     st.write("⚡ You have full access to manage concerts, users, and reports.")
#     # st.sidebar.subheader("Admin Actions")
#     # st.sidebar.button("Manage Users")
#     # st.sidebar.button("View Reports")
#     connection = create_connection()

#     if connection:
#             col1, col2 = st.columns([1, 3])
#             # col1.image("concert_logo.png", width=100)
#             col2.title("Concert Management Web App")
#             # Sidebar for selecting a table
#             selected_table = st.sidebar.selectbox("Concert", ["artist", "concert", "concert_group", "customer", "customer_order", "genre", "order_ticket", "ticket", "ticket_category", "venue", "join tables"])

#             if selected_table == "artist":
#                 # Add artist CRUD operations
#                 st.sidebar.subheader("Artist CRUD Operations")
#                 select_crud = st.sidebar.selectbox("CRUD", ["create","delete"])

#                 # Display all artists
#                 st.write("## All Artists")
#                 artists = get_all_artists(connection)
#                 # st.write(artists)
#                 st.dataframe(artists, width=700)

#                 # Add a new artist
#                 if select_crud == "create": 
#                     st.sidebar.subheader("Add New Artist:")
#                     artist_id = st.sidebar.number_input("Artist ID:", min_value=1)
#                     artist_name = st.sidebar.text_input("Artist Name:")
#                     genre_id = st.sidebar.number_input("Genre ID:", min_value=1)

#                     if st.sidebar.button("Add Artist", key="add_artist_button"):
#                         insert_artist(connection, artist_id, artist_name, genre_id)
#                 elif select_crud == 'delete':
#                     st.sidebar.subheader("Delete Artist:")
#                     delete_artist_id = st.sidebar.number_input("Artist ID to delete:", min_value=1)

#                     if st.sidebar.button("Delete Artist", key="delete_artist_button"):
#                         delete_artist(connection, delete_artist_id)        
        
#             elif selected_table == "concert":
#                 # Add concert CRUD operations
#                 st.sidebar.subheader("Concert CRUD Operations")

#                 # Display all concerts
#                 st.write("## All Concerts")
#                 concerts = get_all_concerts(connection)
#                 st.dataframe(concerts, width=700)

#                 # Add a new concert
#                 st.sidebar.subheader("Add New Concert:")
#                 concert_id = st.sidebar.number_input("Concert ID:", min_value=1)
#                 concert_name = st.sidebar.text_input("Concert Name:")
#                 artist_id = st.sidebar.number_input("Artist ID:", min_value=1)
#                 date = st.sidebar.date_input("Date:")
#                 venue_id = st.sidebar.number_input("Venue ID:", min_value=1)
#                 concert_group_id = st.sidebar.number_input("Concert Group ID:", min_value=1)
                
#                 if st.sidebar.button("Add Concert"):
#                     insert_concert(connection, concert_id, concert_name, artist_id, date, venue_id, concert_group_id)
            
#             elif selected_table == "concert_group":
#                 # Add concert_group CRUD operations
#                 st.sidebar.subheader("Concert Group CRUD Operations")

#                 # Display all concert groups
#                 st.write("## All Concert Groups")
#                 concert_groups = get_all_concert_groups(connection)
#                 st.dataframe(concert_groups, width=700)

#                 # Add a new concert group
#                 st.sidebar.subheader("Add New Concert Group:") 
#                 concert_group_id = st.sidebar.number_input("Concert Group ID:", min_value=1)
#                 concert_group_name = st.sidebar.text_input("Concert Group Name:")
                
#                 if st.sidebar.button("Add Concert Group"):
#                     insert_concert_group(connection, concert_group_id, concert_group_name)
                    
                    
#             elif selected_table == "customer":
#                 # Add customer CRUD operations
#                 st.sidebar.subheader("Customer CRUD Operations")

#                 # Display all customers
#                 st.write("## All Customers")
#                 customers = get_all_customers(connection)
#                 st.dataframe(customers, width=700)

#                 # Add a new customer
#                 st.sidebar.subheader("Add New Customer:")
#                 customer_id = st.sidebar.number_input("Customer ID:", min_value=1)
#                 customer_name = st.sidebar.text_input("Customer Name:")
#                 email = st.sidebar.text_input("Email:")
#                 user_name = st.sidebar.text_input("User Name:")
#                 password = st.sidebar.text_input("Password:", type="password")

#                 if st.sidebar.button("Add Customer"):
#                     insert_customer(connection, customer_id, customer_name, email, user_name, password)
                    
#             elif selected_table == "customer_order":
#                 # Add customer_order CRUD operations
#                 st.sidebar.subheader("Customer Order CRUD Operations")

#                 # Display all customer orders
#                 st.write("## All Customer Orders")
#                 customer_orders = get_all_customer_orders(connection)
#                 st.dataframe(customer_orders, width=700)

#                 # Add a new customer order
#                 st.sidebar.subheader("Add New Customer Order:")
#                 customer_order_id = st.sidebar.number_input("Customer Order ID:", min_value=1)
#                 customer_id = st.sidebar.number_input("Customer ID:", min_value=1)
#                 registered_email_address = st.sidebar.text_input("Registered Email Address:")
#                 total_price = st.sidebar.number_input("Total Price:", min_value=0.0)
#                 discount = st.sidebar.number_input("Discount:", min_value=0.0)
#                 final_price = st.sidebar.number_input("Final Price:", min_value=0.0)

#                 if st.sidebar.button("Add Customer Order"):
#                     insert_customer_order(connection, customer_order_id, customer_id, registered_email_address, total_price, discount, final_price)
                
#             elif selected_table == "genre":
#                 # Add genre CRUD operations
#                 st.sidebar.subheader("Genre CRUD Operations")

#                 # Display all genres
#                 st.write("## All Genres")
#                 genres = get_all_genres(connection)
#                 st.dataframe(genres, width=700)

#                 # Add a new genre
#                 st.sidebar.subheader("Add New Genre:")
#                 genre_id = st.sidebar.number_input("Genre ID:", min_value=1)
#                 genre_name = st.sidebar.text_input("Genre Name:")

#                 if st.sidebar.button("Add Genre"):
#                     insert_genre(connection, genre_id, genre_name)
                
#             elif selected_table == "order_ticket":
#                 # Add order_ticket CRUD operations
#                 st.sidebar.subheader("Order Ticket CRUD Operations")

#                 # Display all order tickets
#                 st.write("## All Order Tickets")
#                 order_tickets = get_all_order_tickets(connection)
#                 st.dataframe(order_tickets, width=700)

#                 # Add a new order ticket
#                 st.sidebar.subheader("Add New Order Ticket:")
#                 order_ticket_id = st.sidebar.number_input("Order Ticket ID:", min_value=1)
#                 customer_order_id = st.sidebar.number_input("Customer Order ID:", min_value=1)
#                 ticket_id = st.sidebar.number_input("Ticket ID:", min_value=1)

#                 if st.sidebar.button("Add Order Ticket"):
#                     insert_order_ticket(connection,order_ticket_id, customer_order_id, ticket_id)
                
#             elif selected_table == "ticket":
#                 # Add ticket CRUD operations
#                 st.sidebar.subheader("Ticket CRUD Operations")

#                 # Display all tickets
#                 st.write("## All Tickets")
#                 tickets = get_all_tickets(connection)
#                 st.dataframe(tickets, width=700)

#                 # Add a new ticket
#                 st.sidebar.subheader("Add New Ticket:")
#                 ticket_id = st.sidebar.number_input("Ticket ID:", min_value=1)
#                 serial_number = st.sidebar.text_input("Serial Number:")
#                 concert_id = st.sidebar.number_input("Concert ID:", min_value=1)
#                 ticket_category_id = st.sidebar.number_input("Ticket Category ID:", min_value=1)
#                 seat = st.sidebar.text_input("Seat:")
#                 purchase_date = st.sidebar.date_input("Purchase Date:")

#                 if st.sidebar.button("Add Ticket"):
#                     insert_ticket(connection,ticket_id, serial_number, concert_id, ticket_category_id, seat, purchase_date)

                

#             elif selected_table == "ticket_category":
#                 # Add ticket_category CRUD operations
#                 st.sidebar.subheader("Ticket Category CRUD Operations")

#                 # Display all ticket categories
#                 st.write("## All Ticket Categories")
#                 ticket_categories = get_all_ticket_categories(connection)
#                 st.dataframe(ticket_categories, width=700)

#                 # Add a new ticket category
#                 st.sidebar.subheader("Add New Ticket Category:")
#                 ticket_category_id = st.sidebar.number_input("Ticket Category ID:", min_value=1)
#                 description = st.sidebar.text_input("Description:")
#                 price = st.sidebar.number_input("Price:", min_value=0.0)
#                 start_date = st.sidebar.date_input("Start Date:")
#                 end_date = st.sidebar.date_input("End Date:")
#                 area = st.sidebar.text_input("Area:")
#                 concert_id_tc = st.sidebar.number_input("Concert ID:", min_value=1)

#                 if st.sidebar.button("Add Ticket Category"):
#                     insert_ticket_category(connection,ticket_category_id, description, price, start_date, end_date, area, concert_id_tc)

                
#             elif selected_table == "venue":
#                 # Add venue CRUD operations
#                 st.sidebar.subheader("Venue CRUD Operations")
#                 select_crud = st.sidebar.selectbox("CRUD", ["create","delete", "update"])

#                 # Display all venues
#                 st.write("## All Venues")
#                 venues = get_all_venues(connection)
#                 st.dataframe(venues, width=700)

#                 # Add a new venue
#                 if select_crud == "create":
#                     st.sidebar.subheader("Add New Venue:")
#                     venue_id = st.sidebar.number_input("Venue ID:", min_value=1)
#                     venue_name = st.sidebar.text_input("Venue Name:")
#                     location = st.sidebar.text_input("Location:")
#                     venue_type = st.sidebar.text_input("Venue Type:")
#                     capacity = st.sidebar.number_input("Capacity:", min_value=1)
                    
#                     if st.sidebar.button("Add Venue"):
#                         insert_venue(connection,venue_id, venue_name, location, venue_type, capacity)
                    
#                 elif select_crud == "delete":
#                     # Delete venue CRUD operation
#                     st.sidebar.subheader("Delete Venue Operation")

#                     # Delete a venue
#                     st.sidebar.subheader("Delete Venue:")
#                     venue_id_to_delete = st.sidebar.number_input("Venue ID to Delete:", min_value=1)
                    
#                     if st.sidebar.button("Delete Venue"):
#                         delete_venue(connection, venue_id_to_delete)        
#                 elif select_crud == "update":
#                     # Update venue CRUD operation
#                     st.sidebar.subheader("Update Venue Operation")

#                     # Update a venue
#                     st.sidebar.subheader("Update Venue:")
#                     venue_id_to_update = st.sidebar.number_input("Venue ID to Update:", min_value=1)
#                     new_venue_name = st.sidebar.text_input("New Venue Name:")
#                     new_location = st.sidebar.text_input("New Location:")
#                     new_type = st.sidebar.text_input("New Venue Type:")
#                     new_capacity = st.sidebar.number_input("New Capacity:", min_value=1)
                    
#                     if st.sidebar.button("Update Venue"):
#                         update_venue(connection, venue_id_to_update, new_venue_name, new_location, new_type, new_capacity)
                        
#                     # Close the database connection
#                     connection.close()
                
#             elif selected_table == "join tables":
#                 st.sidebar.subheader("Join Tables")
#                 selected_join = st.sidebar.selectbox("Join", ["artist_genre"])

#                 # Display the joined data
#                 st.write("## Joined Data from Artist and Genre Tables")
#                 joined_data = None
#                 if selected_join == "artist_genre":
#                     joined_data = join_artist_genre(connection)

#                 st.dataframe(joined_data, width=700)
#             connection.close()

# User Dashboard
def show_admin_dashboard():
    st.subheader("Admin Dashboard 🛠️")
    st.write("⚡ You have full access to manage concerts, users, and reports.")

    connection = create_connection()
    if not connection or not connection.is_connected():
        st.error("❌ Database connection failed.")
        return

    # Sidebar Navigation
    selected_table = st.sidebar.selectbox(
        "Manage Data", 
        ["Artist", "Concert", "Concert Group", "Customer", "Customer Order", "Genre", 
         "Order Ticket", "Ticket", "Ticket Category", "Venue"]
    )

    if selected_table == "Artist":
        manage_artist(connection)
    elif selected_table == "Concert":
        manage_concert(connection)
    elif selected_table == "Concert Group":
        manage_concert_group(connection)
    elif selected_table == "Customer":
        manage_customer(connection)
    elif selected_table == "Customer Order":
        manage_customer_order(connection)
    elif selected_table == "Genre":
        manage_genre(connection)
    elif selected_table == "Order Ticket":
        manage_order_ticket(connection)
    elif selected_table == "Ticket":
        manage_ticket(connection)
    elif selected_table == "Ticket Category":
        manage_ticket_category(connection)
    elif selected_table == "Venue":
        manage_venue(connection)

    connection.close()
    
    
# def user_dashboard():
#     st.subheader("User Dashboard 🎫")
#     st.write("🎵 You can browse and book concerts.")

#     connection = create_connection()  # Get MySQL connection once

#     if not connection or not connection.is_connected():
#         st.error("❌ MySQL Connection Failed. Please check your database settings.")
#         print("❌ DEBUG: Connection issue detected in user_dashboard()")
#         return  # Stop execution if no connection

#     print("✅ DEBUG: Connection successfully created in user_dashboard()")

#     # Sidebar options
#     selected_table = st.sidebar.selectbox("Select Table", ["artist", "concert", "concert_group", "customer", "customer_order", "genre", "order_ticket", "ticket", "ticket_category", "venue", "join tables"])

#     if selected_table == "artist":
#         st.subheader("🎨 All Artists")
#         artists = get_all_artists(connection)  # Pass connection
#         if artists:
#             st.dataframe(artists, width=700)
#         else:
#             st.warning("⚠️ No artists found.")

#         st.sidebar.subheader("Manage Artists")
#         action = st.sidebar.selectbox("Action", ["Add", "Update", "Delete"])

#         if action == "Add":
#             artist_id = st.sidebar.number_input("Artist ID", min_value=1)
#             artist_name = st.sidebar.text_input("Artist Name")
#             genre_id = st.sidebar.number_input("Genre ID", min_value=1)
#             if st.sidebar.button("Add Artist"):
#                 insert_artist(connection, artist_id, artist_name, genre_id)
#                 st.rerun()

#         elif action == "Update":
#             artist_id = st.sidebar.number_input("Artist ID to Update", min_value=1)
#             new_artist_name = st.sidebar.text_input("New Artist Name")
#             new_genre_id = st.sidebar.number_input("New Genre ID", min_value=1)
#             if st.sidebar.button("Update Artist"):
#                 update_artist(connection, artist_id, new_artist_name, new_genre_id)
#                 st.rerun()

#         elif action == "Delete":
#             artist_id = st.sidebar.number_input("Artist ID to Delete", min_value=1)
#             if st.sidebar.button("Delete Artist"):
#                 delete_artist(connection, artist_id)
#                 st.rerun()
    
def show_user_dashboard():
    """User Dashboard for managing tickets, bookings, and profile."""
    
    st.subheader("🎫 User Dashboard")
    st.write("🎵 Welcome! Browse concerts, book tickets, and manage your profile.")

    # Establish Database Connection
    connection = create_connection()
    if not connection or not connection.is_connected():
        st.error("❌ Database connection failed.")
        return

    # Sidebar Navigation
    selected_action = st.sidebar.selectbox(
        "Choose Action", ["Browse Concerts", "Book Ticket", "View My Tickets", "Cancel Booking", "My Profile"]
    )

    if selected_action == "Browse Concerts":
        browse_concerts(connection)
    elif selected_action == "Book Ticket":
        book_new_ticket(connection)
    elif selected_action == "View My Tickets":
        view_user_tickets(connection)
    elif selected_action == "Cancel Booking":
        cancel_user_ticket(connection)
    elif selected_action == "My Profile":
        manage_user_profile(connection)

    connection.close()


if __name__ == '__main__':
    main()
