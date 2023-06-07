import csv
import json
import os
# Define the mapping from CSV categories to JSON tags
category_tag_mapping = {
    'ACCOUNT': 'complaint',
    'CANCELLATION_FEE': 'returns',
    'CONTACT': 'technical_support',
    'DELIVERY': 'delivery',
    'FEEDBACK': 'complaint',
    'INVOICES': 'payments',
    'NEWSLETTER': 'news',
    'ORDER': 'orders',
    'PAYMENT': 'payments',
    'REFUNDS': 'returns',
    'SHIPPING': 'delivery',
    # Add more mappings as necessary
}

# Open the JSON file and load the data
with open('itech_chat/intents.json', 'r') as f:
    data = json.load(f)

data_list = data['intents']


data_dict = {d['tag']: d for d in data_list}
current_directory = os.getcwd()

csv_file_path = os.path.join(current_directory, '20000-Utterances-Training-dataset-for-chatbots-virtual-assistant-Bitext-sample', '20000-Utterances-Training-dataset-for-chatbots-virtual-assistant-Bitext-sample.csv')
with open(csv_file_path, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header

    for row in reader:
        flags, pattern, category, response = row


        tag = category_tag_mapping.get(category)

        if tag not in data_dict:
            data_dict[tag] = {"tag": tag, "patterns": [], "responses": []}

        
        data_dict[tag]["patterns"].append(pattern)
        # data_dict[tag]["responses"].append(response)

# Convert the dictionary values back to a list
data = list(data_dict.values())

# Write the updated data back to the JSON file
with open('itech_chat/intents.json', 'w') as f:
    json.dump(data, f, indent=2)
