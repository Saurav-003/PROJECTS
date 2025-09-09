import sys
import os
import base64  # For Base64 encoding/decoding
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFileDialog, 
                             QRadioButton, QTextEdit, QCheckBox)
from PyQt5.QtGui import QColor
from PIL import Image

# Main GUI application class
class LSBStegoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LSB Steganography Tool")
        self.setGeometry(100, 100, 400, 450)
        self.setStyleSheet("background-color: #FFCCCC;")

        layout = QVBoxLayout()

        # Input field for image path
        self.image_path_input = QLineEdit()
        self.image_path_input.setPlaceholderText("Enter the path to the image")
        layout.addWidget(self.image_path_input)

        # Browse button to select image
        self.browse_button = QPushButton("Browse")
        self.browse_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.browse_button.clicked.connect(self.browse_image)
        layout.addWidget(self.browse_button)

        # Text area to type message or view decoded message
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Enter or view the message")
        layout.addWidget(self.message_input)

        # Encode/Decode radio buttons
        self.encode_radio = QRadioButton("Encode")
        layout.addWidget(self.encode_radio)
        self.decode_radio = QRadioButton("Decode")
        layout.addWidget(self.decode_radio)

        # Base64 encoding checkbox
        self.base64_checkbox = QCheckBox("Use Base64 Encoding/Decoding")
        layout.addWidget(self.base64_checkbox)

        # Process button
        self.process_button = QPushButton("Process")
        self.process_button.setStyleSheet("background-color: #008CBA; color: white;")
        self.process_button.clicked.connect(self.process)
        layout.addWidget(self.process_button)

        # Result label
        self.result_label = QLabel()
        self.result_label.setStyleSheet("color: blue;")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    # Function to browse and select image
    def browse_image(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Image files (*.png *.jpg *.bmp)")
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            self.image_path_input.setText(selected_files[0])

    # Function to handle Encode/Decode
    def process(self):
        image_path = self.image_path_input.text()

        if not os.path.isfile(image_path):
            QMessageBox.warning(self, "Error", "Invalid image path")
            return

        # Encode message
        if self.encode_radio.isChecked():
            message = self.message_input.toPlainText()

            # Apply Base64 if checked
            if self.base64_checkbox.isChecked():
                message = base64.b64encode(message.encode()).decode()

            encode_lsb(image_path, message)
            self.result_label.setText("Message encoded successfully")

        # Decode message
        elif self.decode_radio.isChecked():
            decoded_message = decode_lsb(image_path)
            if decoded_message is not None:
                # Decode Base64 if checked
                if self.base64_checkbox.isChecked():
                    try:
                        decoded_message = base64.b64decode(decoded_message.encode()).decode()
                    except Exception as e:
                        self.result_label.setText("Error decoding Base64: " + str(e))
                        return

                self.result_label.setText("Decoded message: " + decoded_message)
            else:
                self.result_label.setText("No message found in the image")

        else:
            QMessageBox.warning(self, "Error", "Please select whether to encode or decode")

# Convert message to binary
def message_to_bin(message):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    return binary_message

# Encode message into image
def encode_lsb(image_path, message):
    img = Image.open(image_path)
    width, height = img.size

    binary_message = message_to_bin(message)
    binary_message += '1111111111111110'  # Sentinel to mark end

    if len(binary_message) > width * height * 3:
        raise Exception("Message too long to encode in the given image")

    data_index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))
            for i in range(3):
                if data_index < len(binary_message):
                    pixel[i] = pixel[i] & 0b11111110 | int(binary_message[data_index])
                    data_index += 1
            img.putpixel((x, y), tuple(pixel))

    output_directory = os.path.dirname(image_path)
    output_image_path = os.path.join(output_directory, "encoded.png")
    img.save(output_image_path)
    print("Message encoded successfully. Output image saved as:", output_image_path)

# Decode message from image
def decode_lsb(image_path):
    img = Image.open(image_path)
    width, height = img.size
    binary_message = ''

    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            for i in range(3):
                binary_message += str(pixel[i] & 1)

    sentinel_index = binary_message.find('1111111111111110')
    if sentinel_index == -1:
        return None

    binary_message = binary_message[:sentinel_index]

    message = ''
    for i in range(0, len(binary_message), 8):
        message += chr(int(binary_message[i:i+8], 2))
    return message

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LSBStegoApp()
    window.show()
    sys.exit(app.exec_())

