# from fastapi import FastAPI
# from pydantic import BaseModel
# import base64
# from fastapi.middleware.cors import CORSMiddleware
# import io
# import numpy as np
# import easyocr
# from PIL import Image
# import pytesseract
# app= FastAPI()


# #cors
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],      # Allows ALL IPs (Phone, Laptop, etc.)
#     allow_credentials=False,  # Set to False for wildcard (*)
#     allow_methods=["*"],      # Allows POST, OPTIONS, GET
#     allow_headers=["*"],      # Allows all headers
# )



# reader = easyocr.Reader(['en','hi'],gpu=False)
# class ImageRequest(BaseModel):
#     image_base64:str
# @app.post("/predict")
# def run_ai(request:ImageRequest):
#     base64_input=request.image_base64
#     if "," in base64_input:
#         base64_input =base64_input.split(",")[1]
#     image_bytes=base64.b64decode(base64_input)
#     image=Image.open(io.BytesIO(image_bytes)).convert("RGB")
#     image_np=np.array(image)
#     results= reader.readtext(image_np)
#     clean_results=[]
#     for(bbox,text,prob) in results:
#         box_coords=[[int(p[0]),int(p[1])]for p in bbox]
#         clean_results.append({
#             "text":text,
#             "box":box_coords
#         })
#     return {"data":clean_results}




from fastapi import FastAPI
from pydantic import BaseModel
import base64
from fastapi.middleware.cors import CORSMiddleware
import io
from PIL import Image
import pytesseract

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=False,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# If Tesseract is not in PATH, specify the full path
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class ImageRequest(BaseModel):
    image_base64: str

@app.post("/predict")
def run_ai(request: ImageRequest):
    base64_input = request.image_base64
    if "," in base64_input:
        base64_input = base64_input.split(",")[1]
    
    image_bytes = base64.b64decode(base64_input)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    # OCR using Tesseract
    text = pytesseract.image_to_string(image, lang='eng+hin')  # English + Hindi
    
    # Split into lines for consistent JSON output
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    result = [{"text": line} for line in lines]

    return {"data": result}
