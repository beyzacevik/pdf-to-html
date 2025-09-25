from docling.document_converter import DocumentConverter
import os 
import requests
import ssl
from pathlib import Path


def download_pdf_with_ssl_bypass(url, local_path):
    """Download PDF from URL with SSL verification disabled"""
    print(f"Downloading PDF from: {url}")
    
    # Disable SSL verification for requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    response = requests.get(url, verify=False)
    response.raise_for_status()
    
    with open(local_path, 'wb') as f:
        f.write(response.content)
    
    print(f"PDF downloaded successfully to: {local_path}")
    return local_path

def process_pdf_to_html(pdf_path, output_dir):
    """Process PDF using docling and export to HTML"""
    print("Processing PDF with docling...")
    
    # Initialize converter with default settings
    converter = DocumentConverter()
    
    # Convert PDF
    print("Converting PDF document...")
    result = converter.convert(pdf_path)
    doc = result.document
    
    # Export to HTML
    print("Exporting to HTML...")
    html_content = doc.export_to_html()
    
    # Create output path
    pdf_name = Path(pdf_path).stem
    html_output_path = os.path.join(output_dir, f"{pdf_name}.html")
    
    # Write HTML file
    with open(html_output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML content length: {len(html_content)} characters")
    print(f"Successfully exported to: {html_output_path}")
    
    return html_output_path, html_content

def main():
    # Use a simple PDF URL
    pdf_url = "https://arxiv.org/pdf/2505.14683"
    
    # Setup paths
    current_dir = os.path.dirname(__file__)
    pdf_local_path = os.path.join(current_dir, "sample.pdf")
    
    try:
        # Download PDF
        download_pdf_with_ssl_bypass(pdf_url, pdf_local_path)
            
        # Process PDF to HTML
        html_path, html_content = process_pdf_to_html(pdf_local_path, current_dir)
        
        # Show preview of HTML content
        print("\nFirst 800 characters of HTML output:")
        print(html_content[:800])
        print("\n" + "="*50)
        print(f"Processing complete! HTML file saved at: {html_path}")
        
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
