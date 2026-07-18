from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_from_directory
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from werkzeug.utils import secure_filename
import numpy as np
from flask_mail import Mail, Message
import mysql.connector
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
import razorpay
from dotenv import load_dotenv
from google import genai

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "YOURMAILID@gmail.com"
app.config["MAIL_PASSWORD"] = "XXXXXXXXXXX"

mail = Mail(app)

client = genai.Client(api_key="API_KEY")
def generate_recommendation(dietray_preferences, fitness_goals, lifestyle_factors,
                            Dietray_restriction, health_conditions, user_query):

    prompt = f"""
Suggest a comprehensive diet and workout plan.

Dietary preferences: {dietray_preferences}
Fitness goals: {fitness_goals}
Lifestyle factors: {lifestyle_factors}
Dietary restriction: {Dietray_restriction}
Health conditions: {health_conditions}
User query: {user_query}

Give:
1. 5 diet recommendations
2. 5 workout options
3. 5 breakfast ideas
4. 5 dinner options
5. Snacks, supplements, hydration tips
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "PASSWORD",
    "database": "DATABASE_NAME"
}
load_dotenv()

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

razorpay_client = razorpay.Client(
    auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)
)
DOCTORS = [
    {"name": "Dr. Ananya Sen", "speciality": "General Physician", "time": "10:00 AM - 1:00 PM", "mode": "Clinic / Online", "fee": "₹500"},
    {"name": "Dr. Ritam Roy", "speciality": "Mental Wellness", "time": "2:00 PM - 5:00 PM", "mode": "Online", "fee": "₹500"},
    {"name": "Dr. Priya Das", "speciality": "Dermatologist", "time": "6:00 PM - 8:00 PM", "mode": "Clinic", "fee": "₹500"},
]

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS APPOINTMENTS (
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
            STATUS VARCHAR(30) DEFAULT 'Appointment Initiated',
            CREATED_AT VARCHAR(50) NOT NULL
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

UPLOAD_FOLDER = "./uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

model = load_model("models/model_Fixed.keras")

class_labels = ['glioma', 'meningioma', 'notumor', 'pituitary']


def predict_tumor(image_path):
    IMAGE_SIZE = 128
    img = load_img(image_path, target_size=(IMAGE_SIZE, IMAGE_SIZE))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    confidence_score = np.max(predictions, axis=1)[0]

    if class_labels[predicted_class_index] == 'notumor':
        return "No Tumor", confidence_score
    else:
        return f"Tumor: {class_labels[predicted_class_index]}", confidence_score
    

skin_model = load_model("models/model_cancer.keras")

skin_labels = ['actinic keratosis', 'basal cell carcinoma', 'dermatofibroma', 'melanoma', 'nevus', 'pigmented benign keratosis', 'seborrheic keratosis', 'squamous cell carcinoma', 'vascular lesion']

def predict_skin(image_path):
    IMAGE_SIZE = 128
    img = load_img(image_path, target_size=(IMAGE_SIZE, IMAGE_SIZE))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = skin_model.predict(img_array)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    confidence_score = np.max(predictions, axis=1)[0]

    return skin_labels[predicted_class_index], confidence_score
def get_ai_advice(disease_name):

    prompt = f"""
You are an experienced medical assistant.

The AI model predicted:

{disease_name}

Provide the following in simple English.

1. Disease Overview
2. Possible Symptoms
3. Possible Causes
4. Recommended Medical Treatment
5. What to Do
6. What NOT to Do
7. Diet Recommendations
8. Lifestyle Tips
9. When to Consult a Doctor
10. Emergency Warning Signs

Important:
- Use bullet points.
- Keep it easy to understand.
- Do NOT claim the prediction is 100% correct.
- End with:
"This information is educational only and not a substitute for professional medical advice."
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    advice = response.text
    advice = advice.replace("*", "")
    advice = advice.replace("#", "")
    return advice

""" @app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        model_type = request.form.get('model_type')

        if file:
            filename = secure_filename(file.filename)
            file_location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_location)

            if model_type == "brain":
                result, confidence = predict_tumor(file_location)

            elif model_type == "skin":
                result, confidence = predict_skin(file_location)

            else:
                result, confidence = "Invalid Selection", 0

            ai_advice = get_ai_advice(result)

            return render_template(
                'index.html',
                result=result,
                Confidence=f'{confidence*100:.2f}%',
                file_path=f'/uploads/{filename}',
                advice=ai_advice
            )

    return render_template('index.html', result=None) """
@app.route("/disease", methods=["GET", "POST"])
def disease():

    if request.method == "POST":
        file = request.files["file"]
        model_type = request.form.get("model_type")

        if file:
            filename = secure_filename(file.filename)
            file_location = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_location)

            if model_type == "brain":
                result, confidence = predict_tumor(file_location)

            elif model_type == "skin":
                result, confidence = predict_skin(file_location)

            else:
                result, confidence = "Invalid Selection", 0

            ai_advice = get_ai_advice(result)

            return render_template(
                "disease.html",
                result=result,
                Confidence=f"{confidence*100:.2f}%",
                file_path=f"/uploads/{filename}",
                advice=ai_advice
            )

    return render_template("disease.html")

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route('/')
def home():
    return render_template(
        'index.html',
        doctors=DOCTORS,
        user_name=session.get('user_name'),
        role=session.get('role'),
        appointment_booked=False
    )

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/user-signup', methods=['POST'])
def user_signup():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    mobile = request.form.get('mobile', '').strip()
    password = request.form.get('password', '').strip()

    if not name or not email or not mobile or not password:
        flash('Please fill all signup details.', 'error')
        return redirect(url_for('login'))

    hashed_password = generate_password_hash(password)

    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO USERS (NAME, EMAIL, MOBILE, PASSWORD)
            VALUES (%s, %s, %s, %s)
        """, (name, email, mobile, hashed_password))

        conn.commit()
        flash('Signup successful! Please login now.', 'success')

    except mysql.connector.IntegrityError:
        flash('Email already registered. Please login.', 'error')

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('login'))

@app.route('/user-login', methods=['POST'])
def user_login():
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM USERS WHERE EMAIL = %s", (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user and check_password_hash(user['PASSWORD'], password):
        session.clear()
        session['user_id'] = user['USER_ID']
        session['user_name'] = user['NAME']
        session['user_email'] = user['EMAIL']
        session['role'] = 'user'
        return redirect(url_for('home'))

    flash('Invalid email or password.', 'error')
    return redirect(url_for('login'))

@app.route('/admin-login', methods=['POST'])
def admin_login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM ADMINS WHERE USERNAME = %s", (username,))
    admin = cursor.fetchone()

    cursor.close()
    conn.close()

    if admin and admin['PASSWORD'] == password:
        session.clear()
        session['admin_id'] = admin['ADMIN_ID']
        session['user_name'] = 'Admin'
        session['role'] = 'admin'
        return redirect(url_for('admin_appointments'))

    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/appointment')
def appointment():
    if session.get('role') != 'user':
        flash('Please login first to book an appointment.', 'error')
        return redirect(url_for('login'))

    return render_template(
        'appointment.html',
        doctors=DOCTORS,
        user_name=session.get('user_name'),
        user_email=session.get('user_email'),
        role=session.get('role')
    )

@app.route('/book-appointment', methods=['POST'])
def book_appointment():
    if session.get('role') != 'user':
        return redirect(url_for('login'))

    form = request.form

    required = [
        'patient_name', 'email', 'mobile', 'age', 'gender', 'doctor',
        'appointment_date', 'appointment_time', 'consultation_type', 'symptoms'
    ]

    if any(not form.get(field, '').strip() for field in required):
        flash('Please fill all appointment details.', 'error')
        return redirect(url_for('appointment'))

    consultation_type = form['consultation_type'].strip()
    doctor_fee = 500

    session["appointment_data"] = {
        "patient_name": form["patient_name"].strip(),
        "email": session.get("user_email"),
        "mobile": form["mobile"].strip(),
        "age": form["age"].strip(),
        "gender": form["gender"].strip(),
        "doctor": form["doctor"].strip(),
        "appointment_date": form["appointment_date"].strip(),
        "appointment_time": form["appointment_time"].strip(),
        "consultation_type": consultation_type,
        "symptoms": form["symptoms"].strip()
    }
    razorpay_order = razorpay_client.order.create({
        "amount": doctor_fee * 100,
        "currency": "INR",
        "payment_capture": 1
    })
    session["razorpay_order_id"] = razorpay_order["id"]
    return render_template(
        "payment.html",
        key_id=RAZORPAY_KEY_ID,
        order_id=razorpay_order["id"],
        amount=doctor_fee,
        user_name=session.get("user_name"),
        user_email=session.get("user_email")
    )
    
@app.route('/verify-payment', methods=['POST'])
def verify_payment():
    data = request.get_json()

    try:
        # Verify Razorpay signature
        razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id": data["razorpay_order_id"],
            "razorpay_payment_id": data["razorpay_payment_id"],
            "razorpay_signature": data["razorpay_signature"]
        })

        # Get appointment details from session
        appointment = session.get("appointment_data")

        if not appointment:
            return jsonify({
                "status": "failed",
                "message": "Appointment session expired."
            }), 400

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO APPOINTMENTS
            (
                PATIENT_NAME,
                EMAIL,
                MOBILE,
                AGE,
                GENDER,
                DOCTOR,
                APPOINTMENT_DATE,
                APPOINTMENT_TIME,
                CONSULTATION_TYPE,
                SYMPTOMS,
                STATUS,
                DOCTOR_FEE,
                PAYMENT_STATUS,
                RAZORPAY_PAYMENT_ID,
                RAZORPAY_ORDER_ID,
                CREATED_AT
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            appointment["patient_name"],
            appointment["email"],
            appointment["mobile"],
            appointment["age"],
            appointment["gender"],
            appointment["doctor"],
            appointment["appointment_date"],
            appointment["appointment_time"],
            appointment["consultation_type"],
            appointment["symptoms"],
            "Appointment Initiated",
            500,
            "Paid",
            data["razorpay_payment_id"],
            data["razorpay_order_id"],
            datetime.now().strftime("%d %b %Y, %I:%M %p")
        ))

        appointment_id = cursor.lastrowid

        conn.commit()

        cursor.close()
        conn.close()

        # Clear session data
        session.pop("appointment_data", None)
        session.pop("razorpay_order_id", None)

        return jsonify({
            "status": "success",
            "appointment_id": appointment_id
        })

    except Exception as e:
        print(e)
        return jsonify({
            "status": "failed"
        }), 400
@app.route("/payment_receipt/<int:appointment_id>")
def payment_receipt(appointment_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM APPOINTMENTS
        WHERE ID = %s
    """, (appointment_id,))

    receipt = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("payment_receipt.html", receipt=receipt)
@app.route('/update-payment/<int:id>', methods=['POST'])
def update_payment(id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    payment_status = request.form.get('payment_status')

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE APPOINTMENTS
        SET PAYMENT_STATUS = %s
        WHERE ID = %s
    """, (payment_status, id))

    conn.commit()
    cursor.close()
    conn.close()

    flash('Payment status updated successfully!', 'success')
    return redirect(url_for('admin_appointments'))
@app.route('/track-appointments')
def track_appointments():

    if not session.get('user_id'):
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM APPOINTMENTS
        WHERE EMAIL = %s
        ORDER BY ID DESC
    """, (session.get('user_email'),))

    appointments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'track_appointments.html',
        appointments=appointments
    )
@app.route('/admin/appointments')
def admin_appointments():
    if session.get('role') != 'admin':
        #flash('Please login as admin first.', 'error')
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            ID AS id,
            PATIENT_NAME AS patient_name,
            EMAIL AS email,
            MOBILE AS mobile,
            AGE AS age,
            GENDER AS gender,
            DOCTOR AS doctor,
            APPOINTMENT_DATE AS appointment_date,
            APPOINTMENT_TIME AS appointment_time,
            CONSULTATION_TYPE AS consultation_type,
            SYMPTOMS AS symptoms,
            STATUS AS status,
            DOCTOR_FEE AS doctor_fee,
            PAYMENT_STATUS AS payment_status,
            PAYMENT_LINK AS payment_link,
            CREATED_AT AS created_at
        FROM APPOINTMENTS
        ORDER BY ID DESC
    """)

    appointments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_appointments.html', appointments=appointments)

@app.route('/update-status/<int:id>', methods=['POST'])
def update_status(id):

    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    status = request.form.get('status')

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE APPOINTMENTS
        SET STATUS = %s
        WHERE ID = %s
    """, (status, id))

    conn.commit()

    cursor.close()
    conn.close()

    flash('Appointment status updated successfully!', 'success')

    return redirect(url_for('admin_appointments'))
@app.route('/api/appointments')
def api_appointments():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM APPOINTMENTS ORDER BY ID DESC")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(rows)

SYSTEM_PROMPT = """
You are MindMate HealthCare AI Chatbot.
Give basic health guidance, first-aid tips, diet suggestions, Health awareness,
doctor appointment guidance, and symptom explanation.
Do not give final medical diagnosis.
For emergency symptoms, tell user to seek emergency help immediately.
Keep answers simple.
"""

@app.route("/chat")
def chat_page():
    return render_template("chat.html")

@app.route("/chat-api", methods=["POST"])
def chat_api():

    data = request.get_json()
    user_message = data.get("message", "")

    if user_message == "":
        return jsonify({"reply": "Please type your health question."})

    prompt = SYSTEM_PROMPT + "\nUser: " + user_message

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return jsonify({
            "reply": response.text
        })

    except Exception:
        return jsonify({
            "reply": "AI service error."
        })

@app.route("/diet-planner")
def diet_planner():
    return render_template("diet_planner.html")

@app.route('/fitness_focus')
def fitness_focus():
    return render_template('fitness_focus.html')

@app.route('/smart_nutrition')
def smart_nutrition():
    return render_template('smart_nutrition.html')

@app.route("/recommendation", methods=["POST"])
def recommendation():
    dietray_preferences = request.form["dietray_preferences"]
    fitness_goals = request.form["fitness_goals"]
    lifestyle_factors = request.form["lifestyle_factors"]
    Dietray_restriction = request.form["Dietray_restriction"]
    health_conditions = request.form["health_conditions"]
    user_query = request.form["user_query"]

    recommendations_text = generate_recommendation(
        dietray_preferences,
        fitness_goals,
        lifestyle_factors,
        Dietray_restriction,
        health_conditions,
        user_query
    )

    return render_template("diet_planner.html", recommendations=recommendations_text)

@app.route('/health_awareness')
def health_awareness():
    return render_template('health_awareness.html')

@app.route('/first_aid')
def first_aid():
    return render_template('first_aid.html')

@app.route("/contact", methods=["POST"])
def contact():
    try:
        name = request.form["name"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        message = request.form["message"]

        msg = Message(
            subject="New Contact Message - MindMate",
            sender=app.config["MAIL_USERNAME"],
            recipients=["adey011003@gmail.com"]
        )

        msg.body = f"""
New Contact Message

Name: {name}
Email: {email}
Mobile: {mobile}

Message:
{message}
"""

        mail.send(msg)

        flash("Message sent successfully!", "success")

    except Exception as e:
        print("EMAIL ERROR:", repr(e))
        flash(f"Email failed: {e}", "error")

    return redirect(url_for("home"))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)