import csv

def extract_h_column(csv_file, txt_file):
    with open(csv_file, 'r', newline='', encoding='utf-8') as infile, \
         open(txt_file, 'w', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile)
        
        for row in reader:
            if len(row) > 7:  # Make sure column H exists
                h_value = row[7].strip()
                if h_value:
                    outfile.write(h_value + '\n')

    print(f"✅ Column H copied to {txt_file}")

# Example usage
extract_h_column('input.csv', 'websites.txt')