# Phishing Email Analysis & URL Reputation Automation Project

## 📌 Project Overview
This project simulates a **real SOC L1 phishing investigation workflow**, covering everything from collecting a phishing email to automated URL reputation checks and SIEM correlation in QRadar.

The goal is to demonstrate:
- How SOC teams analyze phishing emails
- How to extract URLs, headers, attachments
- How to automate URL reputation (VirusTotal)
- How to submit attachments to sandbox
- How to generate an investigation report
- How to detect phishing using QRadar correlation rules

This project is fully hands‑on and replicates real SOC responsibilities.

---

# 🧩 Project Components
The project includes:

### ✔️ 1. Phishing Email Collection
- Raw `.eml` sample stored in `incoming_emails/`
- Contains phishing indicators

### ✔️ 2. Python Automation Scripts
Four Python scripts automate the investigation:

#### **1. parse_eml.py**
- Extracts email headers (From, To, Subject)
- Extracts URLs from the body
- Extracts attachments
- Saves extracted data to JSON

#### **2. url_reputation.py**
- Takes URLs collected from `parse_eml.py`
- Checks reputation using VirusTotal API
- Outputs malicious/clean/detected categories

#### **3. sandbox_submit.py**
- Extracts attachments from email
- Submits them to VirusTotal sandbox API
- Prints analysis ID

#### **4. report_generator.py**
- Combines results from all stages
- Generates a Markdown investigation report
- Simulates SOC report format

### ✔️ 3. QRadar SIEM Integration
The project simulates a real SIEM detection pipeline:
- Add malicious URLs into QRadar Reference Set (`phishing_urls`)
- Create Correlation Rule:

```
When event category = DNS/HTTP
AND domain/URL contains value from reference set phishing_urls
Then create offense: "User contacted known phishing URL"
```

This represents SOC automation.

---

# 🛠️ Project Folder Structure
```
phishing_project/
│── scripts/
│   ├── parse_eml.py
│   ├── url_reputation.py
│   ├── sandbox_submit.py
│   └── report_generator.py
│
│── incoming_emails/
│   └── sample_phish.eml
│
│── output/
│   ├── parsed_email.json
│   ├── malicious-link.json
│   └── investigation_report.md
│
│── README.md
```

---

# 🚀 Step-by-Step Execution Guide

## 🔹 Step 1 — Parse the Phishing Email
```
python scripts/parse_eml.py incoming_emails/sample_phish.eml
```
Output → `results/parsed_email.json`

Contents include:
- Extracted URLs
- Sender
- Subject
- Email body summary

---

## 🔹 Step 2 — Run URL Reputation Check
```
python scripts/url_reputation.py results/parsed_email.json
```
Output → `results/url_reputation.json`

Shows:
- Is the URL malicious?
- Confidence score
- VT detection categories

---

## 🔹 Step 3 — Submit Attachment to Sandbox
```
python scripts/sandbox_submit.py incoming_emails/sample_phish.eml
```
Output → Printed in terminal

You can optionally save it as JSON.

---

## 🔹 Step 4 — Generate Final Report
```
python scripts/report_generator.py
```
Output → `results/investigation_report.md`

Contains:
- Incident summary
- URLs found
- Reputation findings
- Sandbox results
- Analyst recommendation

This is a **real SOC-style report**.

---

# 🛡️ QRadar SIEM Correlation Rule
### 🔹 Create Reference Set: `phishing_urls`
Populate with malicious domains:
```
phish-login365.net
update-payments-secure.com
fake-amazon-alerts.org
```

### 🔹 Correlation Rule Logic
```
When Event Category is DNS or HTTP
AND URL/Domain contains any value from reference set phishing_urls
Then Create Offense “User contacted known phishing URL”
Set Severity: High
```

### 🔹 What QRadar Reads Internally
QRadar parses:
- URL
- Hostname
- DNS Query
- URI

If any match the reference set → Offense triggered.

This simulates a real detection pipeline.

---

### DNS test
```
nslookup fake-phishing-test.com
```

Logs are captured → forwarded to QRadar → rule fires.

---

# 📄 Use This in Your Resume
### **Project Title:**
**Phishing Email Analysis & URL Reputation Automation (SOC Project)**

### Highlights:
- Built end-to-end phishing investigation workflow
- Automated URL scanning using VirusTotal API
- Performed attachment sandbox analysis
- Integrated phishing detection using QRadar correlation rules
- Created SOC-style investigation report


---

# 🏁 Final Deliverables
You now have:
- A working phishing investigation toolset
- A full SIEM detection pipeline in QRadar
- Python automation scripts
- SOC reporting format
