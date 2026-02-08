from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'your_secret_key_change_this_in_production'

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form.get('name', '').strip()
        user_email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        if not name or not user_email or not message:
            return render_template('error.html', error="All fields are required")

        sender_email = "your_email@gmail.com"
        app_password = "app_password"

        user_msg = MIMEMultipart()
        user_msg['From'] = sender_email
        user_msg['To'] = user_email
        user_msg['Subject'] = "Thank you for your submission"

        user_body = f"""Hi {name},

Thank you for your submission. We have received the following message:

{message}

We will get back to you soon.

Best regards,
Your Team"""

        user_msg.attach(MIMEText(user_body, 'plain'))

        admin_msg = MIMEMultipart()
        admin_msg['From'] = sender_email
        admin_msg['To'] = sender_email
        admin_msg['Subject'] = f"New Form Submission from {name}"

        admin_body = f"""New submission details:

Name: {name}
Email: {user_email}
Message: {message}"""

        admin_msg.attach(MIMEText(admin_body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)

        server.sendmail(sender_email, [user_email], user_msg.as_string())
        server.sendmail(sender_email, [sender_email], admin_msg.as_string())
        server.quit()

        return render_template('success.html', name=name)

    except smtplib.SMTPAuthenticationError as e:
        error_msg = "Authentication failed. Please check your email and app password."
        return render_template('error.html', error=error_msg)

    except smtplib.SMTPRecipientsRefused as e:
        error_msg = f"Invalid recipient email address: {user_email}"
        return render_template('error.html', error=error_msg)

    except smtplib.SMTPException as e:
        error_msg = f"SMTP error occurred: {str(e)}"
        return render_template('error.html', error=error_msg)

    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return render_template('error.html', error=error_msg)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
