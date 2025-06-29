import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import time

def capture_photo(filename):
    os.system(f"gphoto2 --capture-image-and-download --filename {filename}")

def send_email(image_path, recipient):\
    # Email configuration (update with your SMTP details)
    smtp_server = "smtp.example.com"
    smtp_port = 587
    username = "your_email@example.com"
    password = "your_password"
    
    # Create message
    msg = MIMEMultipart()
    msg['Subject'] = 'Your Photo Booth Picture!'
    msg['From'] = username
    msg['To'] = recipient
    
    # Add image
    with open(image_path, 'rb') as f:
        img = MIMEImage(f.read())
    msg.attach(img)
    
    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)

def main():
    print("Welcome to the Photo Booth!")
    email = input("Enter your email address: ")
    
    filename = f"photo_{int(time.time())}.jpg"
    
    print("Smile! Taking photo in 3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    
    capture_photo(filename)
    print("Photo captured! Sending to your email...")
    
    send_email(filename, email)
    print("Email sent! Thank you!")
    
    # Optional: Delete the local file after sending
    os.remove(filename)

if __name__ == "__main__":
    main()