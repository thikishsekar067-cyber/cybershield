from fastapi import APIRouter,UploadFile,File,HTTPException
from pydantic import BaseModel
from app.services.detection import analyze
import io,re
try:
 from PIL import Image
 import pytesseract
except Exception: Image=None
router=APIRouter(prefix='/api/analyze',tags=['analysis'])
class Content(BaseModel): content:str
@router.post('/url')
def url(x:Content):
    if len(x.content)>4096 or not re.match(r'^https?://',x.content.strip(),re.I): raise HTTPException(400,'Please provide a valid http(s) URL.')
    return analyze(x.content,'url')
@router.post('/text')
def text(x:Content):
    if len(x.content)>20000: raise HTTPException(413,'Text is too large.')
    return analyze(x.content,'text')
@router.post('/email')
def email(x:Content):
    if len(x.content)>30000: raise HTTPException(413,'Message is too large.')
    return analyze(x.content,'email')
@router.post('/image')
async def image(file:UploadFile=File(...)):
    if file.content_type not in {'image/png','image/jpeg','image/webp'}: raise HTTPException(415,'Unsupported image type.')
    data=await file.read()
    if len(data)>5*1024*1024: raise HTTPException(413,'Image exceeds 5 MB.')
    if Image is None: raise HTTPException(503,'OCR dependencies unavailable.')
    text=pytesseract.image_to_string(Image.open(io.BytesIO(data)))
    return {'extractedText':text,**analyze(text,'text')}
@router.post('/qr')
async def qr(file:UploadFile=File(...)):
    if file.content_type not in {'image/png','image/jpeg','image/webp'}: raise HTTPException(415,'Unsupported image type.')
    data=await file.read()
    if len(data)>5*1024*1024: raise HTTPException(413,'Image exceeds 5 MB.')
    try:
      import cv2, numpy as np
      img=cv2.imdecode(np.frombuffer(data,np.uint8),cv2.IMREAD_COLOR)
      detector=cv2.QRCodeDetector(); value,_,_=detector.detectAndDecode(img)
    except Exception: value=''
    if not value: raise HTTPException(422,'No QR code could be detected.')
    return {'qrData':value,**analyze(value,'url' if re.match(r'^https?://',value,re.I) else 'text')}
