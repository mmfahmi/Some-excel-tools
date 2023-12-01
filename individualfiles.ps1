# Set execution policy to RemoteSigned
Set-ExecutionPolicy RemoteSigned -Scope Process -Force

# Function to extract file size
function Get-FileSize {
    param (
        [string]$filePath
    )

    try {
        $fileInfo = Get-Item $filePath
        return $fileInfo.Length
    }
    catch {
        Write-Host "Error processing file: $filePath - $($_.Exception.Message)"
        return $null
    }
}

# Function to generate directory tree
function Get-DirectoryTree {
    param (
        [string]$rootPath
    )

    $directoryTree = @("$rootPath")

    Get-ChildItem -Path $rootPath -Recurse | Where-Object { $_.PSIsContainer } | ForEach-Object {
        $indentation = "| " * ($_.FullName.Split('\').Length - $rootPath.Split('\').Length)
        $directoryTree += "$indentation$($_.Name)"
    }

    return $directoryTree
}

# Specify file extensions to include (excluding XML and YAML)
$fileExtensions = @('.wmv', '.jpg_large', '.sty', '.pdf', '.wav', '.cat', '.vec', '.svg', '.storyboard',
                   '.pptx', '.msg', '.eps', '.rmp', '.xls', '.pek', '.json', '.png', '.arff',
                   '.doc', '.txt', '.jfif', '.mov', '.uml', '.dotx', '.jpeg', '.cff', '.rar', '.cardtemplate',
                   '.pfx', '.avi', '.zip', '.docx', '.gif', '.bmp', '.mp4', '.mp3', '.jpg', '.odt', '.ppt',
                   '.flv', '.psd', '.rtf', '.accdb', '.xlsx', '.csv', '.cfa', '.tcl', '.ico', '.xltx',
                   '.ijg', '.pptm', '.m4a')

# Create an array to store CSV data
$csvData = @()

# Create a string to store the directory tree
$directoryTree = @()

# Get all disk volumes
$diskVolumes = Get-WmiObject Win32_LogicalDisk | Where-Object { $_.DriveType -eq 3 } | Select-Object -ExpandProperty DeviceID

# Iterate through each volume
foreach ($volume in $diskVolumes) {
    # Get all user profiles on the current volume
    $userProfiles = Get-ChildItem -Path "$volume\Users" -Directory | Where-Object { $_.Name -ne 'Public' -and $_.Name -ne 'Default' }

    # Iterate through each user profile
    foreach ($userProfile in $userProfiles) {
        $userProfilePath = Join-Path -Path $volume -ChildPath "Users\$($userProfile.Name)"

        # Check if the user profile path exists
        if (Test-Path $userProfilePath) {
            # Specify directories to scan
            $directoriesToScan = @(
                [System.IO.Path]::Combine($userProfilePath, 'Documents'),
                [System.IO.Path]::Combine($userProfilePath, 'Downloads'),
                [System.IO.Path]::Combine($userProfilePath, 'Desktop')
            )

            # Iterate through each directory and extract file size
            foreach ($directory in $directoriesToScan) {
                Write-Host "Processing directory: $directory"

                # Generate directory tree for each specified directory
                $directoryTree += Get-DirectoryTree -rootPath $directory

                # Get all files in the directory and its subdirectories with specified extensions
                $files = Get-ChildItem -Path $directory -Recurse -File | Where-Object { $_.Extension -in $fileExtensions }

                # Iterate through each file and extract file size
                foreach ($file in $files) {
                    $fileSize = Get-FileSize -filePath $file.FullName

                    if ($fileSize -ne $null) {
                        # Add file information to the CSV data array
                        $csvData += [PSCustomObject]@{
                            'File'      = $file.FullName
                            'Extension' = $file.Extension
                            'Size'      = $fileSize
                        }
                    }
                }
            }
        }
        else {
            Write-Host "User profile path does not exist: $userProfilePath"
        }
    }
}

# Define the CSV file path on the desktop
$csvFileName = "file_size_report_AllVolumes.csv"
$csvFilePath = [System.IO.Path]::Combine($env:USERPROFILE, 'Desktop', $csvFileName)

# Define the directory tree file path on the desktop
$treeFileName = "directory_tree_AllVolumes.txt"
$treeFilePath = [System.IO.Path]::Combine($env:USERPROFILE, 'Desktop', $treeFileName)

# Export the CSV data to a CSV file
$csvData | Export-Csv -Path $csvFilePath -NoTypeInformation

# Export the directory tree to a text file
$directoryTree | Out-File -FilePath $treeFilePath

Write-Host "CSV file created at: $csvFilePath"
Write-Host "Directory tree saved at: $treeFilePath"
