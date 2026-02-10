import pytesseract
from pdf2image import convert_from_path
import os
from PIL import Image

# Configurer le chemin de Tesseract et Poppler
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\Users\JP\AppData\Local\Microsoft\WinGet\Packages\oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe\poppler-25.07.0\Library\bin"
os.environ['TESSDATA_PREFIX'] = r"c:\Users\JP\Documents\GitHub\analysemedia\tessdata"

def ocr_pdf(pdf_path, output_path, lang='fra'):
    print(f"Starting OCR for: {pdf_path}")
    try:
        pages = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)
        print(f"Total pages converted: {len(pages)}")
        
        full_text = ""
        for i, page in enumerate(pages):
            print(f"Processing page {i+1}...")
            text = pytesseract.image_to_string(page, lang=lang)
            full_text += f"\n--- OCR Page {i+1} ---\n{text}\n"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        print(f"OCR completed. Saved to: {output_path}")
    except Exception as e:
        print(f"Error during OCR: {e}")

if __name__ == "__main__":
    # Liste des PDF à traiter dans la racine de documents
    docs = [
        "Magic box 1 Le trésor de la motivation.pdf",
        "Les forces de caractère.pdf",
        "Magic box 7  Comment incarner un leadership authentique .pdf",
        "Révèle tes talents - Affirme tes fiertés.pdf"
    ]
    
    for doc_name in docs:
        input_p = os.path.join("documents", doc_name)
        output_p = os.path.join("output", f"ocr_extracted_{doc_name.replace(' ', '_')}.txt")
        if os.path.exists(input_p):
            ocr_pdf(input_p, output_p)
        else:
            print(f"File not found: {input_p}")
