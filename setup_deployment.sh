#!/bin/bash

echo "================================"
echo "Streamlit Cloud Deployment Setup"
echo "================================"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "Initializing Git repository..."
    git init
    echo "✓ Git initialized"
else
    echo "✓ Git repository already exists"
fi

# Create .gitignore if needed
if [ ! -f .gitignore ]; then
    echo "✓ .gitignore already created"
fi

# Show status
echo ""
echo "Current files to be deployed:"
echo "----------------------------"
ls -1 streamlit_app.py html_to_pdf_standalone.py requirements.txt packages.txt .streamlit/config.toml 2>/dev/null

echo ""
echo "Next steps for Streamlit Cloud deployment:"
echo "===========================================" 
echo ""
echo "1. Create a GitHub repository at https://github.com/new"
echo ""
echo "2. Run these commands (replace YOUR_GITHUB_URL):"
echo "   git add ."
echo "   git commit -m 'Initial commit - HTML to PDF Converter'"
echo "   git remote add origin YOUR_GITHUB_URL"
echo "   git push -u origin main"
echo ""
echo "3. Deploy on Streamlit Cloud:"
echo "   - Go to https://share.streamlit.io"
echo "   - Click 'New app'"
echo "   - Select your repository"
echo "   - Main file: streamlit_app.py"
echo "   - Click 'Deploy'"
echo ""
echo "✓ Setup complete!"
