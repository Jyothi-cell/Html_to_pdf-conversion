#!/usr/bin/env python3
"""
Streamlit HTML to PDF Converter
A web-based interface for converting HTML files to PDF
"""

import streamlit as st
import os
from datetime import datetime
from html_to_pdf_standalone import HTMLToPDFConverter
import base64


def get_binary_file_downloader_html(bin_file, file_label='File'):
    """Generate a download link for binary files"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/pdf;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href


def main():
    # Page configuration
    st.set_page_config(
        page_title="HTML to PDF Converter",
        page_icon="📄",
        layout="centered"
    )
    
    # Custom CSS for styling
    st.markdown("""
        <style>
        .main-title {
            color: #1E3A8A;
            text-align: center;
            padding: 20px;
            font-size: 48px;
            font-weight: bold;
        }
        .success-box {
            background-color: #D1FAE5;
            border-left: 5px solid #10B981;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .error-box {
            background-color: #FEE2E2;
            border-left: 5px solid #EF4444;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .info-box {
            background-color: #DBEAFE;
            border-left: 5px solid #3B82F6;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown('<p class="main-title">📄 HTML to PDF Converter</p>', unsafe_allow_html=True)
    
    # Help notice
    with st.expander("💡 How to Save Downloaded Files", expanded=False):
        st.markdown("""
        **Two ways to save your PDF:**
        
        1. **Download Button (Default Browser Download)**
           - Click "📥 Download PDF" 
           - Your browser will download the file
           - Check your browser's download bar (usually at bottom)
           - Or check your Downloads folder
        
        2. **Save to Desktop Button (Direct Save)**
           - Click "💾 Save to Desktop"
           - File saves directly to your Desktop or Downloads folder
           - No browser download needed
        
        **Tip:** If download button opens the PDF instead of saving:
        - Right-click the "📥 Download PDF" button
        - Select "Save link as..." or "Download linked file"
        - Choose where to save it
        """)
    
    st.markdown("---")
    
    # Initialize converter
    if 'converter' not in st.session_state:
        st.session_state.converter = HTMLToPDFConverter()
    
    # File uploader
    st.subheader("📂 Upload HTML File")
    uploaded_file = st.file_uploader(
        "Choose an HTML file",
        type=['html', 'htm'],
        help="Select an HTML file to convert to PDF"
    )
    
    # Conversion options
    st.subheader("⚙️ Conversion Options")
    col1, col2 = st.columns(2)
    
    with col1:
        add_timestamp = st.checkbox(
            "Add timestamp to filename",
            value=True,
            help="Append timestamp to output PDF filename"
        )
    
    with col2:
        show_details = st.checkbox(
            "Show conversion details",
            value=True,
            help="Display detailed conversion progress"
        )
    
    # Convert button
    st.markdown("---")
    
    if uploaded_file is not None:
        # Display file info
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown(f"""
        **File Information:**
        - **Name:** {uploaded_file.name}
        - **Size:** {uploaded_file.size:,} bytes
        - **Type:** {uploaded_file.type}
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Convert button
        if st.button("🔄 Convert to PDF", type="primary", use_container_width=True):
            try:
                # Progress indicators
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Read HTML content
                status_text.text("📄 Reading HTML file...")
                progress_bar.progress(20)
                html_content = uploaded_file.read().decode('utf-8')
                
                if show_details:
                    st.info(f"✓ HTML content loaded ({len(html_content):,} characters)")
                
                # Convert to PDF
                status_text.text("🔄 Converting HTML to PDF...")
                progress_bar.progress(50)
                
                pdf_bytes = st.session_state.converter.create_pdf_from_html(html_content)
                
                progress_bar.progress(80)
                
                if pdf_bytes:
                    # Generate output filename
                    base_name = os.path.splitext(uploaded_file.name)[0]
                    
                    if add_timestamp:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_filename = f"{base_name}_{timestamp}.pdf"
                    else:
                        output_filename = f"{base_name}.pdf"
                    
                    # Save to temp directory
                    temp_dir = "/tmp"
                    output_path = os.path.join(temp_dir, output_filename)
                    
                    with open(output_path, 'wb') as f:
                        f.write(pdf_bytes)
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Conversion complete!")
                    
                    # Success message
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.markdown(f"""
                    ### ✅ Conversion Successful!
                    
                    **Output Details:**
                    - **Filename:** {output_filename}
                    - **Size:** {len(pdf_bytes):,} bytes
                    - **Status:** Ready for download
                    """)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Download button with improved handling
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.download_button(
                            label="📥 Download PDF",
                            data=pdf_bytes,
                            file_name=output_filename,
                            mime="application/pdf",
                            use_container_width=True,
                            help="Click to download the PDF file to your Downloads folder"
                        )
                    
                    with col2:
                        # Also save to a temp location for easier access
                        if st.button("💾 Save to Desktop", use_container_width=True, help="Save PDF to Desktop folder"):
                            try:
                                desktop_path = os.path.expanduser("~/Desktop")
                                if os.path.exists(desktop_path):
                                    desktop_file = os.path.join(desktop_path, output_filename)
                                    with open(desktop_file, 'wb') as f:
                                        f.write(pdf_bytes)
                                    st.success(f"✅ Saved to Desktop: {output_filename}")
                                else:
                                    # Try Downloads folder
                                    downloads_path = os.path.expanduser("~/Downloads")
                                    if os.path.exists(downloads_path):
                                        downloads_file = os.path.join(downloads_path, output_filename)
                                        with open(downloads_file, 'wb') as f:
                                            f.write(pdf_bytes)
                                        st.success(f"✅ Saved to Downloads: {output_filename}")
                                    else:
                                        st.error("Could not find Desktop or Downloads folder")
                            except Exception as save_error:
                                st.error(f"Error saving file: {save_error}")
                    
                    # Show additional details if requested
                    if show_details:
                        st.markdown("---")
                        st.subheader("📊 Conversion Statistics")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Input Size", f"{len(html_content):,} chars")
                        
                        with col2:
                            st.metric("Output Size", f"{len(pdf_bytes):,} bytes")
                        
                        with col3:
                            compression_ratio = (1 - len(pdf_bytes) / len(html_content)) * 100
                            st.metric("Compression", f"{compression_ratio:.1f}%")
                    
                else:
                    st.markdown('<div class="error-box">', unsafe_allow_html=True)
                    st.markdown("### ✗ Conversion Failed")
                    st.markdown("Failed to create PDF. Please check your HTML file and try again.")
                    st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.markdown(f"""
                ### ✗ Error During Conversion
                
                **Error Message:**
                ```
                {str(e)}
                ```
                
                **Troubleshooting Tips:**
                - Ensure your HTML file is valid and well-formed
                - Check for any special characters or unsupported CSS
                - Try simplifying complex HTML structures
                """)
                st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.info("👆 Please upload an HTML file to get started")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6B7280; padding: 20px;'>
        <p><strong>HTML to PDF Converter</strong></p>
        <p>Built with Streamlit & xhtml2pdf</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
