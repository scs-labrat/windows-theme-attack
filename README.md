# Theme-Attack: NTLM Authentication Capture with Steganography

## Overview

This project demonstrates an attack that leverages Windows theme files (`.theme`) in conjunction with NTLM credential capture and steganography. The attack has two main parts:

1. **NTLM Authentication Capture**: Utilizing the `.theme` file to connect to an attacker's SMB server, enabling the capture of NTLM hashes using tools like Responder.
2. **Steganographic Payload Delivery**: Embedding a PowerShell script into an image file using steganography, which is then executed through the `.theme` file.

This attack demonstrates how a seemingly harmless `.theme` file can be used to trick users into executing malicious code and exposing their credentials.

## Components

- **NTLM Capture**: The `.theme` file is configured to load a remote wallpaper from an SMB server under the attacker's control. When Windows attempts to load the wallpaper, it will send the user's NTLM hash to authenticate with the SMB server. Tools like **Responder** can be used to capture these hashes.

- **Steganographic Sub-Attack**: The attack also includes embedding a PowerShell payload into an image using Base64 encoding. The payload is extracted and executed in-memory, making it difficult to detect. This serves as a secondary attack vector that can be leveraged to perform additional actions on the target machine.

## Attack Flow

### Create Steganographic Image

- The PowerShell script provided prompts the user for a `.ps1` script to encode and an image to use as the carrier.
- The script encodes the PowerShell script into Base64 and appends it to the image file.

### Create Theme File

- A Windows `.theme` file is generated with settings to use the steganographic image as the desktop wallpaper and execute a hidden PowerShell command.
- The PowerShell command is encoded in Base64 and is responsible for extracting and executing the payload hidden in the image.

### NTLM Capture

- The `.theme` file also points to a remote SMB server for the wallpaper (e.g., `\\192.168.1.103\wallpaper.jpg`).
- When the target user applies the theme, the system will try to access the SMB share, sending the user's NTLM credentials, which can be captured by tools like **Responder**.

### Host the Files

- The script starts a simple Python HTTP server to host the generated `.theme` and image files, making it easy for the target user to download and execute them.

## Requirements

- **Python 3**: Used to run the script and host the files via a simple HTTP server.
- **Responder**: A tool that captures NTLM hashes from incoming SMB authentication requests.
- **Linux System**: The provided script is written in Python for Linux environments.

## Detailed Steps

### Generate Steganographic Image and Theme File

1. Run the provided Python script (`theme_attack.py`).
2. The script will prompt you for:
   - Path to the PowerShell script (`.ps1`) you wish to encode.
   - Path to an image file (`.jpg`) that will be used for steganography.
   - Output filenames and network location.
3. The script will output a `.theme` file and a steganographic image in the `~/theme-attack` directory.

### Host the Files

- The script will automatically host these files using a simple HTTP server (`python3 -m http.server 8080`).
- You can share the link to the theme file (e.g., `http://<attacker-ip>:8080/custom_theme.theme`) with your target.

### Capture NTLM Hashes

- Use **Responder** on the attacker's machine to listen for incoming SMB requests and capture the NTLM hashes.
- Run Responder in the local network:
  ```bash
  sudo responder -I eth0
    ```
## Directory Structure

- **theme_attack.py**: Main Python script to create the steganographic image and theme file.
- **theme_attack.ps1**: PowerShell script used for Windows systems to create the steganographic image and theme file.
- **custom_theme.theme**: The generated Windows theme file.
- **steganographic_image.jpg**: The image with the embedded payload.

## Usage

### For Python (Linux)

```bash
python3 theme_attack.py
```

Follow the prompts to generate the necessary files, then host them using the Python HTTP server.

For PowerShell (Windows)

```powershell
Copy code
.\theme_attack.ps1
```

Run the PowerShell script to generate the necessary files.

## Notes
Steganography in this context is used to hide a PowerShell script within an image, making it less likely to be detected by standard security tools.

NTLM hash capture using Responder is a well-known attack technique, but it remains effective due to the continued reliance on NTLM in many environments.