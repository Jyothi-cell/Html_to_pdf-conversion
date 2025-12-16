# HTML to PDF Converter

A Streamlit web application that converts HTML files to PDF with customizable formatting.

## Features

- 📄 Upload HTML files and convert to PDF
- 🎨 Optimized formatting with clean spacing (line-height: 1.6, 11pt font)
- 💾 Dual download options (browser & desktop save)
- 📱 Responsive web interface
- ☁️ Cloud-ready for Streamlit deployment

## Local Installation

1. Clone this repository
2. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   streamlit run streamlit_app.py
   ```

## Streamlit Cloud Deployment

### Quick Deploy Steps

1. **Push to GitHub**
   - Create a new repository on GitHub
   - Push this code to your repository:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git remote add origin YOUR_GITHUB_REPO_URL
     git push -u origin main
     ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository, branch (main), and main file: `streamlit_app.py`
   - Click "Deploy"

### Files Required for Deployment

✅ All required files are included:
- `streamlit_app.py` - Main application
- `html_to_pdf_standalone.py` - PDF conversion logic
- `requirements.txt` - Python dependencies
- `packages.txt` - System dependencies (for Linux)
- `.streamlit/config.toml` - Streamlit configuration

## Usage

1. Upload an HTML file using the file uploader
2. Configure options:
   - Add timestamp to filename (optional)
   - Show conversion details (optional)
3. Click "Convert to PDF"
4. Download using either:
   - **📥 Download PDF** - Browser download
   - **💾 Save to Desktop** - Direct file save

## Technical Details

### PDF Formatting
- **Font**: Arial, 11pt
- **Line spacing**: 1.6x (comfortable reading)
- **Paragraph margins**: 0.4em
- **Heading spacing**: 0.6em top, 0.3em bottom
- **Page size**: Letter (8.5" x 11")

### Processing
1. Removes embedded `<style>` blocks from source HTML
2. Applies clean, consistent formatting
3. Replaces inline styles with optimized values
4. Generates PDF with xhtml2pdf engine

## Dependencies

### Python Packages
- streamlit >= 1.28.0
- xhtml2pdf >= 0.2.13
- pillow >= 10.0.0
- reportlab >= 4.0.0

### System Packages (Linux/Cloud)
- libxml2, libxslt1.1
- libcairo2, libpango-1.0-0
- libgdk-pixbuf2.0-0

These are automatically installed on Streamlit Cloud via `packages.txt`.

## Troubleshooting

### Local Development
- **Port already in use**: Change port with `streamlit run streamlit_app.py --server.port 8502`
- **Import errors**: Ensure virtual environment is activated
- **PDF conversion fails**: Check that system packages are installed

### Streamlit Cloud
- **Build fails**: Check logs in Streamlit Cloud dashboard
- **System dependencies**: Ensure `packages.txt` is in root directory
- **App crashes**: Check resource limits (Streamlit Cloud has memory limits)

## License

MIT License

## Support

For issues or questions, please open an issue on GitHub.
