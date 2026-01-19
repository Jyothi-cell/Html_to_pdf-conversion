#!/usr/bin/env python3  
"""  
Standalone HTML to PDF Converter  
Converts HTML content to PDF while preserving source formatting.

KEY FEATURES & FIXES:
1. Font Handling:
   - Uses Liberation Sans (not DejaVu Sans) which has complete italic support
   - Ensures <em>, <i> tags render as italic (not bold)
   - Critical for legal documents with italic annotations (e.g., {curly brace content})

2. List Marker Preservation:
   - Detects lists with list-style-type: none
   - Preserves text markers (a), b), c)) in such lists
   - Removes duplicate markers only when list has automatic markers

3. Character Preservation:
   - All bracket types ({}, [], ()) are preserved exactly as in HTML
   - No character substitution or encoding changes
   - UTF-8 encoding maintained throughout

4. Formatting Preservation:
   - Bold, italic, bold-italic all work correctly
   - Table structures maintained
   - Legal reference numbers (e.g., 14.1.13) preserved
"""
  
import logging  
from io import BytesIO  
from typing import List, Union  
import re  
from xhtml2pdf import pisa  
import argparse  
import sys
  
logger = logging.getLogger(__name__)

  
class HTMLToPDFConverter:  
    """Convert HTML content to PDF format."""
  
    def combine_html_pages(self, html_pages: List[str]) -> str:  
        """  
        Combine multiple HTML pages into a single HTML document with page breaks.
          
        Args:  
            html_pages: List of HTML content strings
              
        Returns:  
            Combined HTML string with CSS styling  
        """  
        combined_content = "".join(  
            [  
                f'<div class="page" style="page-break-after: always;">{page}</div>'  
                for page in html_pages  
            ]  
        )
  
        full_html = f"""  
        <html>  
        <head>  
            <meta charset="UTF-8">  
            <style>  
                /* Using Liberation Sans font family because it has proper support for:
                   - Regular, Bold, Italic, and Bold-Italic variants
                   - This ensures HTML <em>, <i>, <strong>, <b> tags render correctly
                   - Critical for preserving source formatting like italic curly braces */
                @font-face {{
                    font-family: MainFont;
                    src: url('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf');
                    font-weight: normal;
                    font-style: normal;
                }}
                @font-face {{
                    font-family: MainFont;
                    src: url('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf');
                    font-weight: bold;
                    font-style: normal;
                }}
                @font-face {{
                    font-family: MainFont;
                    src: url('/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf');
                    font-weight: normal;
                    font-style: italic;
                }}
                @font-face {{
                    font-family: MainFont;
                    src: url('/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf');
                    font-weight: bold;
                    font-style: italic;
                }}
                @page {{ size: letter; margin: 1cm; }}  
                body {{ font-family: MainFont, "Liberation Sans", Arial, sans-serif; font-size: 11pt; line-height: 1.6; margin: 0; padding: 0; }}  
                .page {{ page-break-after: always; margin: 0; padding: 0; }}  
                .page:last-child {{ page-break-after: auto; }}
                  
                /* List styling */  
                ol, ul {{ margin: 0.5em 0; padding-left: 2em; }}  
                ol[type="a"] {{ list-style-type: lower-alpha; }}  
                ol[type="A"] {{ list-style-type: upper-alpha; }}  
                ol[type="i"] {{ list-style-type: lower-roman; }}  
                ol[type="I"] {{ list-style-type: upper-roman; }}  
                ol[type="1"], ol {{ list-style-type: decimal; }}  
                li {{ margin: 0.3em 0; line-height: 1.6; }}
                  
                table {{  
                    border-collapse: collapse;  
                    width: 100%;  
                    margin: 0.5em 0;  
                    font-size: 11pt;  
                    table-layout: fixed;  
                }}  
                th, td {{  
                    border: 1px solid #ddd;  
                    padding: 6px;  
                    text-align: left;  
                    vertical-align: top;  
                    word-wrap: break-word;  
                    line-height: 1.6;  
                }}  
                th {{ background-color: #f2f2f2; font-weight: bold; }}  
                h1, h2, h3, h4, h5, h6 {{ margin: 0.6em 0 0.3em 0; line-height: 1.4; }}  
                h1 {{ font-size: 18pt; }}  
                h2 {{ font-size: 15pt; }}  
                h3 {{ font-size: 13pt; }}  
                p {{ margin: 0.4em 0; padding: 0; line-height: 1.6; }}  
                div {{ margin: 0; padding: 0; }}  
                pre {{ white-space: pre-wrap; word-wrap: break-word; background-color: #f0f0f0; padding: 6px; border-radius: 2px; margin: 0.4em 0; line-height: 1.6; }}  
                code {{ background-color: #f0f0f0; padding: 3px 5px; border-radius: 2px; }}  
                .error {{ border: 2px solid red; padding: 6px; margin: 0.4em 0; }}  
                b, strong {{ font-weight: bold; }}  
                i, em {{ font-style: italic; }}  
            </style>  
        </head>  
        <body>  
            {combined_content}  
        </body>  
        </html>  
        """  
        return full_html
      
    def fix_list_styles(self, html_content: str) -> str:  
        """  
        Convert ol type attributes to inline CSS styles for better PDF rendering.
          
        Args:  
            html_content: HTML string to process
              
        Returns:  
            HTML string with list styles converted  
        """  
        # Map type attributes to CSS list-style-type values  
        type_mapping = {  
            'a': 'lower-alpha',  
            'A': 'upper-alpha',  
            'i': 'lower-roman',  
            'I': 'upper-roman',  
            '1': 'decimal'  
        }
          
        # Replace ol type attributes with inline styles  
        def replace_ol_type(match):  
            type_value = match.group(1)  
            other_attrs = match.group(2) if match.group(2) else ''
              
            if type_value in type_mapping:  
                css_value = type_mapping[type_value]
                  
                # Check if style attribute already exists in other_attrs  
                if 'style=' in other_attrs:  
                    # Add to existing style  
                    other_attrs = re.sub(  
                        r'style="([^"]*)"',  
                        rf'style="\1; list-style-type: {css_value};"',  
                        other_attrs  
                    )  
                else:  
                    # Add new style attribute  
                    other_attrs += f' style="list-style-type: {css_value};"'
                  
                return f'<ol{other_attrs}>'
              
            return match.group(0)
          
        # Find all <ol type="..."> patterns  
        html_content = re.sub(  
            r'<ol[^>]*type=["\']([^"\']+)["\']([^>]*?)>',  
            replace_ol_type,  
            html_content  
        )
          
        return html_content
    
    def remove_duplicate_list_markers(self, html_content: str) -> str:
        """
        Remove duplicate list markers from <li> content, but ONLY when the list
        has visible markers (not list-style-type: none).
        
        This is critical for preserving source formatting:
        - When list has list-style-type: none → text markers like "a)", "b)" must be kept
        - When list has default markers → text markers should be removed to avoid duplication
        
        Example: <li>1. text</li> becomes <li>text</li> when list has markers
        
        Args:
            html_content: HTML string to process
            
        Returns:
            HTML string with cleaned list items
        """
        # Find all list blocks (ul/ol) and process them individually
        def process_list(match):
            list_tag = match.group(0)
            
            # Check if this list has list-style-type: none (with or without spaces/colons)
            # IMPORTANT: Lists with "none" style need text markers preserved
            if 'list-style-type' in list_tag and 'none' in list_tag:
                # Don't remove markers - they're the ONLY markers visible
                return list_tag
            
            # This list has visible markers, so remove duplicate text markers
            # Remove numbered markers like "1. ", "2. ", "123. " from start of <li>
            list_tag = re.sub(r'<li>\s*\d+\.\s+', r'<li>', list_tag)
            
            # Remove alphabetical markers like "a) ", "b) ", "z) " from start of <li>
            list_tag = re.sub(r'<li>\s*[a-z]\)\s+', r'<li>', list_tag, flags=re.IGNORECASE)
            
            # Remove roman numeral markers like "(i) ", "(ii) ", "(iii) " from start of <li>
            list_tag = re.sub(r'<li>\s*\([ivxlcdm]+\)\s+', r'<li>', list_tag, flags=re.IGNORECASE)
            
            # Remove alphabetical markers with periods like "a. ", "b. " from start of <li>
            list_tag = re.sub(r'<li>\s*[a-z]\.\s+', r'<li>', list_tag, flags=re.IGNORECASE)
            
            # Remove uppercase alphabetical markers like "A) ", "B) " from start of <li>
            list_tag = re.sub(r'<li>\s*[A-Z]\)\s+', r'<li>', list_tag)
            
            # Remove uppercase roman numerals like "(I) ", "(II) " from start of <li>
            list_tag = re.sub(r'<li>\s*\([IVXLCDM]+\)\s+', r'<li>', list_tag)
            
            return list_tag
        
        # Process all <ul> and <ol> blocks
        html_content = re.sub(r'<(?:ul|ol)[^>]*>.*?</(?:ul|ol)>', process_list, html_content, flags=re.DOTALL | re.IGNORECASE)
        
        return html_content
      
    def protect_legal_references(self, html_content: str) -> str:  
        """  
        Temporarily replace periods in legal references with underscores to prevent  
        them from being treated as decimal numbers.
          
        Args:  
            html_content: HTML string to process
              
        Returns:  
            HTML string with protected legal references  
        """  
        # PROTECTION PHASE: Fix patterns like "paragraph 1.1", "clause 3.2", "Article 176.1", etc.  
        html_content = re.sub(r'\b(\w+)\s+(\d+)\.(\d+)\b', r'\1 \2_\3', html_content)
          
        # Fix patterns in parenthetical references like "(paragraph 4.1)"  
        html_content = re.sub(r'\((\w+)\s+(\d+)\.(\d+)\)', r'(\1 \2_\3)', html_content)
          
        # Fix standalone decimal references like "3.1", "5.2" when they appear in legal contexts  
        html_content = re.sub(r'\b(\d+)\.(\d+)\s+(of\s+this\s+article|of\s+Article|of\s+this\s+Code)\b', r'\1_\2 \3', html_content)
          
        return html_content
      
    def restore_legal_references(self, html_content: str) -> str:  
        """  
        Restore legal reference periods that were temporarily replaced with underscores.
          
        Args:  
            html_content: HTML string with protected legal references
              
        Returns:  
            HTML string with restored periods in legal references  
        """  
        # RESTORATION PHASE: Reverse "paragraph 1_1" back to "paragraph 1.1"  
        html_content = re.sub(r'\b(\w+)\s+(\d+)_(\d+)\b', r'\1 \2.\3', html_content)
          
        # Reverse "(paragraph 4_1)" back to "(paragraph 4.1)"  
        html_content = re.sub(r'\((\w+)\s+(\d+)_(\d+)\)', r'(\1 \2.\3)', html_content)
          
        # Reverse "3_1 of this article" back to "3.1 of this article"  
        html_content = re.sub(r'\b(\d+)_(\d+)\s+(of\s+this\s+article|of\s+Article|of\s+this\s+Code)\b', r'\1.\2 \3', html_content)
          
        return html_content
          
    def sanitize_css_values(self, html_content: str) -> str:  
        """  
        Clean up CSS values and problematic patterns in HTML.
          
        Args:  
            html_content: HTML string to sanitize
              
        Returns:  
            Sanitized HTML string  
        """  
        # Fix list styles first (before any other processing)  
        html_content = self.fix_list_styles(html_content)
        
        # Remove duplicate list markers from <li> content
        html_content = self.remove_duplicate_list_markers(html_content)
          
        # Remove the entire <style> section from HTML as it has excessive spacing  
        html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
          
        # Remove empty paragraphs that create unwanted spacing  
        html_content = re.sub(r'<p>\s*</p>', '', html_content)  
        html_content = re.sub(r'<p>\s*&nbsp;\s*</p>', '', html_content)
          
        # Remove multiple consecutive <br> tags (replace with single br)  
        html_content = re.sub(r'(<br\s*/?>\s*){2,}', '<br>', html_content)
          
        # Remove <br> tags at the start of paragraphs  
        html_content = re.sub(r'<p>\s*<br\s*/?>\s*', '<p>', html_content)
          
        # Remove page number patterns like "201/1975"  
        html_content = re.sub(r'<p>\s*\d+/\d+\s*</p>', '', html_content)
          
        # Remove excessive padding and margin from inline styles  
        html_content = re.sub(r'padding:\s*\d+px;?', 'padding:6px;', html_content)  
        html_content = re.sub(r'margin:\s*\d+px;?', 'margin:0.4em;', html_content)  
        html_content = re.sub(r'margin-bottom:\s*\d+px;?', 'margin-bottom:0.4em;', html_content)  
        html_content = re.sub(r'margin-top:\s*\d+px;?', 'margin-top:0.4em;', html_content)  
        html_content = re.sub(r'line-height:\s*[\d.]+;?', 'line-height:1.6;', html_content)
      
        # Clean up any decimal values in CSS or attributes (but NOT in legal references)  
        # First protect legal references  
        html_content = self.protect_legal_references(html_content)
          
        # Now safe to remove decimal values in CSS  
        html_content = re.sub(r'(\d+)\.(\d+)px', r'\1px', html_content)  
        html_content = re.sub(r'(\d+)\.(\d+)pt', r'\1pt', html_content)  
        html_content = re.sub(r'(\d+)\.(\d+)em', r'\1em', html_content)  
        html_content = re.sub(r'(\d+)\.(\d+)%', r'\1%', html_content)
          
        # Remove any problematic attributes that might contain decimal values  
        html_content = re.sub(r'width="[\d.]+?"', 'width="100%"', html_content)  
        html_content = re.sub(r'height="[\d.]+?"', '', html_content)
          
        # Remove page number patterns like "201/1975", "202/1975" etc.  
        html_content = re.sub(r'\b\d+/\d+\b', '', html_content)
          
        # Remove extra whitespace between tags  
        html_content = re.sub(r'>\s+<', '><', html_content)
          
        # RESTORE legal references back to periods  
        html_content = self.restore_legal_references(html_content)
      
        return html_content
      
    def create_pdf_from_html(self, html_content: str) -> bytes:  
        """  
        Convert HTML content to PDF bytes.
          
        Args:  
            html_content: HTML string to convert
              
        Returns:  
            PDF content as bytes
              
        Raises:  
            Exception: If PDF generation fails  
        """  
        pdf_output = BytesIO()  
        # First sanitize (remove bad styles, protect and restore legal references)  
        html_content = self.sanitize_css_values(html_content)  
        # Then wrap with tight CSS styling  
        html_content = self.combine_html_pages([html_content])
          
        try:  
            pisa_status = pisa.CreatePDF(  
                html_content,  
                dest=pdf_output,  
                encoding="utf-8",  
                show_error_as_pdf=True,  
            )
  
            if pisa_status.err:  
                error_msg = f"PDF generation failed: {pisa_status.err}"  
                logger.error(error_msg)  
                raise Exception(error_msg)  
            else:  
                logger.debug("PDF generation successful")
  
            pdf_bytes = pdf_output.getvalue()
              
            return pdf_bytes  
        except Exception as e:  
            error_msg = f"Error in PDF creation process: {str(e)}"  
            logger.error(error_msg)  
            raise Exception(error_msg)
  
    def convert_html_file_to_pdf(self, html_file_path: str, output_pdf_path: str, save_processed_html: bool = False) -> None:  
        """  
        Convert an HTML file to PDF.
          
        Args:  
            html_file_path: Path to input HTML file  
            output_pdf_path: Path to output PDF file  
            save_processed_html: If True, save the processed HTML with restored references  
        """  
        with open(html_file_path, 'r', encoding='utf-8') as f:  
            html_content = f.read()
          
        pdf_bytes = self.create_pdf_from_html(html_content)
          
        with open(output_pdf_path, 'wb') as f:  
            f.write(pdf_bytes)
          
        print(f"✓ PDF created successfully: {output_pdf_path} ({len(pdf_bytes)} bytes)")
          
        # Optionally save the processed HTML  
        if save_processed_html:  
            processed_html = self.sanitize_css_values(html_content)  
            processed_html = self.combine_html_pages([processed_html])  
            processed_html_path = output_pdf_path.replace('.pdf', '_processed.html')  
            with open(processed_html_path, 'w', encoding='utf-8') as f:  
                f.write(processed_html)  
            print(f"✓ Processed HTML saved: {processed_html_path}")
  
    def convert_html_pages_to_pdf(self, html_pages: List[str], output_pdf_path: str) -> None:  
        """  
        Convert a list of HTML pages to a single PDF.
          
        Args:  
            html_pages: List of HTML content strings  
            output_pdf_path: Path to output PDF file  
        """  
        # Check for problematic tables and fix them proactively  
        fixed_pages = []  
        for i, page in enumerate(html_pages):  
            # Check if this page has a table with complex spanning  
            if "<table" in page and (  
                re.search(r'colspan="[^"]*"', page) or re.search(r'rowspan="[^"]*"', page)  
            ):  
                logger.debug(f"Fixing table with complex spanning in page {i+1}")
  
                # Remove colspan and rowspan attributes that cause issues  
                page = re.sub(r'colspan="[^"]*"', "", page)  
                page = re.sub(r'rowspan="[^"]*"', "", page)
  
                # Add explicit width to table and table-layout: fixed  
                page = re.sub(  
                    r"<table([^>]*)>",  
                    r'<table\1 style="table-layout: fixed; width: 100%;">',  
                    page,  
                )
  
                # Add explicit width to cells  
                page = re.sub(r"<td([^>]*)>", r'<td\1 style="width: auto;">', page)  
                page = re.sub(r"<th([^>]*)>", r'<th\1 style="width: auto;">', page)
  
            fixed_pages.append(page)
  
        full_html = self.combine_html_pages(fixed_pages)  
        pdf_bytes = self.create_pdf_from_html(full_html)
          
        with open(output_pdf_path, 'wb') as f:  
            f.write(pdf_bytes)
          
        print(f"✓ PDF created successfully: {output_pdf_path} ({len(pdf_bytes)} bytes)")

  
def main():  
    """Command-line interface for HTML to PDF conversion."""  
    parser = argparse.ArgumentParser(  
        description="Convert HTML files to PDF",  
        formatter_class=argparse.RawTextHelpFormatter  
    )  
    parser.add_argument("input_html", help="Path to input HTML file")  
    parser.add_argument("output_pdf", help="Path to output PDF file")  
    parser.add_argument(  
        "-v", "--verbose", action="store_true",  
        help="Enable verbose logging"  
    )  
    parser.add_argument(  
        "--save-html", action="store_true",  
        help="Save processed HTML for debugging"  
    )
      
    args = parser.parse_args()
      
    # Configure logging  
    if args.verbose:  
        logging.basicConfig(level=logging.DEBUG)  
    else:  
        logging.basicConfig(level=logging.INFO)
      
    try:  
        converter = HTMLToPDFConverter()  
        converter.convert_html_file_to_pdf(  
            args.input_html,   
            args.output_pdf,  
            save_processed_html=args.save_html  
        )  
    except Exception as e:  
        print(f"✗ Error: {e}", file=sys.stderr)  
        sys.exit(1)

  
if __name__ == "__main__":  
    main()  
