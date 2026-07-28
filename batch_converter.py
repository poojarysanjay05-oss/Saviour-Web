#!/usr/bin/env python3
import re
import glob
import os

def convert_dc_to_html(dc_content):
    """Convert Dynaboard .dc.html file to standalone HTML"""
    
    # Extract metadata from helmet section
    helmet_match = re.search(r'<helmet>(.*?)</helmet>', dc_content, re.DOTALL)
    helmet_content = helmet_match.group(1) if helmet_match else ""
    
    # Extract script content
    script_match = re.search(r'<script type="text/x-dc"[^>]*>(.*?)</script>', dc_content, re.DOTALL)
    script_content = script_match.group(1) if script_match else ""
    
    # Extract the main div content
    main_match = re.search(r'<div style="background:#0D0D0F[^>]*>.*?(<header.*?)</x-dc>', dc_content, re.DOTALL)
    if not main_match:
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

# Mapping of ORIGINAL filenames to output calculator filenames
mapping = {
    'ORIGINAL-50-30-20-Budget.dc.html': 'calculator-50-30-20-budget.html',
    'ORIGINAL-Annual-Income.dc.html': 'calculator-annual-income.html',
    'ORIGINAL-Daily-Savings.dc.html': 'calculator-daily-savings.html',
    'ORIGINAL-Dining-Out.dc.html': 'calculator-dining-out.html',
    'ORIGINAL-Emergency-Fund.dc.html': 'calculator-emergency-fund.html',
    'ORIGINAL-EMI.dc.html': 'calculator-emi.html',
    'ORIGINAL-Expense-Split.dc.html': 'calculator-expense-split.html',
    'ORIGINAL-Fuel-Cost.dc.html': 'calculator-fuel-cost.html',
    'ORIGINAL-Interest.dc.html': 'calculator-interest.html',
    'ORIGINAL-Loan-Affordability.dc.html': 'calculator-loan-affordability.html',
    'ORIGINAL-Monthly-Budget.dc.html': 'calculator-monthly-budget.html',
    'ORIGINAL-Retirement-Savings.dc.html': 'calculator-retirement-savings.html',
    'ORIGINAL-Salary-Breakdown.dc.html': 'calculator-salary-breakdown.html',
    'ORIGINAL-Savings-Goal.dc.html': 'calculator-savings-goal.html',
    'ORIGINAL-Subscription-Cost.dc.html': 'calculator-subscription-cost.html',
    'ORIGINAL-Take-Home-Salary.dc.html': 'calculator-take-home-salary.html',
    'ORIGINAL-Travel-Budget.dc.html': 'calculator-travel-budget.html',
    'ORIGINAL-Vacation-Savings.dc.html': 'calculator-vacation-savings.html',
}

successes = 0
failures = 0

for orig_file, output_file in mapping.items():
    if not os.path.exists(orig_file):
        print(f"❌ {orig_file}: NOT FOUND")
        failures += 1
        continue
    
    try:
        with open(orig_file, 'r', encoding='utf-8') as f:
            dc_content = f.read()
        
        result = convert_dc_to_html(dc_content)
        if result:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            size = len(result)
            print(f"✓ {output_file}: {size} bytes")
            successes += 1
        else:
            print(f"❌ {output_file}: Conversion failed")
            failures += 1
    except Exception as e:
        print(f"❌ {output_file}: {str(e)}")
        failures += 1

print(f"\nSummary: {successes} converted, {failures} failed")
