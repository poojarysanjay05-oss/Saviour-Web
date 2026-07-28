#!/usr/bin/env python3
import re
import sys

def convert_dc_to_html(dc_content):
    """Convert Dynaboard .dc.html file to standalone HTML"""
    
    # Extract metadata from helmet section
    helmet_match = re.search(r'<helmet>(.*?)</helmet>', dc_content, re.DOTALL)
    helmet_content = helmet_match.group(1) if helmet_match else ""
    
    # Extract script content
    script_match = re.search(r'<script type="text/x-dc"[^>]*>(.*?)</script>', dc_content, re.DOTALL)
    script_content = script_match.group(1) if script_match else ""
    
    # Extract the main div content (between <div style="background:#0D0D0F"> and </div></x-dc>)
    main_match = re.search(r'<div style="background:#0D0D0F[^>]*>.*?(<header.*?)</x-dc>', dc_content, re.DOTALL)
    if not main_match:
        print("Error: Could not find main content div", file=sys.stderr)
        return None
    
    main_content_with_header = main_match.group(1)
    
    # Build the standalone HTML
    html_parts = [
        '<!DOCTYPE html>',
        '<html>',
        '<head>',
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
    ]
    
    # Add metadata from helmet
    if helmet_content:
        # Remove helmet tags and add content
        helmet_clean = helmet_content.strip()
        html_parts.append(helmet_clean)
    
    html_parts.extend([
        '</head>',
        '<body>',
        '<div style="background:#0D0D0F;overflow-x:hidden;min-height:100vh">',
        main_content_with_header,
        '</div>',
        '',
        '<script>',
        script_content,
        '</script>',
        '</body>',
        '</html>'
    ])
    
    return '\n'.join(html_parts)

# Read the original file
with open('ORIGINAL-Salary-Breakdown.dc.html', 'r') as f:
    content = f.read()

# Convert it
result = convert_dc_to_html(content)

if result:
    # Write the converted file
    with open('calculator-salary-breakdown.html', 'w') as f:
        f.write(result)
    print(f"Converted successfully. Output size: {len(result)} bytes")
else:
    print("Conversion failed")
    sys.exit(1)
