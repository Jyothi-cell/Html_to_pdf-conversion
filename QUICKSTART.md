# Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
cd /home/jyothi/html_to_pdf_streamlit
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
streamlit run streamlit_app.py
```

**Or use the convenient script:**
```bash
./run_app.sh
```

### Step 3: Use the App
1. Open your browser to `http://localhost:8501`
2. Upload an HTML file
3. Click "Convert to PDF"
4. Download your PDF!

## 📋 Features at a Glance

| Feature | Description |
|---------|-------------|
| 📤 **Upload** | Drag & drop or browse for HTML files |
| 🔄 **Convert** | One-click conversion to PDF |
| 📥 **Download** | Instant download of generated PDF |
| ⚙️ **Options** | Timestamp filenames, view details |
| 📊 **Stats** | View file sizes and compression ratio |
| 🎨 **UI** | Clean, modern, responsive interface |

## 🛠️ Alternative Interfaces

### Streamlit Web App (Recommended)
```bash
streamlit run streamlit_app.py
```
- Modern web interface
- Works on any device with a browser
- Real-time feedback
- File upload/download

### Tkinter Desktop App
```bash
python html_to_pdf_app.py
```
- Traditional desktop GUI
- Native file browser
- Standalone application

### Command Line
```bash
python html_to_pdf_standalone.py input.html output.pdf
```
- Quick conversions
- Scriptable
- Batch processing

## 💡 Tips

- **Large Files**: The app handles large HTML files efficiently
- **Multiple Files**: Upload one at a time or use CLI for batch processing
- **Custom CSS**: Most CSS is supported, but complex layouts may need adjustment
- **Tables**: Complex table structures are automatically optimized

## ⚠️ Common Issues

**Port already in use?**
```bash
streamlit run streamlit_app.py --server.port 8502
```

**Dependencies missing?**
```bash
pip install --upgrade -r requirements.txt
```

**HTML not converting?**
- Check HTML validity
- Simplify complex CSS
- Remove unsupported elements

## 📞 Need Help?

Check the full README.md for detailed documentation and troubleshooting.

---
**Happy Converting! 📄➡️📋**
