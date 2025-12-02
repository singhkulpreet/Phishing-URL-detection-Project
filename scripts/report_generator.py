# report_generator.py

from parse_eml import parse_eml
from url_reputation import vt_lookup_url
from sandbox_submit import submit_file_to_vt 
from qradar_ioc_push import push_ioc_list   # <-- IMPORT HERE


def generate_md_report(parsed, vt_results, sandbox_results, out_path='report.md'):
    lines=[]
    lines.append("# Phishing Investigation Report")
    lines.append("")
    lines.append(f"**Subject:** {parsed.get('subject')}")
    lines.append(f"**From:** {parsed.get('from')}")
    lines.append(f"**Date:** {parsed.get('date')}")
    lines.append("")
    lines.append("## Extracted URLs")
    for u in parsed.get('urls',[]):
        lines.append(f"- {u} — VT: {vt_results.get(u,'n/a')}")
    lines.append("")
    lines.append("## Attachments")
    for a in parsed.get('attachments',[]):
        lines.append(f"- {a['filename']} — sha256: {a['sha256']}")
        lines.append(f"  - sandbox: {sandbox_results.get(a['sha256'],'n/a')}")
    with open(out_path,'w') as f:
        f.write("\n".join(lines))
    return out_path



# 1. Parse the email
parsed = parse_eml("incoming_emails/sample_phish.eml")

# 2. VT results for URLs (dict)
vt_results = {
    url: vt_lookup_url(url)
    for url in parsed.get("urls", [])
}

# 3. Sandbox results for attachments
sandbox_results = {}
for att in parsed.get("attachments", []):
    with open(att["path"], "rb") as f:
        file_bytes = f.read()

    sandbox_results[att["sha256"]] = submit_file_to_vt(file_bytes, att["filename"])



# ------------------------------------------------
# 4. COLLECT IOCs TO SEND TO QRADAR
# ------------------------------------------------
ioc_list = []

ioc_list.extend(parsed.get("urls", []))     # URLs
ioc_list.extend([att["sha256"] for att in parsed["attachments"]])  # Attachment hashes

# OPTIONAL: Extract sender email as IOC
if parsed.get("from"):
    ioc_list.append(parsed["from"])

# OPTIONAL: Subject as IOC (useful for phishing campaigns)
if parsed.get("subject"):
    ioc_list.append(parsed["subject"])


# 5. Push IOCs into QRadar
push_ioc_list(ioc_list)




# 6. Generate report
output_file = generate_md_report(
    parsed,
    vt_results,
    sandbox_results,
    out_path="output/phishing_report.md"
)

print("Report generated:", output_file)
