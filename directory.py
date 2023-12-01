import os
import csv
import matplotlib.pyplot as plt


#scanning for user profiles
def scanUserProfiles():
    
    #checking for available volumes
    volumes = [chr(i) + ":" for i in range(65, 91) if os.path.exists(chr(i) + ":")]
    user_profiles = []

    #scanning for user profiles
    for volume in volumes:
        for root, dirs, files in os.walk(volume + "\\Users"):
            for dir in dirs:
                if dir.lower() != "public" and dir.lower() != "default":
                    user_profiles.append(os.path.join(root, dir))
                    
    #list of allowed extensions
    allowed_extensions = {'.wmv', '.jpg_large', '.sty', '.pdf', '.wav', '.cat', '.vec', '.svg', '.storyboard',
                          '.pptx', '.msg', '.eps', '.rmp', '.xls', '.pek', '.json', '.png', '.arff',
                          '.doc', '.txt', '.jfif', '.mov', '.uml', '.dotx', '.jpeg', '.cff', '.rar', '.cardtemplate',
                          '.pfx', '.avi', '.zip', '.docx', '.gif', '.bmp', '.mp4', '.mp3', '.jpg', '.odt', '.ppt',
                          '.flv', '.psd', '.rtf', '.accdb', '.xlsx', '.csv', '.cfa', '.tcl', '.ico', '.xltx',
                          '.ijg', '.pptm', '.m4a'}

    #creating csv file
    with open("file_info.csv", "w", newline="", encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename", "Extension", "File Size"])

        for profile in user_profiles:
            documents_dir = os.path.join(profile, "Documents")
            downloads_dir = os.path.join(profile, "Downloads")
            desktop_dir = os.path.join(profile, "Desktop")
            print(documents_dir, downloads_dir, desktop_dir)

            scanDirectory(writer, documents_dir, allowed_extensions)
            scanDirectory(writer, downloads_dir, allowed_extensions)
            scanDirectory(writer, desktop_dir, allowed_extensions)
        print("Csv file created successfully.")   

#scanning for files in a directory
def scanDirectory(writer, directory, allowed_extensions):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_name, file_extension = os.path.splitext(file)
            file_extension = file_extension.lower()

            if file_extension in allowed_extensions:
                file_size = os.path.getsize(file_path)
                writer.writerow([file_name, file_extension, file_size])

def visualizeTreeChart(directory, output_file):
    fig, ax = plt.subplots(figsize=(10, 6))
    for root, dirs, files in os.walk(directory):
        level = root.replace(directory, '').count(os.sep)
        indent = ' ' * 4 * (level)
        ax.text(level, 0, '{}{}/'.format(indent, os.path.basename(root)), fontsize=10, ha='left', va='center')
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            ax.text(level + 1, 0, '{}{}'.format(sub_indent, file), fontsize=8, ha='left', va='center')
    
    ax.axis('off')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close(fig)

scanUserProfiles()
visualizeTreeChart("C:/Users/fahmi/Documents/Repo/Some excel tools", "tree_chart.png")
 