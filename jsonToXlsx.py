import os
import json
import pandas as pd

# Specify the folder where your JSON files are stored
folder_path = './'

# List to hold specific data from each JSON
filtered_data = []

# Iterate over all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):  # Check if the file is a JSON
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            # Extract the 'contents' list from the JSON
            contents = data.get('contents', [])
            print(len(contents))
            
            # Iterate over each item in the 'contents' list
            for item in contents:
                # Extract specific fields (modify these as needed)
                filtered_item = {
                    'id': item.get('id'),
                    'reviewScore': item.get('reviewScore'),
                    'reviewContent': item.get('reviewContent'),
                    'createDate': item.get('createDate'),
                    'productOption': item.get("productOptionContent")
                    
                }
                
                # Append the filtered data to the list
                filtered_data.append(filtered_item)

# Create a pandas DataFrame from the filtered data
df = pd.DataFrame(filtered_data)

# Specify the output Excel file path
output_excel_path = './filtered_data.xlsx'

# Write the DataFrame to an Excel file
df.to_excel(output_excel_path, index=False)

print(f"Excel file saved to {output_excel_path}")
