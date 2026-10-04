from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.analyze import router
from app.core.config import settings,OFFICIAL_RESOURCES
app=FastAPI(title='Cyber Shield AI API',version='1.0.0')
app.add_middleware(CORSMiddleware,allow_origins=[settings.frontend_origin],allow_credentials=True,allow_methods=['GET','POST','DELETE'],allow_headers=['*'])
app.include_router(router)
@app.get('/health')
def health(): return {'status':'ok','service':'cybershield-ai'}
@app.get('/api/resources')
def resources(): return OFFICIAL_RESOURCES
@app.get('/api/helplines')
def helplines(): return [{'name':'Cybercrime Helpline','number':'1930','purpose':'Online financial fraud reporting','action':'tel:1930'},{'name':'Emergency Police','number':'112','purpose':'Emergency police assistance','action':'tel:112'}]
@app.get('/api/articles')
def articles(): return [{'slug':'phishing','title':'Phishing','summary':'Pause, inspect the sender and verify the destination independently.'},{'slug':'upi-safety','title':'UPI Safety','summary':'Never share a UPI PIN to receive money.'},{'slug':'qr-safety','title':'QR Code Safety','summary':'Inspect QR destinations before opening or paying.'}]
