import csv
import os
from bs4 import BeautifulSoup

def html_to_csv(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the table
    table = soup.find('table', {'id': 'assignmentDatatable'})
    if not table:
        # Fallback if id is not found, try finding the first table
        table = soup.find('table')
        if not table:
            print("Error: No table found in the HTML.")
            return

    # Extract headers
    headers = []
    thead = table.find('thead')
    if thead:
        header_row = thead.find('tr')
        if header_row:
            cols = header_row.find_all(['th', 'td'])
            for col in cols:
                # Remove checkbox text if any, or just get text
                text = col.get_text(strip=True)
                # If the column contains a checkbox input, we might want to skip or label it
                if col.find('input', {'type': 'checkbox'}):
                    text = "Checkbox" if not text else text
                headers.append(text)
        # Add a header for the extracted link
        headers.append("Assignment Link")

    # Extract rows
    rows = []
    tbody = table.find('tbody')
    if tbody:
        tr_elements = tbody.find_all('tr')
        for tr in tr_elements:
            # Check for "No matching records found" row (usually in a td with class dataTables_empty)
            is_empty_row = False
            for td in tr.find_all('td'):
                if 'dataTables_empty' in td.get('class', []):
                    is_empty_row = True
                    break
            if is_empty_row:
                continue
                
            row_data = []
            # We will also look for the specific assignment link in this row
            assignment_link = ""
            
            cols = tr.find_all('td')
            for col in cols:
                # Handle nested elements like links or inputs
                # Extract link if present and looks like the assignment detail
                link_tag = col.find('a', href=True)
                if link_tag and '/assignment-detail/' in link_tag['href']:
                    assignment_link = link_tag['href'].replace('/survey-collection/assignment-detail/', '')

                # If it's a checkbox column
                if col.find('input', {'type': 'checkbox'}):
                    val = col.find('input').get('value', '')
                    # or just mark as Checkbox present
                    # row_data.append(val)
                    # For this specific request, user wants "neat csv", maybe just ignore the checkbox column content or keep empty
                    row_data.append("") 
                else:
                    text = col.get_text(separator=' ', strip=True)
                    row_data.append(text)
            
            # Only add row if it's not empty and matches header length (mostly)
            if row_data:
                # Append the extracted link to the end of the row
                row_data.append(assignment_link)
                rows.append(row_data)

    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if headers:
            writer.writerow(headers)
        writer.writerows(rows)

    print(f"Successfully converted '{input_file}' to '{output_file}'.")
    print(f"Rows extracted: {len(rows)}")

if __name__ == "__main__":
    input_path = "input.txt"
    output_path = "output.csv"
    html_to_csv(input_path, output_path)
