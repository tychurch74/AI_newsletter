import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Your email credentials
sender_email = "tychurch74@gmail.com"
password = "123theboy"

# Read the email list
with open("email_list.txt", "r") as file:
    email_list = [line.strip() for line in file]

# Read the HTML newsletter content
with open("newsletter.html", "r") as file:
    html_content = file.read()

# Send the email to each recipient
for recipient_email in email_list:
    # Create the email message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your Newsletter Subject"
    msg["From"] = sender_email
    msg["To"] = recipient_email

    # Attach the HTML content
    mime_text = MIMEText(html_content, "html")
    msg.attach(mime_text)

    # Send the email
    with smtplib.SMTP_SSL(
        "smtp.gmail.com", 465
    ) as server:  # Use the appropriate SMTP server for your email provider
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"Email sent to {recipient_email}")

print("All emails sent!")
