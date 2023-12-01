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

# Specify file extensions to include (excluding XML and YAML)
$fileExtensions = @('.wmv', '.jpg_large', '.sty', '.pdf', '.wav', '.cat', '.vec', '.svg', '.storyboard',
                   '.pptx', '.msg', '.eps', '.rmp', '.xls', '.pek', '.json', '.png', '.arff',
                   '.doc', '.txt', '.jfif', '.mov', '.uml', '.dotx', '.jpeg', '.cff', '.rar', '.cardtemplate',
                   '.pfx', '.avi', '.zip', '.docx', '.gif', '.bmp', '.mp4', '.mp3', '.jpg', '.odt', '.ppt',
                   '.flv', '.psd', '.rtf', '.accdb', '.xlsx', '.csv', '.cfa', '.tcl', '.ico', '.xltx',
                   '.ijg', '.pptm', '.m4a')

# Create a hashtable to store total file size per user profile
$profileFileSizes = @{}

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

            # Initialize total size for the user profile
            $totalSize = 0

            # Iterate through each directory and extract file size
            foreach ($directory in $directoriesToScan) {
                Write-Host "Processing directory: $directory"

                # Get all files in the directory and its subdirectories with specified extensions
                $files = Get-ChildItem -Path $directory -Recurse -File | Where-Object { $_.Extension -in $fileExtensions }

                # Iterate through each file and extract file size
                foreach ($file in $files) {
                    $fileSize = Get-FileSize -filePath $file.FullName

                    if ($null -ne $fileSize) {
                        # Add file size to the total for the user profile
                        $totalSize += $fileSize
                    }
                }
            }

            # Add the total size to the hashtable for the user profile
            $profileFileSizes[$userProfile.Name] = $totalSize
        }
        else {
            Write-Host "User profile path does not exist: $userProfilePath"
        }
    }
}

# Create an array to store CSV data
$csvData = @()

# Iterate through each user profile to create CSV data
foreach ($userProfileName in $profileFileSizes.Keys) {
    $totalSizeGB = [math]::Round($profileFileSizes[$userProfileName] / 1GB, 2)
    #below is for Gigabytes, above is for Gibibytes
    #$totalSizeGB = [math]::Round($profileFileSizes[$userProfileName] / 1000/1000/1000, 2)

    $csvData += [PSCustomObject]@{
        'UserProfile' = $userProfileName
        'TotalSizeGB' = $totalSizeGB
    }
}

# Define the CSV file path on the desktop
$csvFileName = "filesize_byuser_AllVolumes.csv"
$csvFilePath = [System.IO.Path]::Combine($env:USERPROFILE, 'Desktop', $csvFileName)

# Export the modified CSV data to a CSV file
$csvData | Export-Csv -Path $csvFilePath -NoTypeInformation

Write-Host "CSV file created at: $csvFilePath"
