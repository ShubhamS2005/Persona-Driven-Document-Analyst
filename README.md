# 📄 Persona-Driven Document Analyst

## 🧠 Objective

This system extracts and prioritizes the most relevant **sections and subsections** from a collection of PDFs based on a defined **persona** and their **job-to-be-done (JTBD)**.

##  Project Structure

```bash 
├── Dockerfile #  Container definition 
├── main.py #  Main execution script 
├── modules/ #  Contains logic for extraction, relevance, etc. 
│ ├── extractor.py          
│ ├── relevence_model.py
│ └── utils.py    
├── requirements.txt
├── input 
├── output 
├── README.md #  Execution and usage guide 
└── approach_explanation.md #  Methodology and architecture explanation
```

---

## 🐳 Docker Execution

### 🛠️ Build the Docker Image
```bash
docker build -t persona-analyst .
```

### Testing the Docker Image 
```bash
# Windows Git Bash or Linux/Mac
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  persona-analyst

# if above not run try
docker run --rm \
  -v $(pwd -W)/input:/app/input \
  -v $(pwd -W)/output:/app/output \
  persona-analyst

# Windows CMD or PowerShell (use this on Windows if above fails)
docker run --rm ^
  -v %cd%/input:/app/input ^
  -v %cd%/output:/app/output ^
  persona-analyst
```


## Dependencies 
All core dependencies are listed in the requirements.txt file.

### Key Libraries Used: 
💡 Semantic Modeling |	transformers, sentence-transformers, scikit-learn \
📄 PDF Extraction	PyMuPDF, nltk, spacy \
🔬 ML + NLP Utility	torch, pillow, typer, regex, rich, Jinja2, sentencepiece

#### Note: For language processing, en_core_web_sm model is also loaded during setup.


To install all dependencies (inside Docker or locally), run:

```bash 
pip install -r requirements.txt
```

##  Author

Developed with ❤️ by **Shubham Srivastava**  
If you use or adapt this work, please consider citing or giving credit.

## License

This project is currently under development and does not have a formal license.  
A suitable open-source license (e.g., MIT, Apache 2.0) will be added upon final release.
