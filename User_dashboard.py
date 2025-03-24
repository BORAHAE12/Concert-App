import streamlit as st
from artist import *
from concert import get_available_concerts
from customers import get_user_details, update_own_profile
from tickets import get_user_tickets, book_ticket, cancel_ticket
from Venue import *
from Genre import *

# def show_user_dashboard():
#     """User Dashboard for managing tickets, bookings, and profile."""
    
#     st.subheader("🎫 User Dashboard")
#     st.write("🎵 Welcome! Browse concerts, book tickets, and manage your profile.")

#     # Establish Database Connection
#     connection = create_connection()
#     if not connection or not connection.is_connected():
#         st.error("❌ Database connection failed.")
#         return

#     # Sidebar Navigation
#     selected_action = st.sidebar.selectbox(
#         "Choose Action", ["Browse Concerts", "Book Ticket", "View My Tickets", "Cancel Booking", "My Profile"]
#     )

#     if selected_action == "Browse Concerts":
#         browse_concerts(connection)
#     elif selected_action == "Book Ticket":
#         book_new_ticket(connection)
#     elif selected_action == "View My Tickets":
#         view_user_tickets(connection)
#     elif selected_action == "Cancel Booking":
#         cancel_user_ticket(connection)
#     elif selected_action == "My Profile":
#         manage_user_profile(connection)

#     connection.close()

# 🟢 Browse Available Concerts
def browse_concerts(connection):
    """Allows users to browse available concerts."""
    
    st.subheader("🎵 Browse Available Concerts")
    
    concerts = get_available_concerts(connection)
    if concerts:
        st.dataframe(concerts, width=800)
    else:
        st.warning("🚫 No concerts available at the moment.")

# 🎟️ Book a New Ticket
def book_new_ticket(connection):
    """Allows users to book a ticket for an available concert."""

    st.subheader("🎟️ Book a New Ticket")

    user_id = st.session_state.get("user_id", None)
    if not user_id:
        st.error("⚠️ User not logged in.")
        return

    concerts = get_available_concerts(connection)
    if not concerts:
        st.warning("🚫 No available concerts right now.")
        return

    # Select concert and ticket details
    concert_options = {c["concert_name"]: c["concert_id"] for c in concerts}
    selected_concert = st.selectbox("Choose a Concert", list(concert_options.keys()))
    ticket_category = st.selectbox("Ticket Category", ["Regular", "VIP", "Backstage Pass"])
    seat = st.text_input("Preferred Seat Number:")

    if st.button("Book Ticket"):
        ticket_id = book_ticket(connection, user_id, concert_options[selected_concert], ticket_category, seat)
        if ticket_id:
            st.success(f"🎟️ Ticket {ticket_id} booked successfully!")
            st.experimental_rerun()
        else:
            st.error("❌ Booking failed. Try again.")

# 📄 View User Tickets
def view_user_tickets(connection):
    """Displays all tickets booked by the user."""

    st.subheader("📄 My Tickets")

    user_id = st.session_state.get("user_id", None)
    if not user_id:
        st.error("⚠️ User not logged in.")
        return

    tickets = get_user_tickets(connection, user_id)
    if tickets:
        st.dataframe(tickets, width=700)
    else:
        st.warning("🚫 No tickets found.")

# ❌ Cancel Booking
def cancel_user_ticket(connection):
    """Allows users to cancel a booked ticket."""

    st.subheader("🚫 Cancel Booking")

    user_id = st.session_state.get("user_id", None)
    if not user_id:
        st.error("⚠️ User not logged in.")
        return

    user_orders = get_user_tickets(connection, user_id)
    if not user_orders:
        st.warning("🚫 No active bookings found.")
        return

    ticket_options = {f"Ticket {o['ticket_id']} - {o['concert_name']}": o["ticket_id"] for o in user_orders}
    selected_ticket = st.selectbox("Select Ticket to Cancel", list(ticket_options.keys()))

    if st.button("Cancel Booking"):
        if cancel_ticket(connection, ticket_options[selected_ticket]):
            st.success(f"✅ Ticket {ticket_options[selected_ticket]} canceled successfully!")
            st.rerun()
        else:
            st.error("❌ Failed to cancel ticket.")

# 🔄 Manage User Profile
def manage_user_profile(connection):
    """Allows users to update their profile details securely."""

    st.subheader("🔄 Update Profile")

    user_id = st.session_state.get("user_id", None)
    if not user_id:
        st.error("⚠️ User not logged in.")
        return

    user_details = get_user_details(connection, user_id)
    if not user_details:
        st.error("⚠️ Unable to fetch user details.")
        return

    st.write(f"👤 **Username:** {user_details['user_name']}")
    st.write(f"📧 **Current Email:** {user_details['email']}")

    # Fields for updating profile
    new_email = st.text_input("New Email:", user_details["email"])
    new_password = st.text_input("New Password:", type="password")

    if st.button("Update Profile"):
        update_own_profile(connection, user_id, new_email, new_password)
        st.success("✅ Profile updated successfully!")
        st.rerun()
