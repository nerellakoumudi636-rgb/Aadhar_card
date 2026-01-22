# Aadhar_card

This is a Python based OCR project used to extract important details from Aadhaar card images.

Project Overview

This project uses Tesseract OCR and PaddleOCR to extract the following information from Aadhaar card images.

Name
Date of Birth
Gender
Aadhaar Number

Technologies Used

opencv python for image preprocessing
pytesseract for text extraction using Tesseract OCR
paddleocr for accurate text recognition
paddlepaddle as backend framework for PaddleOCR
numpy for numerical operations
Pillow for image handling
regex for pattern matching and field extraction
create the env
Project Structure

input images folder contains Aadhaar card images
aadhaar_outputs folder contains extracted JSON files
aadhaar_ocr.py is the main Python script
requirements.txt contains required dependencies

Prerequisites

Python version 3.10.4
Tesseract OCR installed on the system


Tesseract path is requried the code.

Installation

Install required Python packages using
pip install -r requirements.txt

Requirements.txt content

opencv python
pytesseract
paddleocr
paddlepaddle
numpy
Pillow
regex

