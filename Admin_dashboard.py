import streamlit as st
from testing_app import *
from artist import *
from concert import *
from customers import *
from tickets import *
from Venue import *
from Genre import *

# def show_admin_dashboard():
#     st.subheader("Admin Dashboard 🛠️")
#     st.write("⚡ You have full access to manage concerts, users, and reports.")

#     connection = create_connection()
#     if not connection or not connection.is_connected():
#         st.error("❌ Database connection failed.")
#         return

#     # Sidebar Navigation
#     selected_table = st.sidebar.selectbox(
#         "Manage Data", 
#         ["Artist", "Concert", "Concert Group", "Customer", "Customer Order", "Genre", 
#          "Order Ticket", "Ticket", "Ticket Category", "Venue"]
#     )

#     if selected_table == "Artist":
#         manage_artist(connection)
#     elif selected_table == "Concert":
#         manage_concert(connection)
#     elif selected_table == "Concert Group":
#         manage_concert_group(connection)
#     elif selected_table == "Customer":
#         manage_customer(connection)
#     elif selected_table == "Customer Order":
#         manage_customer_order(connection)
#     elif selected_table == "Genre":
#         manage_genre(connection)
#     elif selected_table == "Order Ticket":
#         manage_order_ticket(connection)
#     elif selected_table == "Ticket":
#         manage_ticket(connection)
#     elif selected_table == "Ticket Category":
#         manage_ticket_category(connection)
#     elif selected_table == "Venue":
#         manage_venue(connection)

#     connection.close()

# 🎨 Manage Artists
def manage_artist(connection):
    st.sidebar.subheader("Artist Management")
    st.write("## All Artists")
    artists = get_all_artists(connection)
    st.dataframe(artists, width=700)

    action = st.sidebar.radio("Action", ["Add", "Delete"])
    
    if action == "Add":
        artist_id = st.sidebar.number_input("Artist ID:", min_value=1)
        artist_name = st.sidebar.text_input("Artist Name:")
        genre_id = st.sidebar.number_input("Genre ID:", min_value=1)
        if st.sidebar.button("Add Artist"):
            insert_artist(connection, artist_id, artist_name, genre_id)
            st.success(f"🎨 Artist '{artist_name}' added successfully!")
            st.rerun()
    
    elif action == "Delete":
        delete_artist_id = st.sidebar.number_input("Artist ID to delete:", min_value=1)
        if st.sidebar.button("Delete Artist"):
            delete_artist(connection, delete_artist_id)
            st.success(f"🗑️ Artist with ID {delete_artist_id} deleted successfully!")
            st.rerun()

# 🎵 Manage Concerts
def manage_concert(connection):
    st.sidebar.subheader("Concert Management")
    st.write("## All Concerts")
    concerts = get_all_concerts(connection)
    st.dataframe(concerts, width=700)

    st.sidebar.subheader("Add New Concert")
    concert_id = st.sidebar.number_input("Concert ID:", min_value=1)
    concert_name = st.sidebar.text_input("Concert Name:")
    artist_id = st.sidebar.number_input("Artist ID:", min_value=1)
    date = st.sidebar.date_input("Date:")
    venue_id = st.sidebar.number_input("Venue ID:", min_value=1)
    concert_group_id = st.sidebar.number_input("Concert Group ID:", min_value=1)

    if st.sidebar.button("Add Concert"):
        insert_concert(connection, concert_id, concert_name, artist_id, date, venue_id, concert_group_id)
        st.success(f"🎤 Concert '{concert_name}' added successfully!")
        st.rerun()

# 🎭 Manage Concert Groups
def manage_concert_group(connection):
    st.sidebar.subheader("Concert Group Management")
    st.write("## All Concert Groups")
    groups = get_all_concert_groups(connection)
    st.dataframe(groups, width=700)

    st.sidebar.subheader("Add New Concert Group")
    concert_group_id = st.sidebar.number_input("Concert Group ID:", min_value=1)
    concert_group_name = st.sidebar.text_input("Concert Group Name:")
    
    if st.sidebar.button("Add Concert Group"):
        insert_concert_group(connection, concert_group_id, concert_group_name)
        st.success(f"🎭 Concert Group '{concert_group_name}' added successfully!")
        st.rerun()

# 👥 Manage Customers
def manage_customer(connection):
    st.sidebar.subheader("Customer Management")
    st.write("## All Customers")
    customers = get_all_customers(connection)
    st.dataframe(customers, width=700)

    st.sidebar.subheader("Add New Customer")
    customer_id = st.sidebar.number_input("Customer ID:", min_value=1)
    customer_name = st.sidebar.text_input("Customer Name:")
    email = st.sidebar.text_input("Email:")
    user_name = st.sidebar.text_input("Username:")
    password = st.sidebar.text_input("Password:", type="password")

    if st.sidebar.button("Add Customer"):
        insert_customer(connection, customer_id, customer_name, email, user_name, password)
        st.success(f"👤 Customer '{customer_name}' added successfully!")
        st.rerun()

# 🏟️ Manage Venues
def manage_venue(connection):
    st.sidebar.subheader("Venue Management")
    st.write("## All Venues")
    venues = get_all_venues(connection)
    st.dataframe(venues, width=700)

    st.sidebar.subheader("Add New Venue")
    venue_id = st.sidebar.number_input("Venue ID:", min_value=1)
    venue_name = st.sidebar.text_input("Venue Name:")
    location = st.sidebar.text_input("Location:")

    if st.sidebar.button("Add Venue"):
        insert_venue(connection, venue_id, venue_name, location)
        st.success(f"🏟️ Venue '{venue_name}' added successfully!")
        st.rerun()

# 🛒 Manage Customer Orders
def manage_customer_order(connection):
    st.sidebar.subheader("Customer Order Management")
    st.write("## All Customer Orders")
    orders = get_all_customer_orders(connection)
    st.dataframe(orders, width=700)

    st.sidebar.subheader("Add New Customer Order")
    order_id = st.sidebar.number_input("Order ID:", min_value=1)
    customer_id = st.sidebar.number_input("Customer ID:", min_value=1)
    email = st.sidebar.text_input("Registered Email Address:")
    total_price = st.sidebar.number_input("Total Price:", min_value=0.0)
    discount = st.sidebar.number_input("Discount:", min_value=0.0)
    final_price = st.sidebar.number_input("Final Price:", min_value=0.0)

    if st.sidebar.button("Add Order"):
        insert_customer_order(connection, order_id, customer_id, email, total_price, discount, final_price)
        st.success(f"🛍️ Order {order_id} added successfully!")
        st.rerun()

# 🎭 Manage Genres
def manage_genre(connection):
    st.sidebar.subheader("Genre Management")
    st.write("## All Genres")
    genres = get_all_genres(connection)
    st.dataframe(genres, width=700)

    st.sidebar.subheader("Add New Genre")
    genre_id = st.sidebar.number_input("Genre ID:", min_value=1)
    genre_name = st.sidebar.text_input("Genre Name:")

    if st.sidebar.button("Add Genre"):
        insert_genre(connection, genre_id, genre_name)
        st.success(f"🎭 Genre '{genre_name}' added successfully!")
        st.rerun()

# 🎟️ Manage Order Tickets
def manage_order_ticket(connection):
    st.sidebar.subheader("Order Ticket Management")
    st.write("## All Order Tickets")
    order_tickets = get_all_order_tickets(connection)
    st.dataframe(order_tickets, width=700)

    st.sidebar.subheader("Add New Order Ticket")
    order_ticket_id = st.sidebar.number_input("Order Ticket ID:", min_value=1)
    customer_order_id = st.sidebar.number_input("Customer Order ID:", min_value=1)
    ticket_id = st.sidebar.number_input("Ticket ID:", min_value=1)

    if st.sidebar.button("Add Order Ticket"):
        insert_order_ticket(connection, order_ticket_id, customer_order_id, ticket_id)
        st.success(f"🎫 Order Ticket {order_ticket_id} added successfully!")
        st.rerun()

# 🎟️ Manage Tickets
def manage_ticket(connection):
    st.sidebar.subheader("Ticket Management")
    st.write("## All Tickets")
    tickets = get_all_tickets(connection)
    st.dataframe(tickets, width=700)

    st.sidebar.subheader("Add New Ticket")
    ticket_id = st.sidebar.number_input("Ticket ID:", min_value=1)
    serial_number = st.sidebar.text_input("Serial Number:")
    concert_id = st.sidebar.number_input("Concert ID:", min_value=1)
    ticket_category_id = st.sidebar.number_input("Ticket Category ID:", min_value=1)
    seat = st.sidebar.text_input("Seat:")
    purchase_date = st.sidebar.date_input("Purchase Date:")

    if st.sidebar.button("Add Ticket"):
        insert_ticket(connection, ticket_id, serial_number, concert_id, ticket_category_id, seat, purchase_date)
        st.success(f"🎟️ Ticket {ticket_id} added successfully!")
        st.rerun()

# 🎫 Manage Ticket Categories
def manage_ticket_category(connection):
    st.sidebar.subheader("Ticket Category Management")
    st.write("## All Ticket Categories")
    categories = get_all_ticket_categories(connection)
    st.dataframe(categories, width=700)

    st.sidebar.subheader("Add New Ticket Category")
    ticket_category_id = st.sidebar.number_input("Category ID:", min_value=1)
    description = st.sidebar.text_input("Description:")
    price = st.sidebar.number_input("Price:", min_value=0.0)
    start_date = st.sidebar.date_input("Start Date:")
    end_date = st.sidebar.date_input("End Date:")
    area = st.sidebar.text_input("Area:")
    concert_id_tc = st.sidebar.number_input("Concert ID:", min_value=1)

    if st.sidebar.button("Add Ticket Category"):
        insert_ticket_category(connection, ticket_category_id, description, price, start_date, end_date, area, concert_id_tc)
        st.success(f"🎟️ Ticket Category {ticket_category_id} added successfully!")
        st.rerun()