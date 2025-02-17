# Image Encryption and Decryption Application

This application allows users to encrypt and decrypt images using a secret message and a password. It is built using Flask and OpenCV.

## Features

- **Encrypt Images**: Users can upload an image, provide a secret message, and a password to encrypt the image.
- **Decrypt Images**: Users can upload an encrypted image and provide the correct password to retrieve the secret message.

## Requirements

- Python 3.x

You can install the required packages using the `requirements.txt` file.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to `http://127.0.0.1:5000`.

3. Use the forms to encrypt or decrypt images.

## Error Handling

If you encounter the following error:
```
Couldn't find the requested file /dist/css/bootstrap.min.css" in bootstrap.
```
This indicates that the Bootstrap CSS file could not be found. Ensure that you have a stable internet connection, as the application links to Bootstrap via CDN.



## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - for the micro web framework.
- [OpenCV](https://opencv.org/) - for the image identification and scanning.
- [NumPy](https://numpy.org/) - for the arrays in which the data of pixels were stored.
- [Bootstrap](https://getbootstrap.com/) - for styling the web interface.