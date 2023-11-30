import os
import csv
import matplotlib.pyplot as plt
import string

# Function to extract file size
def get_file_size(file_path):
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        print(f"Error processing file: {file_path} - {str(e)}")
        return None

# Function to generate directory tree
def get_directory_tree(root_path):
    directory_tree = [root_path]

    for foldername, subfolders, filenames in os.walk(root_path):
        indentation = "| " * (len(foldername.split(os.sep)) - len(root_path.split(os.sep)))
        directory_tree.append(f"{indentation}{os.path.basename(foldername)}")

    return directory_tree

# Specify file extensions to include (excluding XML and YAML)
file_extensions = {'.wmv', '.jpg_large', '.sty', '.pdf', '.wav', '.cat', '.vec', '.svg', '.storyboard',
                   '.pptx', '.msg', '.eps', '.rmp', '.xls', '.pek', '.json', '.png', '.arff',
                   '.doc', '.txt', '.jfif', '.mov', '.uml', '.dotx', '.jpeg', '.cff', '.rar', '.cardtemplate',
                   '.pfx', '.avi', '.zip', '.docx', '.gif', '.bmp', '.mp4', '.mp3', '.jpg', '.odt', '.ppt',
                   '.flv', '.psd', '.rtf', '.accdb', '.xlsx', '.csv', '.cfa', '.tcl', '.ico', '.xltx',
                   '.ijg', '.pptm', '.m4a'}

# Create an array to store CSV data
csv_data = []

# Get all drive letters
drive_letters = [letter + ":" for letter in string.ascii_uppercase if os.path.exists(letter + ":")]

# Get disk volumes for existing drive letters
disk_volumes = [os.path.join(letter, "") for letter in drive_letters]

# Get all disk volumes
disk_volumes = [volume for volume in os.popen("wmic logicaldisk get caption").read().split()[1:] if volume]

# Iterate through each volume
for volume in disk_volumes:
    # Get all user profiles on the current volume
    user_profiles = [user for user in os.listdir(os.path.join(volume, "Users\\")) if user not in ['Public', 'Default']]

    # Iterate through each user profile
    for user_profile in user_profiles:
        user_profile_path = os.path.join(volume, "Users", user_profile)

        # Check if the user profile path exists
        if os.path.exists(user_profile_path):
            # Specify directories to scan
            directories_to_scan = [
                os.path.join(user_profile_path, 'Documents'),
                os.path.join(user_profile_path, 'Downloads'),
                os.path.join(user_profile_path, 'Desktop')
            ]

            # Iterate through each directory and extract file size
            for directory in directories_to_scan:
                print(f"Processing directory: {directory}")

                # Generate directory tree for each specified directory
                directory_tree += get_directory_tree(directory)

                # Get all files in the directory and its subdirectories with specified extensions
                files = [file for file in glob.glob(os.path.join(directory, '**', '*'), recursive=True) if os.path.isfile(file) and os.path.splitext(file)[1].lower() in file_extensions]

                # Iterate through each file and extract file size
                for file in files:
                    file_size = get_file_size(file)

                    if file_size is not None:
                        # Add file information to the CSV data list
                        csv_data.append({
                            'File': file,
                            'Extension': os.path.splitext(file)[1],
                            'Size': file_size
                        })

# Define the CSV file path on the desktop
csv_file_name = f"file_size_report_AllVolumes.csv"
csv_file_path = os.path.join(os.path.expanduser("~"), "Desktop", csv_file_name)

# Export the CSV data to a CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
    fieldnames = ['File', 'Extension', 'Size']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(csv_data)

print(f"CSV file created at: {csv_file_path}")

# Visualization
sizes = [data['Size'] for data in csv_data]
labels = [os.path.basename(data['File']) for data in csv_data]

plt.figure(figsize=(10, 6))
plt.barh(labels, sizes, color='blue')
plt.xlabel('File Size (Bytes)')
plt.ylabel('File')
plt.title('File Sizes')
plt.tight_layout()
plt.show()
