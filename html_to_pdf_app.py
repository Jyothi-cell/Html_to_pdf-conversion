import tkinter as tk
from tkinter import Text, DISABLED, END, filedialog, messagebox
import os
from datetime import datetime
from html_to_pdf_standalone import HTMLToPDFConverter


class HTMLToPDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML to PDF Converter")
        self.root.configure(background='orange')
        self.root.resizable(0, 0)
        
        # Center window
        windowWidth = 680
        windowHeight = 400
        positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2)
        self.root.geometry(f'{windowWidth}x{windowHeight}+{positionRight}+{positionDown}')
        
        # Variables
        self.html_file_path = ""
        self.output_file_path = ""
        
        # Initialize converter
        self.converter = HTMLToPDFConverter()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        label_text = tk.Label(
            self.root, 
            text='HTML to PDF Converter', 
            font=("Helvetica", 30, "bold"), 
            bg='orange', 
            fg='Dark Blue'
        )
        label_text.place(x=140, y=20)
        
        # HTML File Selection
        html_button = tk.Button(
            self.root, 
            text="Select HTML File", 
            fg="Blue", 
            command=self.browse_html, 
            font=('Sans', '10', 'bold'), 
            bg='light gray'
        )
        html_button.place(x=20, y=90, width=175, height=40)
        
        self.html_text = Text(self.root, bd=3, state=DISABLED, fg='black', relief=tk.SUNKEN)
        self.html_text.place(x=220, y=90, width=425, height=40)
        
        # Output File Display
        output_label = tk.Button(
            self.root, 
            text="Output File", 
            fg="Green", 
            state='disabled', 
            font=('Sans', '10', 'bold'), 
            bg='light gray'
        )
        output_label.place(x=20, y=150, width=175, height=40)
        
        self.output_text = Text(self.root, bd=3, state=DISABLED, fg='Green', relief=tk.SUNKEN)
        self.output_text.place(x=220, y=150, width=425, height=40)
        
        # Progress Display
        progress_label = tk.Label(
            self.root, 
            text='Progress:', 
            font=('Sans', '10', 'bold'), 
            bg='orange', 
            fg='black'
        )
        progress_label.place(x=20, y=210)
        
        self.progress_text = Text(
            self.root, 
            bd=3, 
            fg='black', 
            bg='white', 
            relief=tk.SUNKEN,
            font=('Courier', 9)
        )
        self.progress_text.place(x=20, y=240, width=625, height=80)
        
        # Convert Button
        run_button = tk.Button(
            self.root, 
            text="Convert to PDF", 
            fg="Green", 
            command=self.convert_html_to_pdf, 
            font=('Sans', '14', 'bold'), 
            bg='Light Gray'
        )
        run_button.place(x=20, y=340, width=250, height=40)
        
        # Exit Button
        exit_button = tk.Button(
            self.root, 
            text="Exit", 
            fg="Red", 
            command=self.root.destroy, 
            font=('Sans', '14', 'bold'), 
            bg='Light Gray'
        )
        exit_button.place(x=380, y=340, width=175, height=40)
    
    def browse_html(self):
        filename = filedialog.askopenfilename(
            initialdir="",
            title="Choose HTML file",
            filetypes=[("HTML files", "*.html"), ("All Files", "*.*")]
        )
        if filename:
            self.html_file_path = filename
            self.html_text.configure(state='normal')
            self.html_text.delete('1.0', END)
            self.html_text.insert('end', filename.replace("/", "\\"))
            self.html_text.configure(state='disabled')
            self.log(f"✓ Selected HTML file: {filename}")
    
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir.set(directory)
            self.log(f"✓ Output directory: {directory}")
    
    def log(self, message):
        self.progress_text.configure(state='normal')
        self.progress_text.insert(END, message + "\n")
        self.progress_text.see(END)
        self.progress_text.configure(state='disabled')
        self.root.update()
    
    def convert_html_to_pdf(self):
        if not self.html_file_path:
            messagebox.showerror("Error", "Please select an HTML file")
            return
        
        if not os.path.exists(self.html_file_path):
            messagebox.showerror("Error", "HTML file does not exist")
            return
        
        try:
            # Clear previous logs
            self.progress_text.configure(state='normal')
            self.progress_text.delete('1.0', END)
            self.progress_text.configure(state='disabled')
            
            self.log("=" * 60)
            self.log("Starting HTML to PDF Conversion")
            self.log("=" * 60)
            self.log(f"HTML File: {self.html_file_path}")
            
            # Read HTML content
            self.log("\n📄 Reading HTML file...")
            with open(self.html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            self.log(f"✓ HTML content loaded ({len(html_content)} characters)")
            
            # Convert to PDF
            self.log("\n🔄 Converting HTML to PDF...")
            pdf_bytes = self.converter.create_pdf_from_html(html_content)
            
            if pdf_bytes:
                # Generate output filename
                base_name = os.path.splitext(os.path.basename(self.html_file_path))[0]
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"{base_name}_{timestamp}.pdf"
                
                # Use same directory as HTML file
                output_dir = os.path.dirname(self.html_file_path)
                output_path = os.path.join(output_dir, output_filename)
                
                # Save PDF
                with open(output_path, 'wb') as f:
                    f.write(pdf_bytes)
                
                self.log(f"✓ PDF created successfully ({len(pdf_bytes)} bytes)")
                self.log(f"\n✅ Conversion Complete!")
                self.log(f"📁 Output: {output_path}")
                self.log("=" * 60)
                
                # Update output text field
                self.output_file_path = output_path
                self.output_text.configure(state='normal')
                self.output_text.delete('1.0', END)
                self.output_text.insert('end', output_path.replace("/", "\\"))
                self.output_text.configure(state='disabled')
                
                messagebox.showinfo(
                    "Success", 
                    f"PDF created successfully!\n\nOutput: {output_path}"
                )
            else:
                self.log("✗ Failed to create PDF")
                messagebox.showerror("Error", "Failed to convert HTML to PDF")
            
        except Exception as e:
            error_msg = f"Error during conversion: {str(e)}"
            self.log(f"\n✗ {error_msg}")
            messagebox.showerror("Error", error_msg)


def main():
    root = tk.Tk()
    app = HTMLToPDFApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
