# MindMate – AI Healthcare Management System:
MindMate is a full-stack AI-powered healthcare management system designed to simplify medical services with smart automation. It integrates Machine Learning, APIs, Database Management, and Online Payments into a single platform.

### Project Repository:
`
https://github.com/Arpan-Dey0305/MindMate-Healthcare-Management-System
`

---

## Features:
- AI Medical Detection (Image-based disease prediction)
- Smart AI Chatbot (Medicine suggestions & assistance)
- Doctor Appointment Booking System
- Online Payment Integration (Razorpay)
- User & Admin Management System
- Email Notifications (Flask-Mail)
- Database Integration (MySQL)

---

## Tech Stack:
- Frontend: HTML, CSS, JavaScript, Bootstrap
- Backend: Flask (Python)
- Database: MySQL
- Machine Learning: TensorFlow, Keras
- APIs: Google GenAI
- Payment Gateway: Razorpay

---

## Installation & Setup:
1. Clone the Repository:
```
git clone https://github.com/Arpan-Dey0305/MindMate-Healthcare-Management-System.git
cd MindMate-Healthcare-Management-System
```

2. Create Virtual Environment:
```
python -m venv venv
```

3. Activate Virtual Environment:
   - Windows
    ```
    venv\Scripts\activate
    ```
   - Mac / Linux
    ```
    source venv/bin/activate
    ```
4. Install Dependencies:
```
pip install tensorflow==2.19.0 keras==3.5.0 numpy==1.26.4 pillow flask flask_mail google-genai python-dotenv werkzeug mysql-connector-python razorpay
```

---

## Database Setup (MySQL):
### 1. Create Database:
```sql
CREATE DATABASE MINDMATE_DB;
USE MINDMATE_DB;```sql
CREATE DATABASE MINDMATE_DB;
USE MINDMATE_DB;
```
### 2. Import Tables:
``` sql
mysql -u root -p MINDMATE_DB < database/mindmate.sql
```
## Tables Included:
- ADMINS
- USERS
- APPOINTMENTS
### USERS Table:
``` sql
CREATE TABLE USERS (
    USER_ID INT AUTO_INCREMENT PRIMARY KEY,
    NAME VARCHAR(100) NOT NULL,
    EMAIL VARCHAR(100) NOT NULL UNIQUE,
    MOBILE VARCHAR(15) NOT NULL,
    PASSWORD VARCHAR(255) NOT NULL
);
```
### ADMINS Table:
``` sql
CREATE TABLE ADMINS (
    ADMIN_ID INT AUTO_INCREMENT PRIMARY KEY,
    USERNAME VARCHAR(50) NOT NULL UNIQUE,
    PASSWORD VARCHAR(255) NOT NULL
);
```

### APPOINTMENTS Table:
``` sql
CREATE TABLE APPOINTMENTS (
   ID INT AUTO_INCREMENT PRIMARY KEY,
   PATIENT_NAME VARCHAR(100) NOT NULL,
   EMAIL VARCHAR(100) NOT NULL,
   MOBILE VARCHAR(15) NOT NULL,
   AGE INT NOT NULL,
   GENDER VARCHAR(20) NOT NULL,
   DOCTOR VARCHAR(100) NOT NULL,
   APPOINTMENT_DATE DATE NOT NULL,
   APPOINTMENT_TIME VARCHAR(50) NOT NULL,
   CONSULTATION_TYPE VARCHAR(50) NOT NULL,
   SYMPTOMS TEXT NOT NULL,
   STATUS VARCHAR(30) DEFAULT 'pending',
   CREATED_AT VARCHAR(50) NOT NULL,
   PAYMENT_STATUS VARCHAR(30) DEFAULT 'Payment Pending',
   PAYMENT_LINK VARCHAR(500) DEFAULT NULL,
   DOCTOR_FEE INT DEFAULT 500,
   RAZORPAY_ORDER_ID VARCHAR(100) DEFAULT NULL,
   RAZORPAY_PAYMENT_ID VARCHAR(100) DEFAULT NULL
   );
```

---

## Run the Application:
`python app.py`
Then open your browser and go to:
`http://127.0.0.1:5000/`

---

## Environment Variables:

Create a `.env` file in the root directory and add:
```
SECRET_KEY=your_secret_key
MAIL_USERNAME=your_email
MAIL_PASSWORD=your_email_password
RAZORPAY_KEY_ID=your_key
RAZORPAY_KEY_SECRET=your_secret
```
---

## Future Improvements:
- More accurate AI models
- Mobile responsive enhancements
- Admin analytics dashboard
- Multi-hospital integration
- Ambulance Facility
---

## Author:
Arpan Dey<br>
Final Year CSE Student | Python Developer<br>
Mobile - +91 8710042392<br>
E-mail - adey011003@gmail.com<br>
Portfolio - https://portfolio-arpan-snowy.vercel.app<br>
Linkedin - https://www.linkedin.com/in/arpan-dey-25748526a<br>
Github - https://github.com/Arpan-Dey0305

---
## Show Your Support:
If you like this project, please ⭐ star the repository and share it!
