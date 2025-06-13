# 📬 Smart Post Box Notification System

A smart IoT-based solution that sends **real-time email alerts** when physical mail is detected in a mailbox. Designed using Raspberry Pi Pico W, limit switches, and IR sensors, this project aims to modernize traditional postal experiences with the power of wireless communication and automation.

## 🔧 Features

- Detects arrival of physical mail using **limit switch sensors**
- Sends **email notifications** instantly via Gmail SMTP
- Tracks **individual counters** for multiple users
- **Web server** displays current mail status and counts
- Built using **MicroPython** and **Raspberry Pi Pico W**

## 🖥️ System Architecture

1. Each mailbox is equipped with:
   - A **limit switch** for mail detection
   - A **reset switch** to clear the counter

2. **Microcontroller** (Raspberry Pi Pico W) connects to Wi-Fi and monitors the pins.

3. Upon mail arrival:
   - An email is sent to the corresponding user
   - A counter is incremented

4. A web interface displays the status of each user in real time.

---

## 🧩 Hardware Requirements

- Raspberry Pi Pico W
- Limit switches (x3)
- IR Sensors (optional for extra detection)
- Breadboard and jumper wires
- PCB (optional for compact wiring)
- Power supply or battery
- Soldering tools (if required)

## 🧠 Software Requirements

- MicroPython firmware on Raspberry Pi Pico W
- Python libraries:
  - `network`
  - `usocket`
  - `machine`
  - `_thread`
  - `umail` (for SMTP email)

## 📤 How It Works

- When a postcard is placed, it presses a **limit switch**
- The microcontroller detects this and:
  - Sends an email notification
  - Updates a web-based status server
- A **reset switch** lets the user reset their notification counter


---

## ✉️ Setting Up the Sender Gmail Account (SMTP)

To enable your Raspberry Pi Pico W to send emails via Gmail SMTP, follow these steps:

### 1. Use App Passwords (Highly Recommended)

Google restricts access from less secure apps. To allow email sending from the system:

1. **Enable 2-Step Verification** for your Gmail account.
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Generate a new App Password for “Mail” → “Other (Custom)” (e.g., “Mailbox Guard”)
4. Copy the 16-character app password.

> Use this app password instead of your Gmail password in the code:
> ```python
> SENDER_EMAIL = 'your_email@gmail.com'
> SENDER_PASSWORD = 'your_generated_app_password'
> ```

### 2. Enable IMAP & SMTP in Gmail

- Log in to Gmail → Go to **Settings** → **See all settings**
- Navigate to **Forwarding and POP/IMAP** → Enable **IMAP access**
- Save changes

---

## 🔒 Important Note

Never commit your actual email ID or password (even App Passwords) into public repositories. Use a `.env` file or configuration file (excluded via `.gitignore`) in real-world deployments.

Example:
```python
import config
SENDER_EMAIL = config.email
SENDER_PASSWORD = config.password

