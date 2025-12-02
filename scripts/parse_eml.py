# parse_eml.py
import os, hashlib, re
from bs4 import BeautifulSoup
from eml_parser import EmlParser


URL_REGEX = re.compile(r'https?://[\w\-\./?&=%#]+')

def hash_bytes(b, alg='sha256'):
    h = hashlib.new(alg); h.update(b); return h.hexdigest()

def parse_eml(path):
    # Read raw email
    with open(path, "rb") as f:
        raw_email = f.read()

    parser = EmlParser(include_raw_body=True, include_attachment_data=True)
    data = parser.decode_email_bytes(raw_email)

    # Extract basic fields
    headers = data.get("header", {})
    subject = headers.get("subject", "")
    date = headers.get("date", "")
    from_ = headers.get("from", "")
    to = headers.get("to", "")

    # Extract body text + HTML
    body = ""
    html = ""
    if "body" in data:
        for part in data["body"]:
            if part.get("content_type") == "text/plain":
                body += part.get("content", "")
            elif part.get("content_type") == "text/html":
                html += part.get("content", "")

    # Extract URLs via regex
    urls = set(URL_REGEX.findall(body + "\n" + html))

    # Extract URLs from HTML using BeautifulSoup
    if html:
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", href=True):
            urls.add(a["href"])

    # Extract attachments
    attachments = []
    for att in data.get("attachment", []):
        filename = att.get("filename", "unknown")
        content = att.get("payload", b"")

        if not isinstance(content, bytes):
            content = content.encode("utf-8", errors="ignore")

        sha256 = hash_bytes(content)

        attachments.append({
            "filename": filename,
            "sha256": sha256,
            "size": len(content)
        })

    return {
        "path": path,
        "headers": headers,
        "from": from_,
        "to": to,
        "subject": subject,
        "date": date,
        "urls": list(urls),
        "attachments": attachments
    }
    
    
if __name__=='__main__':
    import json, sys
    p=sys.argv[1]
    print(json.dumps(parse_eml(p),indent=2,default=str))
