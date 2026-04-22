# CertiChain  
### Blockchain-Based Certificate Issuance and Verification System

---

## Overview

CertiChain is a secure and scalable certificate management system that leverages blockchain technology to ensure authenticity, integrity, and tamper-proof verification of academic and professional certificates.

The system enables administrators to issue certificates individually or in bulk, automatically generate PDF certificates with embedded QR codes, and allow public verification using blockchain-backed hash validation.

---

## Key Features

- Blockchain Integration  
  Stores certificate hashes securely to prevent tampering.

- PDF Certificate Generation  
  Generates professional one-page certificates using ReportLab.

- QR Code Verification  
  Each certificate includes a QR code for instant verification.

- Admin Dashboard  
  Displays real-time statistics such as total certificates issued, success rate, and email status.

- Email Automation  
  Certificates are automatically sent to recipients via email.

- Bulk Certificate Issuance  
  Upload Excel or CSV files to generate multiple certificates.

- Excel Normalization  
  Handles varying column formats automatically.

- Public Verification System  
  Users can verify certificates using hash values or QR code scanning.

---

## System Architecture

User → Flask Web Application → Certificate Generation → Blockchain Hash Storage  
                                           ↓  
                                     Email Delivery  
                                           ↓  
                                QR-Based Verification  

---

## Tech Stack

- Backend: Flask (Python)  
- Database: SQLite3  
- Blockchain: Ganache (Ethereum Local Network)  
- Frontend: HTML, CSS  
- PDF Generation: ReportLab  
- QR Code: qrcode  
- Data Processing: Pandas  

---

## Project Structure

project/  
│  
├── app.py  
├── requirements.txt  
│  
├── templates/  
│   ├── login.html  
│   ├── dashboard.html  
│   ├── issue.html  
│   ├── bulk.html  
│   ├── verify.html  
│  
├── static/  
│   └── css/style.css  
│  
├── blockchain/  
│   └── blockchain.py  
│  
├── database/  
├── certificates/  

---

## Installation and Setup

### 1. Clone the Repository

git clone https://github.com/Kumaran-Thevar/certichain.git  
cd certichain  

---

### 2. Create Virtual Environment (Recommended)

python -m venv venv  
venv\Scripts\activate   (Windows)  

---

### 3. Install Dependencies

pip install -r requirements.txt  

---

### 4. Run the Application

python app.py  

---

### 5. Access the System

http://127.0.0.1:5000  

---

## Bulk Upload Format

Supported formats: .xlsx, .csv  

Required columns:

Name, Course, Department, Email  

Notes:  
- Column order does not matter  
- Column names are case insensitive  

---

## Environment Variables

For email functionality, set the following environment variable:

EMAIL_PASS=your_app_password  

---

## Key Concepts Implemented

- Blockchain-based integrity verification  
- Secure hash generation using SHA-256  
- Automated document generation  
- Data normalization and preprocessing  
- Secure email transmission  

---

## Future Enhancements

- Cloud deployment using platforms such as AWS, Render, or Railway  
- Advanced analytics dashboard  
- Search and filtering functionality  
- Role-based authentication  
- Export reports in PDF or Excel format  

---

## Academic Relevance

This project demonstrates practical implementation of:

- Blockchain in real-world applications  
- Secure data handling  
- Scalable system design  
- Workflow automation  

---

## Author

Kanda Kumaran  
M.Tech (Information Security)
Abhishek 
M.Tech (Information Security)
Shruti
M.Tech (Information Security)
---

## License

This project is developed for academic and research purposes.