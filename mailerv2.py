import smtplib
import sys
import time
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# ===== COLORS =====
G = '\033[1;32m'
B = '\033[1;34m'
Y = '\033[1;33m'
C = '\033[1;36m'
W = '\033[1;37m'
R = '\033[1;31m'

def slow_print(text):
    for c in text + "\n":
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.01)

# ===== BIRD ASCII THEME =====
banner = f"""
{G}
                   _.:._
                 .\"\\ | /\".
{B}.,__            \"=.\:/.=\"            __,.
{Y} \"=.`\"=._          /^\          _.=\"`.=\" 
{C}   \".'.'.\"=.=.=.=.     .'.'.'.'.'.'.\""
{G}     `~.`.`.`.`.`.`.   .'.'.'.'.'.~`
{B}        `~.` ` `.`.`   .'.'.'.'.~`
{C}            `=.-~~-._ ) ( _.-~~-.=`
{Y}                    \\ /
{G}                     ( )
{B}                      Y

=====================================
        SMTP MAIL SENDER TOOL
             Bird Edition 🐦
=====================================
"""

print("\033[H\033[J")
print(banner)
slow_print(G + "[+] Bird Mail System Loaded...\n")

# ===== INPUTS =====
smtp_server = input(G + "SMTP Server (smtp.gmail.com): " + Y)
smtp_port = int(input(G + "SMTP Port (587): " + Y))

email = input(G + "Your Email: " + Y)
password = input(G + "App Password: " + Y).replace(" ", "")

to = input(G + "Send To: " + Y)
subject = input(G + "Subject: " + Y)
message = input(G + "Message: " + Y)

priority = input(G + "Make HIGH PRIORITY? (y/n): " + Y).lower()

# ===== HTML (YELLOW WARNING STYLE) =====
if priority == "y":
    html_body = f"""
    <html>
    <body style="font-family:Arial;background-color:#fff7b2;padding:20px;">

    <div style="background:#ffcc00;color:black;padding:15px;
                border-left:10px solid orange;font-size:18px;font-weight:bold;">
        ⚠️ BE CAREFUL WITH THIS MESSAGE ⚠️
    </div>

    <br>

    <div style="background:white;padding:15px;border:1px solid #ddd;">
        <h2>IMPORTANT MESSAGE</h2>
        <p>{message}</p>
    </div>

    <br>
    <small>🐦 Sent via Bird SMTP Mailer</small>

    </body>
    </html>
    """
    msg_subject = "⚠️ IMPORTANT: " + subject
else:
    html_body = f"""
    <html>
    <body style="font-family:Arial;padding:20px;">
        <h3>🐦 {subject}</h3>
        <p>{message}</p>
    </body>
    </html>
    """
    msg_subject = subject

# ===== EMAIL BUILD =====
msg = MIMEMultipart("alternative")
msg["From"] = email
msg["To"] = to
msg["Subject"] = msg_subject

msg.attach(MIMEText(html_body, "html"))

# ===== ATTACHMENT =====
file_path = input(G + "Attach file (ENTER to skip): " + Y)

if file_path:
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(file_path)}"
        )

        msg.attach(part)
        slow_print(C + "[+] File attached 🐦")
    else:
        slow_print(R + "[!] File not found")

# ===== SEND EMAIL =====
try:
    slow_print(C + "\n[+] Connecting SMTP...")
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    slow_print(C + "[+] Logging in...")
    server.login(email, password)

    slow_print(C + "[+] Sending email...")
    server.send_message(msg)
    server.quit()

    slow_print(G + "[SUCCESS] Email sent 🐦")

except Exception as e:
    slow_print(R + "[ERROR] Failed")
    print(R + str(e))

slow_print(W + "Done.")
