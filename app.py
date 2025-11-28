from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ✅ GOOGLE SMTP SETTINGS
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# ✅ LOGIN MUST BE PRIMARY GMAIL (USED FOR SMTP LOGIN)
app.config['MAIL_USERNAME'] = 'mugilansdpi@gmail.com'  

# ✅ USE ONLY GMAIL APP PASSWORD (NOT NORMAL PASSWORD)
app.config['MAIL_PASSWORD'] = 'mlcg kvfv ipvk nqjg'   # ⚠️ Keep only App Password here

# ✅ DEFAULT SENDER MUST MATCH LOGIN OR A VERIFIED ALIAS
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

        # ✅ 1. MAIL TO ADMIN
        admin_msg = Message(
            subject="New Form Submission",
            recipients=["mugilan18sdpi@gmail.com"],  # ✅ Admin receiver
            reply_to=user_email,
            body=f"""
New Form Submission:

Name: {name}
Phone: {phone}
Email: {user_email}
"""
        )

        mail.send(admin_msg)

        return jsonify({
            "status": "success",
            "message": "Admin notified successfully"
        }), 200

    except Exception as e:
        print("SEND_MAIL ERROR:", str(e))   # ✅ shows exact SMTP issue in logs
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# -------------------------
# ✅ CONTACT FORM API
# -------------------------
@app.route('/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()

        required = ["name", "email", "phone", "subject", "message"]
        if not all(key in data and data[key] for key in required):
            return jsonify({"message": "All fields are required"}), 400

        msg = Message(
            subject=f"New Contact Form: {data['subject']}",
            recipients=["mugilan18sdpi@gmail.com"],
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

        mail.send(msg)
        return jsonify({"message": "Message sent successfully"}), 200

    except Exception as e:
        print("CONTACT ERROR:", str(e))
        return jsonify({"message": str(e)}), 500


# -------------------------
# ✅ COURSE ENQUIRY API
# -------------------------
@app.route("/submit-form", methods=["POST"])
def submit_form():
    try:
        data = request.get_json()

        name = data.get("firstName", "")
        email = data.get("email", "")
        phone = data.get("phone", "")
        course = data.get("courseTitle", "")
        message = data.get("message", "")

        email_body = f"""
New Course Enquiry Received:

Name: {name}
Email: {email}
Phone: {phone}
Course: {course}

Message:
{message}
        """

        msg = Message(
            subject="New Course Enquiry",
            recipients=["mugilan18sdpi@gmail.com"],
            body=email_body
        )

        mail.send(msg)

        return jsonify({
            "status": "success",
            "message": "Form submitted and email sent successfully"
        }), 200

    except Exception as e:
        print("SUBMIT FORM ERROR:", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ✅ HELLO API FOR RENDER TESTING
@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({
        "status": "success",
        "message": "Hello API is working fine ✅"
    }), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
