# 🛒 Online Auction System

An intuitive and feature-rich online auction platform built with Django. Users can post items for auction, place bids in real-time, and manage their activity securely with full user authentication, authorization, and notifications.

---

## 🚀 Features

- 🔐 **User Authentication & Authorization**  
  Secure login system with email verification for valid users.

- 📬 **Email Verification**  
  Confirms new users before they can access core functionalities.

- 💬 **Notification System**  
  Real-time alerts on bidding activity and auction outcomes.

- 🧾 **Product Management**  
  Full CRUD support for auction item listings.

- 💰 **Bidding System**  
  Real-time bid tracking, current highest bid display, and activity logging.

- 📊 **Admin Panel**  
  Powerful admin dashboard using Django's admin site.

- 🌐 **Responsive UI**  
  Built with Bootstrap for mobile-friendly viewing.

---

## ⚙️ Setup Procedures

Follow these steps to get the project up and running locally:

### 1. Clone the Repository
```bash
git clone https://github.com/rasel-33/online-auction.git
cd online-auction
```
### 2. Set Up Virtual Environment
```
python -m venv venv
source venv/bin/activate          # On Windows: venv\\Scripts\\activate
```

### 3. Install Required Packages
```
pip install -r requirements.txt

```

### 4. Configure Email (for verification)
```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_password'
EMAIL_USE_TLS = True
```

### 5. Apply Migrations and Create Superuser
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

```
### 6. Run the Server
```
python manage.py runserver

```
## 📷 Screenshots

> Save these images in a `/screenshots` folder inside your project

| Homepage | Product Detail | Bid Panel |
|----------|----------------|-----------|
| ![](screenshots/home.png) | ![](screenshots/product.png) | ![](screenshots/bid.png) |

---
