# 📄 Intelligent Document Processor (OCR + NER)

An end-to-end **intelligent document processing** tool that combines:

- 🧾 **Optical Character Recognition (OCR)** – extract text from images / scanned documents  
- 🧠 **Named Entity Recognition (NER)** – detect and categorize entities (persons, organizations, locations, dates, etc.) in text  

Built with **Python**, **Tesseract OCR**, **OpenCV**, **spaCy**, and **Streamlit**.

---

## 🚀 Features

- Upload images of scanned documents or handwritten notes
- Run **OCR** to extract machine-readable text
- Run **NER** to automatically detect entities like:
  - `PERSON`, `ORG`, `GPE`, `DATE`, `TIME`, etc.
- Interactive **Streamlit web UI** with:
  - `OCR Only` mode
  - `NER Only` mode
  - `OCR → NER Pipeline` (end-to-end flow)
- Highlight entities directly inside the text
- Basic support for **Arabic OCR** (via Tesseract `ara` language) in addition to English

> **Note:**  
> NER is currently **English-only** using `spaCy (en_core_web_sm)`.  
> Arabic text can be extracted via OCR, but NER for Arabic is not yet implemented.

---

## 🧱 Tech Stack

- **Language:** Python  
- **Web UI:** Streamlit  
- **OCR:** Tesseract OCR + pytesseract + OpenCV  
- **NLP / NER:** spaCy  
- **Image handling:** Pillow  
- **Data display:** pandas  

---

## 📂 Project Structure

```text
intelligent-document-processor/
│
├─ app.py              # Main Streamlit app (UI + logic)
├─ ocr_utils.py        # OCR helper functions (Tesseract + OpenCV)
├─ ner_utils.py        # NER helper functions (spaCy)
├─ requirements.txt    # Python dependencies
└─ README.md           # Project documentation
🛠️ Installation
1️⃣ Clone the repository
bash
Copy code
git clone https://github.com/<your-username>/intelligent-document-processor.git
cd intelligent-document-processor
2️⃣ Create and activate a virtual environment (recommended)
bash
Copy code
python -m venv .venv
.venv\Scripts\activate   # On Windows

# On Linux / macOS:
# source .venv/bin/activate
3️⃣ Install Python dependencies
bash
Copy code
python -m pip install -r requirements.txt
This installs:

streamlit

pytesseract

opencv-python

Pillow

spacy

pandas

4️⃣ Install spaCy English model
bash
Copy code
python -m spacy download en_core_web_sm
🔡 Tesseract OCR Setup
1️⃣ Install Tesseract
Download and install Tesseract OCR for your OS (Windows / Linux / macOS).

On Windows, it is commonly installed to:

text
Copy code
C:\Program Files\Tesseract-OCR\
Make sure you can run tesseract from the terminal (add it to PATH if needed).

2️⃣ Install Arabic language data (optional but recommended)
To enable Arabic OCR, ensure that ara.traineddata exists in your Tesseract tessdata folder, e.g.:

text
Copy code
C:\Program Files\Tesseract-OCR\tessdata\ara.traineddata
If it's missing, download ara.traineddata from the official Tesseract tessdata repository and place it into the tessdata folder.

3️⃣ Configure Tesseract path in code
In ocr_utils.py, the Tesseract executable and tessdata path are set explicitly (you can adjust if your path is different):

python
Copy code
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"
▶️ Running the App
From the project root:

bash
Copy code
streamlit run app.py
Then open the URL shown in the terminal (usually http://localhost:8501) in your browser.

🧪 How to Use
1️⃣ OCR → NER Pipeline (End-to-End)
In the sidebar, select “OCR → NER Pipeline” mode.

Upload an image containing text (scanned document / printed text / clear handwriting).

Select OCR language:

eng → English

ara → Arabic (requires ara.traineddata)

eng+ara → mixed content

Click “Run OCR” to extract text.

Scroll down to the NER section.

Click “Run NER” to detect entities in the extracted text.

View:

A table of extracted entities.

The text with highlighted spans for each entity.

2️⃣ OCR Only
Select “OCR Only” from the sidebar.

Upload an image and choose OCR language.

Click “Run OCR”.

View the extracted text in the text area.

3️⃣ NER Only
Select “NER Only” from the sidebar.

Paste or type any English text into the input box.

Click “Run NER”.

View:

A table listing entities (text, label, start_char, end_char).

The same text with entities highlighted and labeled inline.

📌 Limitations & Future Work
✅ OCR:

English: supported

Arabic: supported via Tesseract language data (quality depends on image quality and font)

✅ NER:

English: supported using spaCy (en_core_web_sm)

❌ Arabic NER:

Not yet implemented (future enhancement: use CAMeL Tools, Stanza, or a HuggingFace Arabic NER model)

Possible future improvements:

Add Arabic NER model for detecting entities in Arabic text.

Support for PDF uploads with multi-page OCR.

Add export to CSV / JSON for detected entities.

Add Dockerfile for easier deployment.

📚 Example Use Cases
Automating processing of scanned contracts and documents.

Extracting structured data (names, organizations, locations, dates) from reports.

Building a quick prototype for document understanding in an AI / NLP portfolio.

Using it as a base for more advanced document AI pipelines.

👨‍💻 Author
Developed by Ziad Saqr as part of an AI / NLP portfolio project.

If you find this useful, feel free to ⭐ the repo and contribute with ideas or pull requests!

🇦🇷 ملاحظة بالعربي
المشروع ده معمول عشان يورّي End-to-End Flow لطيف:

تاخد صورة/سكان → تطلع منها نص (OCR)

وبعدين تحلل النص وتستخرج منه كيانات مهمّة (NER)

الكود قابل للتطوير بسهولة:

تقدر تزود موديلات NER عربية

أو تحسّن الـ preprocessing بتاع الصور

أو تضيف export للنتائج