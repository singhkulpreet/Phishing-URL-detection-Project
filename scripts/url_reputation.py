# url_reputation.py
import os, requests

VT_API=os.getenv('Place VIRUSTOTAL API KEY HERE ')
VT_BASE='https://www.virustotal.com/api/v3'
headers={'x-apikey':VT_API} if VT_API else {}

def vt_lookup_url(url):
    if not VT_API:
        return {'url':url,'source':'local','malicious':None,'notes':'VT_API not configured'}
    res=requests.post(f'{VT_BASE}/urls',headers=headers,data={'url':url})
    if res.status_code not in (200,201):
        return {'url':url,'source':'vt','error':res.text}
    jt=res.json(); analysis_id=jt['data']['id']
    r2=requests.get(f'{VT_BASE}/analyses/{analysis_id}',headers=headers)
    return {'url':url,'source':'vt','analysis':r2.json()}

if __name__=='__main__':
    import sys,json
    print(json.dumps(vt_lookup_url(sys.argv[1]),indent=2))
