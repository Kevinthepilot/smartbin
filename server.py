from flask import Flask, request
import cv2

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
     if 'imageFile' not in request.files:
          return "No imageFile part in the request", 400

     file = request.files['imageFile']

     if file.filename == '':
          return "No selected file", 400

     # Save the uploaded image to disk (optional)
     file.save("uploaded_cam.jpg")
     print("Image received and saved!")
     return "OK", 200
     

if __name__ == "__main__":
     app.run(host="0.0.0.0", port=8080)