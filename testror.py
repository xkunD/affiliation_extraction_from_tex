import json

# Keywords to check for
institution_keywords = ['University', 'Institute', 'Research', 'College', 'Laboratory', 'Center', 'School']

# Function to check if any of the institution names contain the keywords
def contains_keywords(names, keywords):
    for name_entry in names:
        name = name_entry['value']
        for keyword in keywords:
            if keyword in name:
                return True
    return False

# Load the ROR data (assuming 'ror.json' is the filename)
with open('ror.json', 'r') as file:
    institutions_data = json.load(file)

# Initialize counters for statistics
total_institutions = 0
containing_keywords = 0
not_containing_keywords = 0

# Loop through the data to check each institution's names
for institution in institutions_data:
    total_institutions += 1
    institution_names = institution['names']

    if contains_keywords(institution_names, institution_keywords):
        containing_keywords += 1
    else:
        not_containing_keywords += 1
        # Print the institution's primary name (or first name) if no keyword is found
        print(f"Keyword not found in institution: {institution_names[0]['value']}")

# Calculate proportions
if total_institutions > 0:
    containing_proportion = (containing_keywords / total_institutions) * 100
    not_containing_proportion = (not_containing_keywords / total_institutions) * 100
else:
    containing_proportion = 0
    not_containing_proportion = 0

# Print the summary statistics
print("\nSummary:")
print(f"Total institutions: {total_institutions}")
print(f"Institution names containing keywords: {containing_keywords} ({containing_proportion:.2f}%)")
print(f"Institution names not containing keywords: {not_containing_keywords} ({not_containing_proportion:.2f}%)")
