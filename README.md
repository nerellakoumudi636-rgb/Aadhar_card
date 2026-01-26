Aadhaar Card OCR Extraction using Tesseract and PaddleOCR   
Project Description

This project extracts key information from Aadhaar card images using Optical Character Recognition (OCR).
It combines Tesseract OCR and PaddleOCR to improve text recognition accuracy and stores the extracted details in a structured JSON format.

Features

Extracts important Aadhaar details:
Name
Date of Birth (DOB)
Gender
Aadhaar Number
Uses two OCR engines (Tesseract + PaddleOCR) for better accuracy
Image preprocessing using OpenCV
Regex-based field extraction
Saves extracted output in JSON format

Technologies Used

Python 3.10.4 – Core programming language
OpenCV (opencv-python) – Image preprocessing (grayscale, resizing, thresholding)
PyTesseract – Python wrapper for Tesseract OCR engine
PaddleOCR – Deep learning–based OCR for accurate text recognition
PaddlePaddle – Backend framework used by PaddleOCR
NumPy – Numerical operations and image array processing
Pillow (PIL) – Image handling and format support
Regex (Regular Expressions) – Pattern matching for Name, DOB, Gender, Aadhaar Number
warnings – Suppresses unnecessary runtime warnings for cleaner output

Environment Setup

Create Virtual Environment
python -m venv venv
venv\Scripts\activate

Install Required Libraries

pip install -r requirements.txt
Required Packages
opencv-python
pytesseract
paddleocr
paddlepaddle
numpy
Pillow
regex (re)

Tesseract OCR Installation & Path Setup
Install Tesseract OCR (Windows)
Tesseract OCR must be installed separately.
Official Tesseract OCR Download:
[https://github.com/UB-Mannheim/tesseract/wiki](url)
Recommended version: tesseract-ocr-w64-setup-5.x.x.exe

Configure Tesseract Path in Python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

Use of warnings Module

OCR libraries such as PaddleOCR and PaddlePaddle may generate multiple runtime warnings (deprecation, performance, backend warnings).
To keep the console output clean, the warnings module is used.
Why warnings is used:
Suppresses non-critical warnings
Improves log readability
Helps focus on actual OCR output and errors

Code Example:
import warnings
warnings.filterwarnings("ignore")

OCR Workflow

Aadhaar card image is preprocessed using OpenCV
Text is extracted using Tesseract OCR and PaddleOCR
Combined OCR output is cleaned and normalized
Regex patterns extract Aadhaar fields
Final extracted data is saved in JSON format

Name Field Extraction Logic (Improved Aadhaar Logic)

Aadhaar cards often do not explicitly label the Name field.
A rule-based filtering approach is used to identify the most likely name.

Logic Explanation

OCR output is split into individual lines
Each line is cleaned using regex to keep only uppercase alphabets and spaces
A blacklist removes government and metadata text
Lines containing 2–4 words are considered valid name candidates
The first valid candidate is selected (usually appears near the top)

# Name (Improved Aadhaar Logic)
# -------------------------
blacklist = [
    "GOVERNMENT", "INDIA", "DOB", "DATE", "BIRTH",
    "MALE", "FEMALE", "TRANSGENDER",
    "AADHAAR", "UIDAI", "YEAR", "OF"
]

name_candidates = []

for line in lines:
    clean = re.sub(r"[^A-Z\s]", "", line.upper())
    words = clean.split()

    if (
        2 <= len(words) <= 4
        and not any(word in blacklist for word in words)
    ):
        name_candidates.append(" ".join(words))
# Pick the first valid name (usually appears near top)
if name_candidates:
    data["Name"] = name_candidates[0].title()

    Output Format (Sample)
    {
  "Name": "KUMAR",
  "DOB": "12/05/1996",
  "Gender": "Male",
  "AadhaarNumber": "1234 5678 9012"
}


Drawbacks / Limitations

OCR accuracy depends on image quality
Handwritten Aadhaar cards are not supported
Low-resolution or blurred images reduce accuracy
Names with more than 4 words may be ignored
OCR misrecognition can affect regex-based extraction

Conclusion

This project demonstrates a practical Aadhaar OCR pipeline using both traditional and deep learning–based OCR engines.



    


