# sandbox_submit.py
import os, requests
from parse_eml import parse_eml

VT_API = os.getenv('VT_API')
VT_BASE = 'https://www.virustotal.com/api/v3'
headers = {'x-apikey': VT_API} if VT_API else {}


def submit_file_to_vt(file_bytes, filename):
    if not VT_API:
        return {'error': 'VT_API not configured for sandbox'}
    files = {'file': (filename, file_bytes)}
    r = requests.post(f'{VT_BASE}/files', headers=headers, files=files)
    if r.status_code not in (200, 201):
        return {'error': r.text}
    return r.json()

# 1. Read file bytes
with open("incoming_emails/sample_phish.eml", "rb") as f:
    file_bytes = f.read()

# 2. Call the function
output = submit_file_to_vt(file_bytes, "sample_phish.eml")

# 3. Print output
print("FUNCTION OUTPUT:", output)