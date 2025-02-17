from flask import Flask, request, render_template_string, send_file
import cv2
import numpy as np
from io import BytesIO

app = Flask(__name__)

def encrypt_image(img, msg, password):

    flat = img.flatten().copy()  
    msg_len = len(msg)
    p_len = len(password)
    required = 2 + p_len + msg_len
    if len(flat) < required:
        raise Exception("Image too small for the message and password.")
    
    flat[0] = msg_len
    flat[1] = p_len
    # Embed the password
    for i in range(p_len):
        flat[2 + i] = ord(password[i])
    # Embed the secret message
    for i in range(msg_len):
        flat[2 + p_len + i] = ord(msg[i])
    new_img = flat.reshape(img.shape)
    return new_img

def decrypt_image(img, provided_password):
    flat = img.flatten()
    msg_len = int(flat[0])
    p_len = int(flat[1])
    stored_password = ''.join(chr(int(flat[2 + i])) for i in range(p_len))
    if stored_password != provided_password:
        return "You are not authorised"
    secret_message = ''.join(chr(int(flat[2 + p_len + i])) for i in range(msg_len))
    return secret_message

@app.route('/')
def index():
    return render_template_string('''
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Image Encryption</title>
      <!-- Bootstrap CSS -->
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
      <!-- Font Awesome -->
      <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
      <style>
         body { padding: 20px; background-color: #f4f4f9; }
         h1 { color: #007bff; }
         .form-container { 
             background-color: white; padding: 20px; border-radius: 8px; 
             box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; 
         }
         .section-title { margin-top: 30px; margin-bottom: 20px; color: #007bff; }
      </style>
    </head>
    <body>
      <div class="container">
        <h1 class="text-center">Image Encryption and Decryption</h1>
        <!-- Encryption Form -->
        <div class="form-container">
          <h3 class="section-title">Encrypt Image</h3>
          <form action="/encrypt" method="post" enctype="multipart/form-data">
             <div class="mb-3">
                <label for="image" class="form-label">Upload Image</label>
                <input type="file" name="image" class="form-control" required>
             </div>
             <div class="mb-3">
                <label for="message" class="form-label">Secret Message</label>
                <input type="text" name="message" class="form-control" required>
             </div>
             <div class="mb-3">
                <label for="password" class="form-label">Passcode</label>
                <input type="password" name="password" class="form-control" required>
             </div>
             <button type="submit" class="btn btn-primary w-100">
                 <i class="fas fa-lock"></i> Encrypt Image
             </button>
          </form>
        </div>
        <!-- Decryption Form -->
        <div class="form-container">
          <h3 class="section-title">Decrypt Image</h3>
          <form action="/decrypt" method="post" enctype="multipart/form-data">
             <div class="mb-3">
                <label for="encrypted_image" class="form-label">Upload Encrypted Image</label>
                <input type="file" name="encrypted_image" class="form-control" required>
             </div>
             <div class="mb-3">
                <label for="password" class="form-label">Enter Passcode for Decryption</label>
                <input type="password" name="password" class="form-control" required>
             </div>
             <button type="submit" class="btn btn-success w-100">
                 <i class="fas fa-unlock"></i> Decrypt Image
             </button>
          </form>
        </div>
      </div>
      <!-- Bootstrap JS -->
      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    ''')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    if 'image' not in request.files:
        return 'No file part'
    image_file = request.files['image']
    if image_file.filename == '':
        return 'No selected file'
    msg = request.form['message']
    password = request.form['password']
    # Read the image from the uploaded file
    file_bytes = np.frombuffer(image_file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    try:
        encrypted_img = encrypt_image(img, msg, password)
    except Exception as e:
        return str(e)
    # Encode image to PNG in memory (lossless)
    success, encoded_image = cv2.imencode('.png', encrypted_img)
    if not success:
        return "Image encoding failed."
    # Use BytesIO to store the encoded image
    image_io = BytesIO(encoded_image.tobytes())
    # Return the file as an attachment so that download starts automatically
    return send_file(
        image_io,
        mimetype='image/png',
        as_attachment=True,
        download_name="encryptedImage.png"
    )

@app.route('/decrypt', methods=['POST'])
def decrypt():
    if 'encrypted_image' not in request.files:
        return 'No file part'
    encrypted_image_file = request.files['encrypted_image']
    if encrypted_image_file.filename == '':
        return 'No selected file'
    password = request.form['password']
    file_bytes = np.frombuffer(encrypted_image_file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    decrypted_msg = decrypt_image(img, password)
    return render_template_string('''
    <!doctype html>
    <html lang="en">
      <head>
         <meta charset="UTF-8">
         <meta name="viewport" content="width=device-width, initial-scale=1">
         <title>Image Decryption - Result</title>
         <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
         <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
      </head>
      <body>
         <div class="container">
            <h1 class="text-center mt-5">Decryption Result</h1>
            <p class="text-center">Decrypted Message: <strong>{{ decrypted_msg }}</strong></p>
         </div>
      </body>
    </html>
    ''', decrypted_msg=decrypted_msg)

if __name__ == '__main__':
    app.run(debug=True)
