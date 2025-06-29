import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import time
import cameraOperation
import re

def main():
    clear = lambda: os.system('clear')
    
    #clear console to remove previous uses logs
    clear()
    print("Welcome to the Photo Booth!")
    #Todo can ask if we want to keep it? might be cool for media stuff
    print("[don't worry, your pic isnt stored after we email it to you.]\n")
    
    # Use regex to make sure its an email
    while True:
        email = input("email address: ")
        if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            break
        else:
            print("that email doesn't look valid to me.")
    
    filename = f"photo_{int(time.time())}-{email}.jpg"
    
    # ask user how long they want to wait
    while True:
        try:
            userIn = int(input("how long do you need? (timer in seconds): "))
            break
        except ValueError:
            print("integer please.")
    
    if userIn >= 40:
        # no one needs this long
        print("way too long of a timer")
    
    else:
        # Countdown for userIn
        #TODO add flash blinking for timer??
        for i in range(userIn, 0, -1):
            print(f"Smile! Taking photo in {i}...")
            time.sleep(1)
        
        cameraOperation.capture_photo(filename, cameraOperation.find_camera_port())
        
        print(f"Photo captured! Sending to your email: {email}...")
        
        try:
            send_email(filename, email)
        except:
            print("something happened. contact someone from dev.")
            
        print("Email sent! Thank you for stopping by! :)")
        
        # delete the local file after sending
        os.remove(filename)

# add email stuff
def send_email(image_path: str, recipient: str):
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

if __name__ == "__main__":
    while (True):
        main()