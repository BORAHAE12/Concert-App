# 🚀 Concert Management System 🎵  
📌 **Status:** 🚧 Work in Progress  

A **secure, role-based concert management system** where:  
✅ **Users** can **browse concerts, book tickets, and manage bookings**  
✅ **Admins** can **manage venues, artists, customer data, and bookings**  

---

## 📌 Features (Under Development 🚧)  
✅ **User Dashboard:** Browse concerts, book tickets, cancel bookings  
✅ **Admin Dashboard:** Manage concerts, customers, artists, and venues  
✅ **Secure Login & Authentication:** JWT-based authentication with role-based access  
✅ **Database Integration:** Uses **MySQL** (Railway or Localhost)  
✅ **CRUD Operations:** Manage concerts, venues, tickets, orders, and users  
✅ **Role-Based Access:** Admin vs User functionality  
✅ **Secure Password Hashing:** Using bcrypt  
✅ **Session Management:** JWT Authentication  
✅ **Real-Time Data Updates** using Streamlit  
🚀 **Upcoming Features:** AI-based recommendations, seat selection, Docker Support  

---

## 🔧 Tech Stack  
- **Frontend:** Streamlit  
- **Backend:** Python  
- **Database:** MySQL (Local & Cloud)  
- **Authentication:** JWT (JSON Web Token)  
- **Security:** Bcrypt for password hashing  
- **Hosting:** Railway (WIP) or streamlit cloud

---

## 📂 Project Structure  
```bash
📁 Concert-Management-System/
│── 📜 secure_testing_app.py     # Main Streamlit App
│── 📜 database.py               # MySQL Database Connection
│── 📜 testing_security.py       # Authentication & Security
│── 📜 User_dashboard.py         # User Role Dashboard
│── 📜 Admin_dashboard.py        # Admin Role Dashboard
│── 📜 artist.py                 # CRUD for Artists
│── 📜 concert.py                # CRUD for Concerts
│── 📜 customers.py              # CRUD for Customers
│── 📜 tickets.py                # CRUD for Tickets
│── 📜 Venue.py                  # CRUD for Venues
│── 📜 Genre.py                  # CRUD for Genres
│── 📜 User.py                   # CRUD for Users & Authentication
│── 📜 requirements.txt          # Python dependencies
│── 📜 README.md                 # Project Documentation (This File)
