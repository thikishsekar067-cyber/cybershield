from app.services.detection import analyze

def test_ip_url_is_flagged():
 r=analyze('http://192.0.2.1/login','url'); assert r['riskScore']>=25

def test_otp_urgency():
 r=analyze('URGENT! Your account will be blocked. Share OTP now: https://example.test/login','email'); assert r['riskLevel']=='HIGH'

def test_plain_text_is_not_high():
 r=analyze('Remember to update your software regularly.','text'); assert r['riskLevel']=='LOW'
