# WatchDog Keylogger

WatchDog is a Python-based keylogger tool designed to silently capture keyboard input, mouse events, and system information. It periodically sends logged data via email, providing a discreet method for monitoring user activities on a system.

## Features

- Captures keyboard input (keystrokes) and special keys.
- Records mouse movements, clicks, and scrolls.
- Collects system information such as hostname, IP address, processor, system type, and machine type.
- Takes screenshots of the desktop.
- Records audio from the microphone (optional).
- Sends logged data via email at regular intervals.
- Resilient against termination attempts through Task Manager.

## Installation

1. Clone or download the KeyTrack repository to your local machine.
2. Install the required Python dependencies using pip:

```bash
pip install -r requirements.txt
```

3. Configure the email address and password in the `watchdog.py` file.

## Usage

1. Run the `watchdog.py` script using Python:

```bash
python watchdog.py
```

2. The keylogger will start capturing keyboard input, mouse events, and system information silently.
3. Logged data will be periodically sent via email to the specified address.

## Configuration

Before using KeyTrack, make sure to configure the following settings:

- Email address: Replace `"your_email@example.com"` with your actual email address.
- Email password: Replace `"your_email_password"` with your email password.
- SMTP server: Replace `'smtp.example.com'` with the SMTP server of your email provider.
- SMTP port: Replace `587` with the port number used by your email provider.

## Disclaimer

KeyTrack is intended for educational and testing purposes only. It should not be used for any illegal or unethical activities. The developers of this project are not responsible for any misuse or damage caused by the use of this software.
Always use keyloggers responsibly and ethically, respecting the privacy and security of others.
