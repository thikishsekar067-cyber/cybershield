from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    database_url:str='mysql+pymysql://root:password@localhost:3306/cybershield'
    auth_secret:str='change-me'
    ai_api_key:str=''
    threat_intelligence_api_key:str=''
    ocr_api_key:str=''
    frontend_origin:str='http://localhost:3000'
    class Config: env_file='.env'
settings=Settings()
OFFICIAL_RESOURCES=[
 {'name':'National Cyber Crime Reporting Portal','url':'https://www.cybercrime.gov.in/','purpose':'Report cybercrime and suspicious identifiers'},
 {'name':'RBI Complaint Management System','url':'https://cms.rbi.org.in/','purpose':'Complaints against RBI-regulated entities'},
 {'name':'CERT-In','url':'https://www.cert-in.org.in/','purpose':'Indian national cybersecurity incident response and advisories'},
 {'name':'Emergency Police','url':'tel:112','purpose':'Emergency police assistance'},
 {'name':'Cybercrime Helpline','url':'tel:1930','purpose':'Immediate reporting of online financial fraud'},
]
