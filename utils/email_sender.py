import smtplib
from email.message import EmailMessage

def send_email(receiver, file_path):

    sender = "thevarkandakumaran@gmail.com"
    password = "Kumaranm@2001"

    msg = EmailMessage()
    msg["Subject"] = "Your Certificate"
    msg["From"] = sender
    msg["To"] = receiver

    msg.set_content("Your certificate is attached.")

    with open(file_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename="certificate.pdf")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)