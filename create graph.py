import os
import csv

def scanUserProfiles():
    volumes = [chr(i) + ":" for i in range(65, 91) if os.path.exists(chr(i) + ":")]
    user_profiles = []

    for volume in volumes:
        for root, dirs, files in os.walk(volume + "\\Users"):
            for dir in dirs:
                if dir.lower() != "public" and dir.lower() != "default":
                    user_profiles.append(os.path.join(root, dir))

    allowed_extensions = {'.wmv', '.jpg_large', '.sty', '.pdf', '.wav', '.cat', '.vec', '.svg', '.storyboard',
                          '.pptx', '.msg', '.eps', '.rmp', '.xls', '.pek', '.json', '.png', '.arff',
                          '.doc', '.txt', '.jfif', '.mov', '.uml', '.dotx', '.jpeg', '.cff', '.rar', '.cardtemplate',
                          '.pfx', '.avi', '.zip', '.docx', '.gif', '.bmp', '.mp4', '.mp3', '.jpg', '.odt', '.ppt',
                          '.flv', '.psd', '.rtf', '.accdb', '.xlsx', '.csv', '.cfa', '.tcl', '.ico', '.xltx',
                          '.ijg', '.pptm', '.m4a'}

    with open("file_info.csv", "w", newline="", encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename", "Extension", "File Size"])

        for profile in user_profiles:
            documents_dir = os.path.join(profile, "Documents")
            downloads_dir = os.path.join(profile, "Downloads")
            desktop_dir = os.path.join(profile, "Desktop")

            scanDirectory(writer, documents_dir, allowed_extensions)
            scanDirectory(writer, downloads_dir, allowed_extensions)
            scanDirectory(writer, desktop_dir, allowed_extensions)

def scanDirectory(writer, directory, allowed_extensions):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_name, file_extension = os.path.splitext(file)
            file_extension = file_extension.lower()

            if file_extension in allowed_extensions:
                file_size = os.path.getsize(file_path)
                writer.writerow([file_name, file_extension, file_size])

scanUserProfiles()
