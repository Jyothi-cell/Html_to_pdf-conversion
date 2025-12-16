#!/bin/bash
# Run script for HTML to PDF Streamlit App

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Run Streamlit app
echo "Starting Streamlit app..."
echo "Opening at http://localhost:8501"
streamlit run streamlit_app.py
