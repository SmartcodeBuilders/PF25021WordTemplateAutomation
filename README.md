# 📄 Excel → Word Template Automation  

This project is a **Streamlit web app** that lets you:  

1. Upload an **Excel file** with tags and user input data.  
2. Upload a **Word template** containing placeholders (`{{KEYWORD}}`).  
3. Automatically replace placeholders with Excel values.  
4. Download the processed Word file.  

---

## 🚀 Features  

- Upload **Excel input data**.  
- Configure:  
  - **First row with data** (default: 5)  
  - **Tag column** (default: 6 → Column F)  
  - **User input column** (default: 5 → Column E)  
- Preview extracted tags and values.  
- Upload a **Word `.docx` template**.  
- Replace placeholders like `{{LANDLORD_NAME}}` with values from Excel.  
- Download the generated Word file.  
- Missing placeholders remain in the document without breaking formatting.  

---

## 🛠️ Installation (Development)  

1. Clone the repo:  

```bash
git clone https://github.com/SmartcodeBuilders/PF25021WordTemplateAutomation.git
cd PF25021WordTemplateAutomation
```

2. Create a virtual environment:
```bash
python -m venv venv
```
Activate it: 
- Windows: ```venv\Scripts\activate```
- Linux: ```source venv/bin/activate```

3. Install dependencies:
```pip install -r requirements.txt```

4. Run the app locally:
```streamlit run app.py```