# HTML to PDF Converter - Streamlit App

A modern web-based interface for converting HTML files to PDF using Streamlit.

## Features

- 📤 **Easy File Upload**: Drag and drop or browse for HTML files
- 🔄 **Instant Conversion**: Convert HTML to PDF with a single click
- 📥 **Direct Download**: Download converted PDFs immediately
- ⚙️ **Customizable Options**: Add timestamps, view conversion details
- 📊 **Statistics**: View conversion metrics and file information
- 🎨 **Modern UI**: Clean, intuitive interface with real-time feedback

## Installation

### Prerequisites
- Python 3.8 or higher

### Setup

1. **Create a virtual environment** (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Usage

### Run the Streamlit App

```bash
streamlit run streamlit_app.py
```

The app will open in your default web browser at `http://localhost:8501`

### Using the App

1. **Upload HTML File**: Click "Browse files" or drag-and-drop an HTML file
2. **Configure Options**:
   - Toggle timestamp addition to filename
   - Enable/disable detailed conversion information
3. **Convert**: Click "Convert to PDF" button
4. **Download**: Click "Download PDF" to save the converted file

### Command-Line Usage (Standalone)

You can also use the standalone converter from command line:

```bash
python html_to_pdf_standalone.py input.html output.pdf
```

With verbose output:
```bash
python html_to_pdf_standalone.py -v input.html output.pdf
```

## Project Structure

```
html_to_pdf_streamlit/
├── streamlit_app.py              # Main Streamlit web application
├── html_to_pdf_standalone.py     # Core converter logic
├── html_to_pdf_app.py           # Tkinter GUI (alternative interface)
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Components

### streamlit_app.py
Modern web-based interface using Streamlit framework with:
- File upload functionality
- Real-time conversion progress
- Download capabilities
- Conversion statistics
- Error handling and validation

### html_to_pdf_standalone.py
Core conversion engine featuring:
- HTML to PDF conversion using xhtml2pdf
- CSS sanitization and optimization
- Multi-page HTML support
- Table handling with complex spanning
- Command-line interface

### html_to_pdf_app.py
Traditional desktop GUI using Tkinter (optional):
- Native desktop application
- File browser integration
- Progress logging
- Standalone executable capability

## Conversion Features

The converter handles:
- ✅ Standard HTML5 elements
- ✅ CSS styling (inline and embedded)
- ✅ Tables with complex layouts
- ✅ Images (embedded and external)
- ✅ Multiple pages with page breaks
- ✅ Custom fonts and formatting
- ✅ Legal document formatting (paragraph numbering)

## Troubleshooting

### Common Issues

1. **Import Error**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Conversion Failed**: 
   - Check HTML file validity
   - Ensure CSS is compatible with xhtml2pdf
   - Try simplifying complex structures

3. **Port Already in Use**: Change Streamlit port
   ```bash
   streamlit run streamlit_app.py --server.port 8502
   ```

## Dependencies

- **streamlit**: Web application framework
- **xhtml2pdf**: HTML to PDF conversion engine
- **pillow**: Image processing
- **reportlab**: PDF generation backend

## License

This project is provided as-is for HTML to PDF conversion tasks.

## Support

For issues or questions:
1. Check the error messages in the app
2. Verify your HTML file is valid
3. Review the troubleshooting section above
