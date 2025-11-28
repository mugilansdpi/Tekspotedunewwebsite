from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ✅ GOOGLE WORKSPACE SMTP SETTINGS
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# ✅ LOGIN MUST BE PRIMARY ACCOUNT
app.config['MAIL_USERNAME'] = 'mugilansdpi@gmail.com'  

# ✅ USE APP PASSWORD (NOT NORMAL PASSWORD)
app.config['MAIL_PASSWORD'] = 'mlcg kvfv ipvk nqjg'

#  mlcg kvfv ipvk nqjg  this is mugilan personal

# ✅ SENDER MUST BE ALIAS
app.config['MAIL_DEFAULT_SENDER'] = 'mugilansdpi@gmail.com'

mail = Mail(app)

# -------------------------
# ✅ SEND EMAIL API
# -------------------------
@app.route('/send_mail', methods=['POST'])
def send_mail_route():
    try:
        data = request.get_json()

        name = data.get("name", "")
        phone = data.get("phone", "")
        user_email = data.get("email", "")

        # ✅ 1. MAIL TO ADMIN (RETAINED)
        # This message notifies the administrator about the new submission.
        admin_msg = Message(
            subject="New Form Submission",
            sender="mugilansdpi@gmail.com",  # Sent from alias
            recipients=["mugilan18sdpi@gmail.com"],  # Admin receiver
            reply_to=user_email,
            body=f"""
New Form Submission:

Name: {name}
Phone: {phone}
Email: {user_email}
"""
        )

        mail.send(admin_msg)

        # ❌ 2. GREETING MAIL TO USER - REMOVED

        return jsonify({
            "status": "success",
            # Updated message to reflect that only the Admin was notified.
            "message": "Admin notified successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500



@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()

    required = ["name", "email", "phone", "subject", "message"]
    if not all(key in data and data[key] for key in required):
        return jsonify({"message": "All fields are required"}), 400

    msg = Message(
        subject=f"New Contact Form: {data['subject']}",
        recipients=["mugilan18sdpi@gmail.com"],  # ✅ Receiver
        reply_to=data['email'],
        body=f"""
New Contact Message:

Name: {data['name']}
Email: {data['email']}
Phone: {data['phone']}
Subject: {data['subject']}

Message:
{data['message']}
"""
    )

    try:
        mail.send(msg)
        return jsonify({"message": "Message sent successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500




@app.route("/submit-form", methods=["POST"])
def submit_form():
    try:
        data = request.get_json()

        name = data.get("firstName", "")
        email = data.get("email", "")
        phone = data.get("phone", "")
        course = data.get("courseTitle", "")
        message = data.get("message", "")

        print("New Form Submission:")
        print("Name:", name)
        print("Email:", email)
        print("Phone:", phone)
        print("Course:", course)
        print("Message:", message)

        # ✅ EMAIL BODY
        email_body = f"""
New Course Enquiry Received:

Name: {name}
Email: {email}
Phone: {phone}
Course: {course}

Message:
{message}
        """

        # ✅ SEND EMAIL TO THIS ADDRESS
        msg = Message(
            subject="New Course Enquiry",
            recipients=["mugilan18sdpi@gmail.com"],   # ✅ YOUR TARGET EMAIL
            body=email_body
        )

        mail.send(msg)

        return jsonify({
            "status": "success",
            "message": "Form submitted and email sent successfully"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
