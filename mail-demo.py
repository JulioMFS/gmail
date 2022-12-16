
import os
import smtplib
import imghdr
from email.message import EmailMessage

os.environ['EMAIL_USER'] = 'sanfonaj@gmail.com'
os.environ['EMAIL_PASS'] = 'jumzifzrvptdkgll'

EMAIL_ADDRESS = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")

contacts = ["sanfonaj@gmail.com", "jsanfona@gmail.com"]

msg = EmailMessage()
msg["Subject"] = "Check out Bronx as a puppy"
msg["From"] = EMAIL_ADDRESS
#msg["To"] = ", ".join(contacts)
msg["To"] = "sanfonaj@gmail.com"
msg.set_content("Image attached...")

files = ["C:/Users/User/Downloads/IMG-20220625-WA0008.jpg", "C:/Users/User/Downloads/20220423_113313.jpg"]

for file in files:
    with open(file, "rb") as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name

    #    print(file_type)
    msg.add_attachment(file_data, maintype = "image", subtype = file_type, filename=file_name)

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
     smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

     smtp.send_message(msg)