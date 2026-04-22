from flask import Flask, render_template, request, redirect, session, send_from_directory
import sqlite3, os, hashlib, datetime
import qrcode, smtplib
import pandas as pd
from email.message import EmailMessage

from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from blockchain.blockchain import store_hash, verify_hash

app = Flask(__name__)
app.secret_key = "super_secret_key"

DB_PATH = "database/db.sqlite3"

# ---------------- DATABASE ----------------
def connect_db():
    return sqlite3.connect(DB_PATH)

def create_tables():
    if not os.path.exists("database"):
        os.makedirs("database")

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS certificates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        course TEXT,
        department TEXT,
        email TEXT,
        cert_hash TEXT,
        issued_at TEXT,
        email_status TEXT
    )
    """)

    conn.commit()
    conn.close()

create_tables()

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["email"] == "admin@gmail.com" and request.form["password"] == "admin123":
            session["admin"] = "admin"
            return redirect("/dashboard")
    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect("/")

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM certificates")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM certificates WHERE email_status='Sent'")
    sent = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM certificates WHERE email_status='Failed'")
    failed = cur.fetchone()[0]

    success_rate = (sent / total * 100) if total > 0 else 0

    cur.execute("SELECT name, course, issued_at, email_status FROM certificates ORDER BY id DESC")
    recent = cur.fetchall()

    conn.close()

    return render_template("dashboard.html",
                           total=total,
                           sent=sent,
                           failed=failed,
                           success_rate=round(success_rate, 2),
                           recent=recent)

# ---------------- DOWNLOAD ----------------
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('certificates', filename)

# ---------------- EMAIL ----------------
def send_email(receiver, file_path):
    sender = "thevarkandakumaran@gmail.com"
    password = "aeaeettuyqbwwduf"


    if not password:
        raise Exception("EMAIL_PASS not set")

    msg = EmailMessage()
    msg["Subject"] = "Your Certificate"
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content("Certificate attached. Scan QR to verify.")

    with open(file_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename="certificate.pdf")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

# ---------------- CERTIFICATE ----------------
def generate_certificate(name, course, department, cert_hash, issued_at):

    if not os.path.exists("certificates"):
        os.makedirs("certificates")

    safe_name = name.replace(" ", "_")
    filename = f"certificates/{safe_name}.pdf"

    doc = SimpleDocTemplate(filename, pagesize=landscape(A4), topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<para align='center'><font size=26><b>CERTIFICATE OF COMPLETION</b></font></para>", styles["Normal"]))
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("<para align='center'>This is to certify that</para>", styles["Normal"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"<para align='center'><b>{name}</b></para>", styles["Normal"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("<para align='center'>has successfully completed</para>", styles["Normal"]))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph(f"<para align='center'><b>{course}</b></para>", styles["Normal"]))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph(f"<para align='center'>Department of {department}</para>", styles["Normal"]))
    elements.append(Spacer(1, 15))

    table = Table([
        ["Hash", cert_hash[:25] + "..."],
        ["Issued", issued_at]
    ])
    table.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.grey)]))
    elements.append(table)
    elements.append(Spacer(1, 10))

    verify_url = f"http://127.0.0.1:5000/verify?hash={cert_hash}"
    qr = qrcode.make(verify_url)
    qr_path = f"certificates/{safe_name}_qr.png"
    qr.save(qr_path)

    elements.append(Image(qr_path, width=80, height=80))
    elements.append(Spacer(1, 10))

    elements.append(Table([
        ["__________________", "__________________"],
        ["Authorized Signatory", "Director"]
    ]))

    doc.build(elements)
    return filename

# ---------------- ISSUE ----------------
@app.route("/issue", methods=["GET", "POST"])
def issue():
    if "admin" not in session:
        return redirect("/")

    if request.method == "POST":
        name = request.form["name"]
        course = request.form["course"]
        department = request.form["department"]
        email = request.form["email"]

        issued_at = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        cert_hash = hashlib.sha256((name+course+department+email+issued_at).encode()).hexdigest()

        store_hash(cert_hash)

        pdf_path = generate_certificate(name, course, department, cert_hash, issued_at)

        try:
            send_email(email, pdf_path)
            status = "Sent"
        except:
            status = "Failed"

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO certificates (name, course, department, email, cert_hash, issued_at, email_status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, course, department, email, cert_hash, issued_at, status))
        conn.commit()
        conn.close()

        return render_template("issue.html", success=True, hash=cert_hash, time=issued_at, pdf=pdf_path, email_status=status)

    return render_template("issue.html")

# ---------------- BULK ----------------
@app.route("/bulk", methods=["GET", "POST"])
def bulk():
    if "admin" not in session:
        return redirect("/")

    if request.method == "POST":
        file = request.files["file"]

        if file.filename.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        df.columns = df.columns.str.lower()

        results = []

        for _, row in df.iterrows():
            name = str(row["name"])
            course = str(row["course"])
            department = str(row["department"])
            email = str(row["email"])

            issued_at = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            cert_hash = hashlib.sha256((name+course+department+email+issued_at).encode()).hexdigest()

            store_hash(cert_hash)
            pdf_path = generate_certificate(name, course, department, cert_hash, issued_at)

            try:
                send_email(email, pdf_path)
                status = "Sent"
            except:
                status = "Failed"

            conn = connect_db()
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO certificates (name, course, department, email, cert_hash, issued_at, email_status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, course, department, email, cert_hash, issued_at, status))
            conn.commit()
            conn.close()

            results.append((name, status))

        return render_template("bulk.html", results=results)

    return render_template("bulk.html")

# ---------------- VERIFY ----------------
@app.route("/verify", methods=["GET", "POST"])
def verify():
    result = None
    cert_hash = request.args.get("hash")

    if cert_hash:
        result = verify_hash(cert_hash)
    elif request.method == "POST":
        result = verify_hash(request.form["hash"])

    return render_template("verify.html", result=result)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)