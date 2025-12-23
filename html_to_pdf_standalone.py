#!/usr/bin/env python3
"""
Standalone HTML to PDF Converter
Converts HTML content to PDF without external framework dependencies.
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
                @page {{ size: letter; margin: 1cm; }}
                body {{ font-family: Arial, sans-serif; font-size: 11pt; line-height: 1.6; margin: 0; padding: 0; }}
                .page {{ page-break-after: always; margin: 0; padding: 0; }}
                .page:last-child {{ page-break-after: auto; }}
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
        
    def sanitize_css_values(self, html_content: str) -> str:
        """
        Clean up CSS values and problematic patterns in HTML.
        
        Args:
            html_content: HTML string to sanitize
            
        Returns:
            Sanitized HTML string
        """
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
    
        # Clean up any decimal values in CSS or attributes
        html_content = re.sub(r'(\d+)\.(\d+)px', r'\1px', html_content)
        html_content = re.sub(r'(\d+)\.(\d+)pt', r'\1pt', html_content)
        html_content = re.sub(r'(\d+)\.(\d+)em', r'\1em', html_content)
        html_content = re.sub(r'(\d+)\.(\d+)%', r'\1%', html_content)
        
        # Remove any problematic attributes that might contain decimal values
        html_content = re.sub(r'width="[\d.]+?"', 'width="100%"', html_content)
        html_content = re.sub(r'height="[\d.]+?"', '', html_content)
        
        # Fix patterns like "paragraph 1.1", "clause 3.2", "Article 176.1", etc.
        #html_content = re.sub(r'\b(\w+)\s+(\d+)\.(\d+)\b', r'\1 \2_\3', html_content)
        
        # Fix patterns in parenthetical references like "(paragraph 4.1)"
        #html_content = re.sub(r'\((\w+)\s+(\d+)\.(\d+)\)', r'(\1 \2_\3)', html_content)
        
        # Fix standalone decimal references like "3.1", "5.2" when they appear in legal contexts
        #html_content = re.sub(r'\b(\d+)\.(\d+)\s+(of\s+this\s+article|of\s+Article|of\s+this\s+Code)\b', r'\1_\2 \3', html_content)
        
        # Remove page number patterns like "201/1975", "202/1975" etc.
        html_content = re.sub(r'\b\d+/\d+\b', '', html_content)
        
        # Remove extra whitespace between tags
        html_content = re.sub(r'>\s+<', '><', html_content)
    
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
        # First sanitize (remove bad styles)
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

            return pdf_output.getvalue()
        except Exception as e:
            error_msg = f"Error in PDF creation process: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)

    def convert_html_file_to_pdf(self, html_file_path: str, output_pdf_path: str) -> None:
        """
        Convert an HTML file to PDF.
        
        Args:
            html_file_path: Path to input HTML file
            output_pdf_path: Path to output PDF file
        """
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        pdf_bytes = self.create_pdf_from_html(html_content)
        
        with open(output_pdf_path, 'wb') as f:
            f.write(pdf_bytes)
        
        print(f"✓ PDF created successfully: {output_pdf_path} ({len(pdf_bytes)} bytes)")

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
    
    args = parser.parse_args()
    
    # Configure logging
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    try:
        converter = HTMLToPDFConverter()
        converter.convert_html_file_to_pdf(args.input_html, args.output_pdf)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
