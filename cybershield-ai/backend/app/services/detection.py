from urllib.parse import urlparse
import re, ipaddress
SUSPICIOUS_TLDS={'zip','click','top','xyz','work','support','country','gq','tk'}
URGENCY=re.compile(r'\b(urgent|immediately|act now|within \d+ hours?|account will be blocked|last warning)\b',re.I)
CREDENTIAL=re.compile(r'\b(otp|one[- ]time password|upi pin|cvv|password|pin|login|verify your account)\b',re.I)
PAYMENT=re.compile(r'\b(pay|payment|transfer|refund|fee|deposit|upi|bank account)\b',re.I)

def urls(text): return re.findall(r'https?://[^\s<>\"\']+',text)
def score_url(u):
    reasons=[]; score=0
    try:
        p=urlparse(u)
        if p.scheme!='https': score+=10; reasons.append('The URL does not use HTTPS.')
        host=p.hostname or ''
        try: ipaddress.ip_address(host); score+=15; reasons.append('The URL uses an IP address instead of a normal domain.')
        except ValueError: pass
        if host.startswith('xn--') or '.xn--' in host: score+=20; reasons.append('The domain contains punycode, which can be used for look-alike domains.')
        tld=host.rsplit('.',1)[-1].lower() if '.' in host else ''
        if tld in SUSPICIOUS_TLDS: score+=12; reasons.append(f'The top-level domain .{tld} has elevated abuse risk in this heuristic.')
        if len(host)>45: score+=8; reasons.append('The hostname is unusually long.')
        if host.count('.')>=4: score+=8; reasons.append('The hostname has many subdomain levels.')
        if '@' in p.netloc: score+=20; reasons.append('The URL contains an @ character that can obscure the actual destination.')
        if p.port: score+=10; reasons.append('The URL uses a non-default port.')
        if any(x in (p.query or '').lower() for x in ['redirect=','url=','next=','return=']): score+=12; reasons.append('The URL contains redirect-like parameters.')
        if any(x in host.lower() for x in ['login','verify','secure','account','update']): score+=5; reasons.append('The hostname uses credential-themed words; verify the organization independently.')
    except Exception: score=60; reasons.append('The URL could not be parsed reliably.')
    return min(score,100),reasons

def analyze(text,kind='text'):
    reasons=[]; score=0
    if kind=='url':
        score,reasons=score_url(text.strip())
    else:
        us=urls(text)
        for u in us:
            s,r=score_url(u); score=max(score,s); reasons.extend(r)
        if URGENCY.search(text): score+=10; reasons.append('The message uses urgency or threat language.')
        if CREDENTIAL.search(text): score+=20; reasons.append('The message references credentials, OTPs, PINs or account verification.')
        if PAYMENT.search(text): score+=15; reasons.append('The message contains payment or money-transfer language.')
        if not us and kind=='email': reasons.append('No URL was detected; sender identity still needs independent verification.')
    score=min(score,100)
    level='HIGH' if score>=65 else 'MEDIUM' if score>=30 else 'LOW'
    cls='LIKELY_PHISHING' if level=='HIGH' else 'SUSPICIOUS_NEEDS_VERIFICATION' if level=='MEDIUM' else 'LIKELY_LEGITIMATE'
    if not reasons: reasons=['No high-risk heuristic indicators were detected in the submitted content.']
    actions=['Do not click suspicious links.','Verify the claimed organization through its official website or known contact channel.'] if level!='LOW' else ['Continue to verify important requests independently.','Do not disclose confidential credentials.']
    if level=='HIGH': actions+=['Do not provide OTPs, UPI PINs, passwords or card details.','If money was lost, contact your bank/payment provider and report promptly through official cybercrime channels.']
    return {'riskLevel':level,'riskScore':score,'confidence':'HIGH' if len(reasons)>=2 else 'MEDIUM','classification':cls,'summary':'This content contains indicators associated with phishing or scams.' if level!='LOW' else 'This appears legitimate based on the indicators we could verify.','indicators':list(dict.fromkeys(reasons))[:8],'explanation':'The score combines deterministic signals. Optional AI/threat-intelligence adapters can add context, but neither can guarantee safety.','recommendedActions':actions}
