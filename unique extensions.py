import csv
import os

def get_unique_extensions(csv_file_path):
    unique_extensions = set()

    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            # Assuming the CSV file has a column named 'FilePath'
            file_path = row['File']

            # Extract the file extension
            _, file_extension = os.path.splitext(file_path)

            # Add the file extension to the set
            unique_extensions.add(file_extension.lower())

    return unique_extensions

# Example usage
csv_file_path = 'C:/Users/fahmi/Desktop/file_size_report_fahmi.csv'
extensions = get_unique_extensions(csv_file_path)

print("Unique File Extensions:")
for ext in extensions:
    print(ext)