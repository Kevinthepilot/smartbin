import torch
import cv2
import numpy as np
from ultralytics import YOLO
import random

# Load YOLOv8 model
userModel = YOLO("best.pt")
backupModel = YOLO(r"a.pt")
backupModel.conf = 0.3  # confidence threshold

# Nhóm phân loại rác
recycle = {
    'cardboard_box', 'cardboard_bowl', 'plastic_bottle', 'plastic_bottle_cap', 'plastic_box',
    'plastic_cup', 'plastic_cup_lid', 'plastic_spoon', 'plastic_cultery', 'can', 'light_bulb',
    'reusable_paper', 'scrap_paper', 'scrap_plastic', 'stick', 'paper'}
non_recycle = {'plastic_bag', 'snack_bag', 'straw', 'coltello', 'paint_bucket', 'nylon', 'spoon'}
dangerous = {'battery', 'chemical_plastic_bottle', 'chemical_plastic_gallon', 'chemical_spray_can', 'lighter'}

class Ai:


     # Hàm tiền xử lý ảnh (tăng chất lượng ảnh)
     def preprocess_image(self, img):
          # Resize ảnh về 640x640
          img = cv2.resize(img, (640, 640))

          # Giảm nhiễu nhưng giữ biên
          img = cv2.bilateralFilter(img, 9, 75, 75)

          # Tăng tương phản sử dụng CLAHE
          lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
          l, a, b = cv2.split(lab)
          clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
          cl = clahe.apply(l)
          limg = cv2.merge((cl, a, b))
          img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

          # Làm sắc nét ảnh
          sharpen_kernel = np.array([[0, -1, 0],
                                        [-1, 5, -1],
                                        [0, -1, 0]])
          img = cv2.filter2D(img, -1, sharpen_kernel)

          return img
     
     def center_crop(self, img, sx, sy):
          h, w, _ = img.shape
          ch, cw = sx, sy
          start_x = w // 2 - cw // 2+ 50
          start_y = h // 2 - ch // 2+ 10
          cropped = img[start_y:start_y + ch, start_x:start_x + cw]
          return cropped
     
     def predict(self):
          # Đường dẫn ảnh
          image_path = "uploaded_cam.jpg"

          # Đọc ảnh
          frame = cv2.imread(image_path)
          if frame is None:
               print("Không thể đọc ảnh. Kiểm tra lại đường dẫn.")
               exit()

          # Tiền xử lý ảnh để tăng chất lượng
          frame = self.center_crop(frame, 480, 480)
          frame = self.preprocess_image(frame)
          #cv2.imwrite(f"dataset/Nylon/nylon{random.randint(1, 1000)}.jpg", frame)
          cv2.imwrite("processed.jpg", frame)

          # Dự đoán bằng YOLO
          results = userModel(frame)
          result = results[0]

          # Chọn box có độ tin cậy cao nhất
          best_box = None
          best_conf = -1
          best_label = ""
          best_coords = ()
          conf = 0
          label = "None"

          for box in result.boxes:
               cls_id = int(box.cls[0].item())
               conf = float(box.conf[0].item())
               label = result.names[cls_id]

          if conf > best_conf:
               best_conf = conf
               best_label = label
          
          # Fallback if confidence too low
          if best_conf < 0.3:  # You can adjust the threshold
               print(f"Low confidence ({best_conf:.2f}), using backup model...")
               results = backupModel(frame)
               result = results[0]
               best_conf = -1
               for box in result.boxes:
                    cls_id = int(box.cls[0].item())
                    conf = float(box.conf[0].item())
                    label = result.names[cls_id]
                    if conf > best_conf:
                         best_conf = conf
                         best_label = label

          # Chuyển gallon thành plastic bag nếu conf thấp
          if best_label == "chemical_plastic_gallon" and best_conf < 0.8:
               best_label = "plastic_bag"
          if best_label == "can" and best_conf < 0.5:
               best_label = "plastic_bag"
          # Xác định nhóm và hiển thị
          if best_conf > 0:
               if best_label in recycle:
                    group = 'Recycle'
               elif best_label in non_recycle:
                    group = 'Non-Recycle'
               elif best_label in dangerous:
                    group = 'Dangerous'
               else:
                    group = 'None'
          else:
               group = "None"
          print(f"Detected: {best_label}, Confidence: {best_conf:.2f}, Group: {group}")
          return group

