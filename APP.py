import streamlit as st
import mysql.connector
from mysql.connector import Error
import bcrypt
import jwt
import datetime
from testing_security import *
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

# Function to create a MySQL connection
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv("host"),
            user=os.getenv("user"),
            password= os.getenv("password"),
            database=os.getenv("database"),
            autocommit=True  # all the changes are saved instantly
        )
        if connection.is_connected():
            st.success("Connected to MySQL database")
    except Error as e:
        st.error(f"Database Connection Error: {e}")
    return connection

# Function to execute MySQL queries and return results as a Pandas DataFrame
def execute_query(connection, query, params=None, fetch_one=False):
    try:
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        
        if query.strip().lower().startswith("select"):
            result = cursor.fetchone() if fetch_one else cursor.fetchall()
            cursor.close()  # Close the cursor after fetching results
            return result
        
        connection.commit()
        cursor.close()
        return None

    except Error as e:
        st.error(f"Database Error: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close() # Close the connection adfter query execution


# Function to get all data from the "artist" table
def get_all_artists(connection):
    query = "SELECT * FROM artist"
    return execute_query(connection, query)

# Function to insert data into the "artist" table
def insert_artist(connection,artist_id, artist_name, genre_id):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO artist (artist_id, artist_name, genre_id) VALUES (%s, %s, %s)"
        cursor.execute(query, (artist_id, artist_name, genre_id))
        #connection.commit()
        st.success("Artist added successfully!")
    except Error as e:
        st.error(f"Error: {e}")
def delete_artist(connection, artist_id):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM artist WHERE artist_id = %s"
        cursor.execute(query, (artist_id, ))
        #connection.commit()
        st.success(f"Artist with ID {artist_id} deleted successfully!")
    except Error as e:
        st.error(f"Error: {e}")
def update_artist(connection, artist_id, new_artist_name, new_genre_id):
    try:
        cursor = connection.cursor()
        query = "UPDATE artist SET artist_name = %s, genre_id = %s WHERE artist_id = %s"
        cursor.execute(query, (artist_id, new_artist_name, new_genre_id))
        #connection.commit()
        st.success("Artist updated successfully!")
    except Error as e:
        st.error(f"Error: {e}")

# Function to get all data from the "concert" table
def get_all_concerts(connection):
    query = "SELECT * FROM concert"
    return execute_query(connection, query)

# Function to insert data into the "concert" table
def insert_concert(connection,concert_id, concert_name, artist_id, date, venue_id, concert_group_id):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO concert (concert_id, concert_name, artist_id, date, venue_id, concert_group_id) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (concert_id, concert_name, artist_id, date, venue_id, concert_group_id))
        #connection.commit()
        st.success("Concert added successfully!")
    except Error as e:
        st.error(f"Error: {e}")
def delete_concert(connection, concert_id):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM concert WHERE concert_id = %s"
        cursor.execute(query, (concert_id, ))
        #connection.commit()
        st.success(f"Concert with ID {concert_id} deleted successfully!")
    except Error as e:
        st.error(f"Error: {e}")
def update_concert(connection, concert_id, new_concert_name, new_artist_id, new_date, new_venue_id, new_concert_group_id):
    try:
        cursor = connection.cursor()
        query = f"UPDATE concert SET concert_name = %s, artist_id = %s, date = %s, venue_id = %s, concert_group_id = %s WHERE concert_id = %s"
        cursor.execute(query, (concert_id, new_concert_name, new_artist_id, new_date, new_venue_id, new_concert_group_id))
        #connection.commit()
        st.success("Concert updated successfully!")
    except Error as e:
        st.error(f"Error: {e}")

# Function to get all data from the "concert_group" table
def get_all_concert_groups(connection):
    query = "SELECT * FROM concert_group"
    return execute_query(connection, query)

# Function to insert data into the "concert_group" table
def insert_concert_group(connection, concert_group_id, concert_group_name):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO concert_group (concert_group_id, concert_group_name) VALUES (%s, %s)"
        cursor.execute(query, (concert_group_id, concert_group_name))
        #connection.commit()
        st.success("Concert group added successfully!")
    except Error as e:
        st.error(f"Error: {e}")
def delete_concert_group(connection, concert_group_id):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM concert_group WHERE concert_group_id = %s"
        cursor.execute(query, (concert_group_id, ))
        #connection.commit()
        st.success(f"Concert Group with ID {concert_group_id} deleted successfully!")
    except Error as e:
        st.error(f"Error: {e}")
def update_concert_group(connection, concert_group_id, new_concert_group_name):
    try:
        cursor = connection.cursor()
        query = "UPDATE concert_group SET concert_group_name = %s WHERE concert_group_id = %s"
        cursor.execute(query, (concert_group_id, new_concert_group_name))
        #connection.commit()
        st.success("Concert Group updated successfully!")
    except Error as e:
        st.error(f"Error: {e}")

# Function to get all data from the "customer" table
def get_all_customers(connection):
    query = "SELECT * FROM customer"
    return execute_query(connection, query)

# Function to insert data into the "customer" table
def insert_customer(connection,customer_id, customer_name, email, user_name, password):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO customer (customer_id, customer_name, email, user_name, password) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (customer_id, customer_name, email, user_name, password))
        #connection.commit()
        st.success("Customer added successfully!")
    except Error as e:
        st.error(f"Error: {e}")
def delete_customer(connection, customer_id):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM customer WHERE customer_id = %s"
        cursor.execute(query, (customer_id, ))
        #connection.commit()
        st.success(f"Customer with ID {customer_id} deleted successfully!")
    except Error as e:
        st.error(f"Error: {e}")
def update_customer(connection, customer_id, new_customer_name, new_email, new_user_name, new_password):
    try:
        cursor = connection.cursor()
        query = "UPDATE customer SET customer_name = %s, email = %s, user_name = %s, password = %s WHERE customer_id = %s"
        cursor.execute(query, (customer_id, new_customer_name, new_email, new_user_name, new_password))
        #connection.commit()
        st.success("Customer updated successfully!")
    except Error as e:
        st.error(f"Error: {e}")

# Function to get all data from the "customer_order" table
def get_all_customer_orders(connection):
    query = "SELECT * FROM customer_order"
    return execute_query(connection, query)

#Function to join two tables
def join_tables(connection, table1, table2, join_condition, columns):
    columns_str = ', '.join(columns)
    query = f"""
    SELECT {columns_str}
    FROM {table1} t1
    INNER JOIN {table2} t2 ON {join_condition}
    """
    return execute_query(connection, query)

# Function to insert data into the "customer_order" table
def insert_customer_order(connection,customer_order_id, customer_id, registered_email_address, total_price, discount, final_price):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO customer_order (customer_order_id, customer_id, registered_email_address, total_price, discount, final_price) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (customer_order_id, customer_id, registered_email_address, total_price, discount, final_price))
        #connection.commit()
        st.success("Customer order added successfully!")
    except Error as e:
        st.error(f"Error: {e}")
def delete_customer_order(connection, customer_order_id):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM customer_order WHERE customer_order_id = %s"
        cursor.execute(query, (customer_order_id))
        #connection.commit()
        st.success(f"Customer Order with ID {customer_order_id} deleted successfully!")
    except Error as e:
        st.error(f"Error: {e}")
def update_customer_order(connection, customer_order_id, new_customer_id, new_registered_email_address, new_total_price, new_discount, new_final_price):
    try:
        cursor = connection.cursor()
        query = "UPDATE customer_order SET customer_id = %s, registered_email_address = %s, total_price = %s, discount = %s, final_price = %s WHERE customer_order_id = %s"
        cursor.execute(query, ( customer_order_id, new_customer_id, new_registered_email_address, new_total_price, new_discount, new_final_price))
        #connection.commit()
        st.success("Customer Order updated successfully!")
    except Error as e:
        st.error(f"Error: {e}")

# Function to get all data from the "genre" table
def get_all_genres(connection):
    query = "SELECT * FROM genre"
    return execute_query(connection, query)

# Function to insert data into the "genre" table
def insert_genre(connection,genre_id, genre_name):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO genre (genre_name) VALUES (%s, %s)"
        cursor.execute(query,(genre_id, genre_name))
        #connection.commit()
        st.success("Genre added successfully!")
    except Error as e:
        st.error(f"Error: {e}")
def delete_genre(connection, genre_id):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM genre WHERE genre_id = %s"
        cursor.execute(query, (genre_id, ))
        #connection.commit()
        st.success(f"Genre with ID {genre_id} deleted successfully!")
    except Error as e:
        st.error(f"Error: {e}")
def update_genre(connection, genre_id, new_genre_name):
    try:
        cursor = connection.cursor()
        query = "UPDATE genre SET genre_name = %s WHERE genre_id = %s"
        cursor.execute(query, (genre_id, new_genre_name))
        #connection.commit()
        st.success("Genre updated successfully!")
    except Error as e:
        st.error(f"Error: {e}")

# Function to get all data from the "order_ticket" table
def get_all_order_tickets(connection):
    query = "SELECT * FROM order_ticket"
    return execute_query(connection, query)

# Function to insert data into the "order_ticket" table
def insert_order_ticket(connection, order_ticket_id, customer_order_id, ticket_id):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO order_ticket (order_ticket_id, customer_order_id, ticket_id) VALUES (%s,%s, %s)"
        cursor.execute(query, (order_ticket_id, customer_order_id, ticket_id))
        #connection.commit()
        st.success("Order ticket added successfully!")
    except Error as e:
        st.error(f"Error: {e}")
def delete_order_ticket(connection, order_ticket_id):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM order_ticket WHERE order_ticket_id = %s"
        cursor.execute(query, order_ticket_id, )
        #connection.commit()
        st.success(f"Order Ticket with ID {order_ticket_id} deleted successfully!")
    except Error as e:
        st.error(f"Error: {e}")
def update_order_ticket(connection, order_ticket_id, new_customer_order_id, new_ticket_id):
    try:
        cursor = connection.cursor()
        query = "UPDATE order_ticket SET customer_order_id = %s, ticket_id = %s WHERE order_ticket_id = %s"
        cursor.execute(query, (order_ticket_id, new_customer_order_id, new_ticket_id))
        #connection.commit()
        st.success("Order Ticket updated successfully!")
    except Error as e:
        st.error(f"Error: {e}")

# Function to get all data from the "ticket" table
def get_all_tickets(connection):
    query = "SELECT * FROM ticket"
    return execute_query(connection, query)

# Function to insert data into the "ticket" table
def insert_ticket(connection, ticket_id, serial_number, concert_id, ticket_category_id, seat, purchase_date):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO ticket (ticket_id, serial_number, concert_id, ticket_category_id, seat, purchase_date) VALUES (%s, %s, %s, $s, %s, %s)"
        cursor.execute(query, (ticket_id, serial_number, concert_id, ticket_category_id, seat, purchase_date))
        #connection.commit()
        st.success("Ticket added successfully!")
    except Error as e:
        st.error(f"Error: {e}")
def delete_ticket(connection, ticket_id):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM ticket WHERE ticket_id = %s"
        cursor.execute(query, (ticket_id, ))
        #connection.commit()
        st.success(f"Ticket with ID {ticket_id} deleted successfully!")
    except Error as e:
        st.error(f"Error: {e}")
def update_ticket(connection, ticket_id, new_serial_number, new_concert_id, new_ticket_category_id, new_seat, new_purchase_date):
    try:
        cursor = connection.cursor()
        query = f"UPDATE ticket SET serial_number = %s, concert_id = %s, ticket_category_id = %s, seat = %s, purchase_date = %s WHERE ticket_id = %s"
        cursor.execute(query, (ticket_id, new_serial_number, new_concert_id, new_ticket_category_id, new_seat, new_purchase_date))
        #connection.commit()
        st.success("Ticket updated successfully!")
    except Error as e:
        st.error(f"Error: {e}")

# Function to get all data from the "ticket_category" table
def get_all_ticket_categories(connection):
    query = "SELECT * FROM ticket_category"
    return execute_query(connection, query)

# Function to insert data into the "ticket_category" table
def insert_ticket_category(connection,ticket_category_id, description, price, start_date, end_date, area, concert_id):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO ticket_category (ticket_category_id, description, price, start_date, end_date, area, concert_id) VALUES (%s,%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (ticket_category_id, description, price, start_date, end_date, area, concert_id))
        #connection.commit()
        st.success("Ticket category added successfully!")
    except Error as e:
        st.error(f"Error: {e}")
def delete_ticket_category(connection, ticket_category_id):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM ticket_category WHERE ticket_category_id = %s"
        cursor.execute(query, (ticket_category_id, ))
        #connection.commit()
        st.success(f"Ticket Category with ID {ticket_category_id} deleted successfully!")
    except Error as e:
        st.error(f"Error: {e}")
def update_ticket_category(connection, ticket_category_id, new_description, new_price, new_start_date, new_end_date, new_area, new_concert_id):
    try:
        cursor = connection.cursor()
        query = "UPDATE ticket_category SET description = %s, price = %s, start_date = %s, end_date = %s, area = %s, concert_id = %s WHERE ticket_category_id = %s"
        cursor.execute(query, (ticket_category_id, new_description, new_price, new_start_date, new_end_date, new_area, new_concert_id))
        #connection.commit()
        st.success("Ticket Category updated successfully!")
    except Error as e:
        st.error(f"Error: {e}")

# Function to get all data from the "venue" table
def get_all_venues(connection):
    query = "SELECT * FROM venue"
    return execute_query(connection, query)

# Function to insert data into the "venue" table
def insert_venue(connection,venue_id, venue_name, location, type, capacity):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO venue (venue_id, venue_name, location, type, capacity) VALUES (%s,%s, %s, %s, %s)"
        cursor.execute(query, (venue_id, venue_name, location, type, capacity))
        #connection.commit()
        st.success("Venue added successfully!")
    except Error as e:
        st.error(f"Error: {e}")
def delete_venue(connection, venue_id):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM venue WHERE venue_id = %s"
        cursor.execute(query, (venue_id, ))
        #connection.commit()
        st.success("Venue deleted successfully!")
    except Error as e:
        st.error(f"Error: {e}")
def update_venue(connection, venue_id, new_venue_name, new_location, new_type, new_capacity):
    try:
        cursor = connection.cursor()
        query = "UPDATE venue SET venue_name = %s, location = %s, type = %s, capacity = %s WHERE venue_id = %s"
        cursor.execute(query, (venue_id, new_venue_name, new_location, new_type, new_capacity))
        #connection.commit()
        st.success("Venue updated successfully!")
    except Error as e:
        st.error(f"Error: {e}")
        
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
def show_admin_dashboard():
    st.subheader("Admin Dashboard 🛠️")
    st.write("⚡ You have full access to manage concerts, users, and reports.")
    # st.sidebar.subheader("Admin Actions")
    # st.sidebar.button("Manage Users")
    # st.sidebar.button("View Reports")
    connection = create_connection()

    if connection:
            col1, col2 = st.columns([1, 3])
            # col1.image("concert_logo.png", width=100)
            col2.title("Concert Management Web App")
            # Sidebar for selecting a table
            selected_table = st.sidebar.selectbox("Concert", ["artist", "concert", "concert_group", "customer", "customer_order", "genre", "order_ticket", "ticket", "ticket_category", "venue", "join tables"])

            if selected_table == "artist":
                # Add artist CRUD operations
                st.sidebar.subheader("Artist CRUD Operations")
                select_crud = st.sidebar.selectbox("CRUD", ["create","delete"])

                # Display all artists
                st.write("## All Artists")
                artists = get_all_artists(connection)
                # st.write(artists)
                st.dataframe(artists, width=700)

                # Add a new artist
                if select_crud == "create": 
                    st.sidebar.subheader("Add New Artist:")
                    artist_id = st.sidebar.number_input("Artist ID:", min_value=1)
                    artist_name = st.sidebar.text_input("Artist Name:")
                    genre_id = st.sidebar.number_input("Genre ID:", min_value=1)

                    if st.sidebar.button("Add Artist", key="add_artist_button"):
                        insert_artist(connection, artist_id, artist_name, genre_id)
                elif select_crud == 'delete':
                    st.sidebar.subheader("Delete Artist:")
                    delete_artist_id = st.sidebar.number_input("Artist ID to delete:", min_value=1)

                    if st.sidebar.button("Delete Artist", key="delete_artist_button"):
                        delete_artist(connection, delete_artist_id)        
        
            elif selected_table == "concert":
                # Add concert CRUD operations
                st.sidebar.subheader("Concert CRUD Operations")

                # Display all concerts
                st.write("## All Concerts")
                concerts = get_all_concerts(connection)
                st.dataframe(concerts, width=700)

                # Add a new concert
                st.sidebar.subheader("Add New Concert:")
                concert_id = st.sidebar.number_input("Concert ID:", min_value=1)
                concert_name = st.sidebar.text_input("Concert Name:")
                artist_id = st.sidebar.number_input("Artist ID:", min_value=1)
                date = st.sidebar.date_input("Date:")
                venue_id = st.sidebar.number_input("Venue ID:", min_value=1)
                concert_group_id = st.sidebar.number_input("Concert Group ID:", min_value=1)
                
                if st.sidebar.button("Add Concert"):
                    insert_concert(connection, concert_id, concert_name, artist_id, date, venue_id, concert_group_id)
            
            elif selected_table == "concert_group":
                # Add concert_group CRUD operations
                st.sidebar.subheader("Concert Group CRUD Operations")

                # Display all concert groups
                st.write("## All Concert Groups")
                concert_groups = get_all_concert_groups(connection)
                st.dataframe(concert_groups, width=700)

                # Add a new concert group
                st.sidebar.subheader("Add New Concert Group:") 
                concert_group_id = st.sidebar.number_input("Concert Group ID:", min_value=1)
                concert_group_name = st.sidebar.text_input("Concert Group Name:")
                
                if st.sidebar.button("Add Concert Group"):
                    insert_concert_group(connection, concert_group_id, concert_group_name)
                    
                    
            elif selected_table == "customer":
                # Add customer CRUD operations
                st.sidebar.subheader("Customer CRUD Operations")

                # Display all customers
                st.write("## All Customers")
                customers = get_all_customers(connection)
                st.dataframe(customers, width=700)

                # Add a new customer
                st.sidebar.subheader("Add New Customer:")
                customer_id = st.sidebar.number_input("Customer ID:", min_value=1)
                customer_name = st.sidebar.text_input("Customer Name:")
                email = st.sidebar.text_input("Email:")
                user_name = st.sidebar.text_input("User Name:")
                password = st.sidebar.text_input("Password:", type="password")

                if st.sidebar.button("Add Customer"):
                    insert_customer(connection, customer_id, customer_name, email, user_name, password)
                    
            elif selected_table == "customer_order":
                # Add customer_order CRUD operations
                st.sidebar.subheader("Customer Order CRUD Operations")

                # Display all customer orders
                st.write("## All Customer Orders")
                customer_orders = get_all_customer_orders(connection)
                st.dataframe(customer_orders, width=700)

                # Add a new customer order
                st.sidebar.subheader("Add New Customer Order:")
                customer_order_id = st.sidebar.number_input("Customer Order ID:", min_value=1)
                customer_id = st.sidebar.number_input("Customer ID:", min_value=1)
                registered_email_address = st.sidebar.text_input("Registered Email Address:")
                total_price = st.sidebar.number_input("Total Price:", min_value=0.0)
                discount = st.sidebar.number_input("Discount:", min_value=0.0)
                final_price = st.sidebar.number_input("Final Price:", min_value=0.0)

                if st.sidebar.button("Add Customer Order"):
                    insert_customer_order(connection, customer_order_id, customer_id, registered_email_address, total_price, discount, final_price)
                
            elif selected_table == "genre":
                # Add genre CRUD operations
                st.sidebar.subheader("Genre CRUD Operations")

                # Display all genres
                st.write("## All Genres")
                genres = get_all_genres(connection)
                st.dataframe(genres, width=700)

                # Add a new genre
                st.sidebar.subheader("Add New Genre:")
                genre_id = st.sidebar.number_input("Genre ID:", min_value=1)
                genre_name = st.sidebar.text_input("Genre Name:")

                if st.sidebar.button("Add Genre"):
                    insert_genre(connection, genre_id, genre_name)
                
            elif selected_table == "order_ticket":
                # Add order_ticket CRUD operations
                st.sidebar.subheader("Order Ticket CRUD Operations")

                # Display all order tickets
                st.write("## All Order Tickets")
                order_tickets = get_all_order_tickets(connection)
                st.dataframe(order_tickets, width=700)

                # Add a new order ticket
                st.sidebar.subheader("Add New Order Ticket:")
                order_ticket_id = st.sidebar.number_input("Order Ticket ID:", min_value=1)
                customer_order_id = st.sidebar.number_input("Customer Order ID:", min_value=1)
                ticket_id = st.sidebar.number_input("Ticket ID:", min_value=1)

                if st.sidebar.button("Add Order Ticket"):
                    insert_order_ticket(connection,order_ticket_id, customer_order_id, ticket_id)
                
            elif selected_table == "ticket":
                # Add ticket CRUD operations
                st.sidebar.subheader("Ticket CRUD Operations")

                # Display all tickets
                st.write("## All Tickets")
                tickets = get_all_tickets(connection)
                st.dataframe(tickets, width=700)

                # Add a new ticket
                st.sidebar.subheader("Add New Ticket:")
                ticket_id = st.sidebar.number_input("Ticket ID:", min_value=1)
                serial_number = st.sidebar.text_input("Serial Number:")
                concert_id = st.sidebar.number_input("Concert ID:", min_value=1)
                ticket_category_id = st.sidebar.number_input("Ticket Category ID:", min_value=1)
                seat = st.sidebar.text_input("Seat:")
                purchase_date = st.sidebar.date_input("Purchase Date:")

                if st.sidebar.button("Add Ticket"):
                    insert_ticket(connection,ticket_id, serial_number, concert_id, ticket_category_id, seat, purchase_date)

                

            elif selected_table == "ticket_category":
                # Add ticket_category CRUD operations
                st.sidebar.subheader("Ticket Category CRUD Operations")

                # Display all ticket categories
                st.write("## All Ticket Categories")
                ticket_categories = get_all_ticket_categories(connection)
                st.dataframe(ticket_categories, width=700)

                # Add a new ticket category
                st.sidebar.subheader("Add New Ticket Category:")
                ticket_category_id = st.sidebar.number_input("Ticket Category ID:", min_value=1)
                description = st.sidebar.text_input("Description:")
                price = st.sidebar.number_input("Price:", min_value=0.0)
                start_date = st.sidebar.date_input("Start Date:")
                end_date = st.sidebar.date_input("End Date:")
                area = st.sidebar.text_input("Area:")
                concert_id_tc = st.sidebar.number_input("Concert ID:", min_value=1)

                if st.sidebar.button("Add Ticket Category"):
                    insert_ticket_category(connection,ticket_category_id, description, price, start_date, end_date, area, concert_id_tc)

                
            elif selected_table == "venue":
                # Add venue CRUD operations
                st.sidebar.subheader("Venue CRUD Operations")
                select_crud = st.sidebar.selectbox("CRUD", ["create","delete", "update"])

                # Display all venues
                st.write("## All Venues")
                venues = get_all_venues(connection)
                st.dataframe(venues, width=700)

                # Add a new venue
                if select_crud == "create":
                    st.sidebar.subheader("Add New Venue:")
                    venue_id = st.sidebar.number_input("Venue ID:", min_value=1)
                    venue_name = st.sidebar.text_input("Venue Name:")
                    location = st.sidebar.text_input("Location:")
                    venue_type = st.sidebar.text_input("Venue Type:")
                    capacity = st.sidebar.number_input("Capacity:", min_value=1)
                    
                    if st.sidebar.button("Add Venue"):
                        insert_venue(connection,venue_id, venue_name, location, venue_type, capacity)
                    
                elif select_crud == "delete":
                    # Delete venue CRUD operation
                    st.sidebar.subheader("Delete Venue Operation")

                    # Delete a venue
                    st.sidebar.subheader("Delete Venue:")
                    venue_id_to_delete = st.sidebar.number_input("Venue ID to Delete:", min_value=1)
                    
                    if st.sidebar.button("Delete Venue"):
                        delete_venue(connection, venue_id_to_delete)        
                elif select_crud == "update":
                    # Update venue CRUD operation
                    st.sidebar.subheader("Update Venue Operation")

                    # Update a venue
                    st.sidebar.subheader("Update Venue:")
                    venue_id_to_update = st.sidebar.number_input("Venue ID to Update:", min_value=1)
                    new_venue_name = st.sidebar.text_input("New Venue Name:")
                    new_location = st.sidebar.text_input("New Location:")
                    new_type = st.sidebar.text_input("New Venue Type:")
                    new_capacity = st.sidebar.number_input("New Capacity:", min_value=1)
                    
                    if st.sidebar.button("Update Venue"):
                        update_venue(connection, venue_id_to_update, new_venue_name, new_location, new_type, new_capacity)
                        
                    # Close the database connection
                    connection.close()
                
            elif selected_table == "join tables":
                st.sidebar.subheader("Join Tables")
                selected_join = st.sidebar.selectbox("Join", ["artist_genre"])

                # Display the joined data
                st.write("## Joined Data from Artist and Genre Tables")
                joined_data = None
                if selected_join == "artist_genre":
                    joined_data = join_artist_genre(connection)

                st.dataframe(joined_data, width=700)
            connection.close()

# User Dashboard
def show_user_dashboard():
    st.subheader("User Dashboard 🎫")
    st.write("🎵 You can browse and book concerts.")
    # st.sidebar.subheader("User Actions")
    # st.sidebar.button("Browse Concerts")
    # st.sidebar.button("My Bookings")
    connection = create_connection()

    if connection:
            col1, col2 = st.columns([1, 3])
            # col1.image("concert_logo.png", width=100)
            col2.title("Concert Management Web App")
            # Sidebar for selecting a table
            selected_table = st.sidebar.selectbox("Concert", ["artist", "concert", "concert_group", "customer", "customer_order", "genre", "order_ticket", "ticket", "ticket_category", "venue", "join tables"])

            if selected_table == "artist":
                # Add artist CRUD operations
                st.sidebar.subheader("Artist CRUD Operations")
                select_crud = st.sidebar.selectbox("CRUD", ["create","delete"])

                # Display all artists
                st.write("## All Artists")
                artists = get_all_artists(connection)
                # st.write(artists)
                st.dataframe(artists, width=700)

        
            elif selected_table == "concert":
                # Add concert CRUD operations
                st.sidebar.subheader("Concert CRUD Operations")

                # Display all concerts
                st.write("## All Concerts")
                concerts = get_all_concerts(connection)
                st.dataframe(concerts, width=700)

                
            elif selected_table == "concert_group":
                # Add concert_group CRUD operations
                st.sidebar.subheader("Concert Group CRUD Operations")

                # Display all concert groups
                st.write("## All Concert Groups")
                concert_groups = get_all_concert_groups(connection)
                st.dataframe(concert_groups, width=700)
                    
                    
            elif selected_table == "customer":
                # Add customer CRUD operations
                st.sidebar.subheader("Customer CRUD Operations")

                # Display all customers
                st.write("## All Customers")
                customers = get_all_customers(connection)
                st.dataframe(customers, width=700)

                # Add a new customer
                st.sidebar.subheader("Add New Customer:")
                customer_id = st.sidebar.number_input("Customer ID:", min_value=1)
                customer_name = st.sidebar.text_input("Customer Name:")
                email = st.sidebar.text_input("Email:")
                user_name = st.sidebar.text_input("User Name:")
                password = st.sidebar.text_input("Password:", type="password")

                if st.sidebar.button("Add Customer"):
                    insert_customer(connection, customer_id, customer_name, email, user_name, password)
                    
            elif selected_table == "customer_order":
                # Add customer_order CRUD operations
                st.sidebar.subheader("Customer Order CRUD Operations")

                # Display all customer orders
                st.write("## All Customer Orders")
                customer_orders = get_all_customer_orders(connection)
                st.dataframe(customer_orders, width=700)

                # Add a new customer order
                st.sidebar.subheader("Add New Customer Order:")
                customer_order_id = st.sidebar.number_input("Customer Order ID:", min_value=1)
                customer_id = st.sidebar.number_input("Customer ID:", min_value=1)
                registered_email_address = st.sidebar.text_input("Registered Email Address:")
                total_price = st.sidebar.number_input("Total Price:", min_value=0.0)
                discount = st.sidebar.number_input("Discount:", min_value=0.0)
                final_price = st.sidebar.number_input("Final Price:", min_value=0.0)

                if st.sidebar.button("Add Customer Order"):
                    insert_customer_order(connection, customer_order_id, customer_id, registered_email_address, total_price, discount, final_price)
                
            elif selected_table == "genre":
                # Add genre CRUD operations
                st.sidebar.subheader("Genre CRUD Operations")

                # Display all genres
                st.write("## All Genres")
                genres = get_all_genres(connection)
                st.dataframe(genres, width=700)
                
            elif selected_table == "order_ticket":
                # Add order_ticket CRUD operations
                st.sidebar.subheader("Order Ticket CRUD Operations")

                # Display all order tickets
                st.write("## All Order Tickets")
                order_tickets = get_all_order_tickets(connection)
                st.dataframe(order_tickets, width=700)

                # Add a new order ticket
                st.sidebar.subheader("Add New Order Ticket:")
                order_ticket_id = st.sidebar.number_input("Order Ticket ID:", min_value=1)
                customer_order_id = st.sidebar.number_input("Customer Order ID:", min_value=1)
                ticket_id = st.sidebar.number_input("Ticket ID:", min_value=1)

                if st.sidebar.button("Add Order Ticket"):
                    insert_order_ticket(connection,order_ticket_id, customer_order_id, ticket_id)
                
            elif selected_table == "ticket":
                # Add ticket CRUD operations
                st.sidebar.subheader("Ticket CRUD Operations")

                # Display all tickets
                st.write("## All Tickets")
                tickets = get_all_tickets(connection)
                st.dataframe(tickets, width=700)

                # Add a new ticket
                st.sidebar.subheader("Add New Ticket:")
                ticket_id = st.sidebar.number_input("Ticket ID:", min_value=1)
                serial_number = st.sidebar.text_input("Serial Number:")
                concert_id = st.sidebar.number_input("Concert ID:", min_value=1)
                ticket_category_id = st.sidebar.number_input("Ticket Category ID:", min_value=1)
                seat = st.sidebar.text_input("Seat:")
                purchase_date = st.sidebar.date_input("Purchase Date:")

                if st.sidebar.button("Add Ticket"):
                    insert_ticket(connection,ticket_id, serial_number, concert_id, ticket_category_id, seat, purchase_date)

                

            elif selected_table == "ticket_category":
                # Add ticket_category CRUD operations
                st.sidebar.subheader("Ticket Category CRUD Operations")

                # Display all ticket categories
                st.write("## All Ticket Categories")
                ticket_categories = get_all_ticket_categories(connection)
                st.dataframe(ticket_categories, width=700)

                
            elif selected_table == "venue":
                # Add venue CRUD operations
                st.sidebar.subheader("Venue CRUD Operations")
                select_crud = st.sidebar.selectbox("CRUD", ["create","delete", "update"])

                # Display all venues
                st.write("## All Venues")
                venues = get_all_venues(connection)
                st.dataframe(venues, width=700)

                
            elif selected_table == "join tables":
                st.sidebar.subheader("Join Tables")
                selected_join = st.sidebar.selectbox("Join", ["artist_genre"])

                # Display the joined data
                st.write("## Joined Data from Artist and Genre Tables")
                joined_data = None
                if selected_join == "artist_genre":
                    joined_data = join_artist_genre(connection)

                st.dataframe(joined_data, width=700)
            connection.close()


if __name__ == '__main__':
    main()


