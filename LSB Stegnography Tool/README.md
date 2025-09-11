# 🔐 LSB Steganography Tool

A simple Python GUI application that allows you to hide (encode) and extract (decode) secret messages inside images using **Least Significant Bit (LSB) steganography**.  
This version also supports **Base64 encoding** as an extra option to make messages harder to interpret.


## 🚀 Features
- Encode secret messages into PNG, JPG, or BMP images  
- Decode hidden messages from encoded images  
- Optional **Base64 encoding/decoding** for added obfuscation  
- User-friendly **GUI built with PyQt5**  
- Saves the output image as `encoded.png` in the same folder

- ## ⚙️ Installation Guide  

### 1. Clone the repository  
Download the project to your computer:  

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>/projects/LSB-Steganography-Tool

###2.Install required dependencies

   -pip install -r requirements.txt

###3.Run the application

   - python3 lsb.py

###4.How to use

   - Select an image file (.png, .jpg, .bmp)

   - Choose Encode or Decode

      -If encoding:

         - Enter your secret message

         - Optionally check Base64 encoding

   - Click Process → A new image called encoded.png will be created

      -If decoding:

         - Select the encoded image

         - Click Process → The hidden message will be displayed


