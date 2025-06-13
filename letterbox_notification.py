import network
import usocket as socket
import time
import machine
import ubinascii
import _thread
import sys
from umail import SMTP

# ===================== CONFIGURATION =====================

WIFI_SSID = 'REALMEE'
WIFI_PASSWORD = '1234567889'

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465
SENDER_EMAIL = 'sendergmailid'
SENDER_PASSWORD = 'mimr jddv kinf dlen'
SENDER_DISPLAY_NAME = "Mailbox Guard"

# ✅ DEBUG MODE: Set to True to enable Serial Monitor logs
DEBUG_MODE = True

users = [
    {
        "name": "user1",
        "email": "user1@gmail.com",
        "trigger_pin": 0,
        "reset_pin": 5
    },
    {
        "name": "user2",
        "email": "user2@gmail.com",
        "trigger_pin": 1,
        "reset_pin": 3
    },
    {
        "name": "user3",
        "email": "user3@gmail.com",
        "trigger_pin": 2,
        "reset_pin": 4
    }
]

# ===================== INITIALIZATION =====================

for user in users:
    user["pin_obj"] = machine.Pin(user["trigger_pin"], machine.Pin.IN)
    user["reset_switch"] = machine.Pin(user["reset_pin"], machine.Pin.IN)
    user["email_sent"] = False
    user["counter"] = 0
    user["last_reset_state"] = user["reset_switch"].value()

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    if DEBUG_MODE:
        print("📡 Connecting to WiFi", end="")

    for _ in range(20):
        if wlan.isconnected():
            break
        if DEBUG_MODE:
            print(".", end="")
        time.sleep(1)

    if not wlan.isconnected():
        if DEBUG_MODE:
            print("\n❌ WiFi Connection Failed")
        return None

    if DEBUG_MODE:
        print("\n✅ Connected! IP:", wlan.ifconfig()[0])
    return wlan

def get_timestamp():
    t = time.localtime()
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(*t)

def send_email(recipient_email, recipient_name, count, reset=False):
    try:
        if DEBUG_MODE:
            print(f"📤 Sending email to {recipient_name}...")

        smtp = SMTP(SMTP_SERVER, SMTP_PORT, ssl=True)
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        smtp.to(recipient_email)

        subject = "📬 You've Got Mail!" if not reset else "🔁 Mailbox Counter Reset"
        smtp.write(f"From: {SENDER_DISPLAY_NAME} <{SENDER_EMAIL}>\n")
        smtp.write(f"To: <{recipient_email}>\n")
        smtp.write(f"Subject: {subject}\n")
        smtp.write("Content-Type: text/plain\n\n")

        if not reset:
            body = f"""Hello {recipient_name},

You've got mail! 📬

Time: {get_timestamp()}
Total items received: {count}

- Mailbox Guard"""
        else:
            body = f"""Hello {recipient_name},

The mailbox counter was reset. 🔁

Time: {get_timestamp()}
Count before reset: {count}

- Mailbox Guard"""

        smtp.write(body)
        smtp.send()

        if DEBUG_MODE:
            print("✅ Email sent!")
        return True

    except Exception as e:
        if DEBUG_MODE:
            print("❌ Email error:", e)
        return False

    finally:
        try:
            smtp.quit()
        except:
            pass

def web_server():
    s = socket.socket()
    s.bind(('0.0.0.0', 80))
    s.listen(1)
    if DEBUG_MODE:
        print("🌐 Web server running on port 80")

    while True:
        try:
            conn, addr = s.accept()
            if DEBUG_MODE:
                print(f"🌍 HTTP request from {addr}")

            request = conn.recv(1024)
            if not request:
                conn.close()
                continue

            response = """HTTP/1.1 200 OK
Content-Type: text/html

<html>
<head><title>Mailbox Status</title></head>
<body>
<h1>📫 Mailbox Notifications</h1>"""

            for user in users:
                response += f"<p>{user['name']}: {user['counter']} notifications</p>"

            response += "</body></html>"

            conn.send(response.encode())
            conn.close()
        except Exception as e:
            if DEBUG_MODE:
                print("❌ Web server error:", str(e))

def main():
    if DEBUG_MODE:
        print("📦 Starting Mail Detection System...")

    wlan = connect_wifi()

    if wlan is None:
        if DEBUG_MODE:
            print("Retrying WiFi in 10 seconds...")
        time.sleep(10)
        machine.reset()

    _thread.start_new_thread(web_server, ())

    if DEBUG_MODE:
        print("🟢 System ready. Monitoring...")

    while True:
        for user in users:
            pin_val = user["pin_obj"].value()
            reset_val = user["reset_switch"].value()

            if pin_val == 0 and not user["email_sent"]:
                user["counter"] += 1
                if send_email(user["email"], user["name"], user["counter"]):
                    user["email_sent"] = True
                    if DEBUG_MODE:
                        print(f"📨 Mail detected for {user['name']} (#{user['counter']})")
                else:
                    if DEBUG_MODE:
                        print("⏳ Retrying email in 5s...")
                    time.sleep(5)

            elif pin_val == 1:
                user["email_sent"] = False

            current_reset_val = user["reset_switch"].value()
            if current_reset_val != user["last_reset_state"]:
                if DEBUG_MODE:
                    print(f"🔁 Reset triggered for {user['name']}")
                send_email(user["email"], user["name"], user["counter"], reset=True)
                user["counter"] = 0
                user["last_reset_state"] = current_reset_val
                time.sleep(0.5)

        time.sleep(0.1)

if _name_ == "_main_":
    try:
        main()
    except Exception as e:
        if DEBUG_MODE:
            print("❗ Fatal error:", str(e))
        sys.print_exception(e)
        time.sleep(10)
        machine.reset() based on this code  and report create an image block digram to unerstand the project 