import argparse
import subprocess
import os
from weasyprint import HTML

def convert_to_pdf(input_file, output_file=None, css_file=None, keep=False, debug=False):
    # Check if input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' not found")
    
    # Check if CSS file exists when specified
    if css_file and not os.path.exists(css_file):
        raise FileNotFoundError(f"CSS file '{css_file}' not found")
    
    # Get base filename without extension
    base_name = os.path.splitext(input_file)[0]
    if debug:
        print(f'The file name is {base_name}.')
    # Set default output filename if none provided
    if output_file is None:
        output_file = f"{base_name}.pdf"
        if debug:
            print(f'The output file is {output_file}')
    
    # Create temporary HTML file path
    temp_html = f"{base_name}_temp.html"
    if debug:
        print(f'The temporary file is {temp_html}.')
    
    # Prepare pandoc command
    pandoc_cmd = ["pandoc", "-s", input_file, "-o", temp_html]
    if css_file:
        pandoc_cmd.extend(["-c", css_file])

    if debug:
        print(f'The command I will run is: "{" ".join(pandoc_cmd)}')
    
    try:
        # Convert markdown to HTML using pandoc
        subprocess.run(pandoc_cmd, check=True)
        
        # Convert HTML to PDF using weasyprint
        HTML(filename=temp_html).write_pdf(output_file)
        
        # Clean up temporary HTML file
        
        if not keep:
            os.remove(temp_html)
        
        print(f"Successfully created {output_file}")
        if keep:
            print(f"Kept the transitional HTML file {temp_html} as requested")
        
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        if os.path.exists(temp_html):
            os.remove(temp_html)
        raise

def main():
    parser = argparse.ArgumentParser(description='Convert markdown to PDF via HTML')
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('-o', '--output', help='Output PDF file')
    parser.add_argument('-c', '--css', help='CSS stylesheet file')
    parser.add_argument('-k', '--keep', action='store_true', help='Keep the temporary HTML file')
    parser.add_argument('-d', '--debug', action='store_true', help='debug, show commands')
    
    args = parser.parse_args()
    
    convert_to_pdf(args.input, args.output, args.css, args.keep, args.debug)

if __name__ == "__main__":
    main()