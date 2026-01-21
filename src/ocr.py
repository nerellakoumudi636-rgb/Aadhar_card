import cv2
import pytesseract
import re
import os
import json
import warnings
from paddleocr import PaddleOCR

# -------------------------------------------------
# SUPPRESS WARNINGS (OPTIONAL)
# -------------------------------------------------
warnings.filterwarnings("ignore")

# -------------------------------------------------
# TESSERACT PATH (WINDOWS)
# -------------------------------------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# -------------------------------------------------
# INIT PADDLE OCR (LATEST COMPATIBLE)
# -------------------------------------------------
ocr = PaddleOCR(
    lang="en",
    use_textline_orientation=True
)

# -------------------------------------------------
# TESSERACT OCR
# -------------------------------------------------
def extract_text_tesseract(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(" Image not found")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    config = r"--oem 3 --psm 6"
    text = pytesseract.image_to_string(gray, config=config)
    return text

# -------------------------------------------------
# PADDLE OCR (FIXED FOR NEW API)
# -------------------------------------------------
def extract_text_paddle(image_path):
    result = ocr.ocr(image_path)

    text = ""
    for page in result:
        for line in page:
            text += line[1][0] + "\n"

    return text


# -------------------------------------------------
# AADHAAR FIELD EXTRACTION
# -------------------------------------------------
def extract_aadhaar_fields(text):
    data = {
        "Name": "",
        "DOB": "",
        "Gender": "",
        "Aadhaar Number": ""
    }

    lines = [l.strip() for l in text.split("\n") if l.strip()]
    text_upper = text.upper()

    # -------------------------
    # Aadhaar Number
    # -------------------------
    aadhaar = re.search(r"\b\d{4}\s?\d{4}\s?\d{4}\b", text_upper)
    if aadhaar:
        data["Aadhaar Number"] = aadhaar.group()

    # -------------------------
    # DOB
    # -------------------------
    dob_match = re.search(
        r"(DOB|DATE OF BIRTH)[:\s]*([0-9]{2}[/-][0-9]{2}[/-][0-9]{4})",
        text_upper
    )
    if dob_match:
        data["DOB"] = dob_match.group(2)

    # -------------------------
    # Gender
    # -------------------------
    gender = re.search(r"\b(MALE|FEMALE|TRANSGENDER)\b", text_upper)
    if gender:
        data["Gender"] = gender.group().capitalize()

    # -------------------------
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

    return data

# -------------------------------------------------
# MAIN
# -------------------------------------------------
def main():
    image_path = r"C:\Users\HP\Desktop\ocr\input images\aadhar4.jpeg"
    output_path = r"C:\Users\HP\Desktop\ocr\aadhaar_output.json"

    if not os.path.exists(image_path):
        print(" Image path not found")
        return

    print("\n Reading Aadhaar Image...\n")

    # OCR
    tess_text = extract_text_tesseract(image_path)
    paddle_text = extract_text_paddle(image_path)

    print(" Paddle OCR Text:\n", paddle_text)
    print(" Tesseract OCR Text:\n", tess_text)

    # Combine OCR results
    combined_text = tess_text + "\n" + paddle_text

    # Extract fields
    data = extract_aadhaar_fields(combined_text)

    print("\n Extracted Aadhaar Details:\n")
    print(json.dumps(data, indent=4))

    # Save JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"\n JSON saved at: {output_path}")

# -------------------------------------------------
# RUN
# -------------------------------------------------
if __name__ == "__main__":

    main()
