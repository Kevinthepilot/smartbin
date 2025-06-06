import torch
import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO(r"C:\Users\ThinkPad\Desktop\trash\tester2.pt")
model.conf = 0.3  # confidence threshold

# Nhóm phân loại rác
recycle = {
    'cardboard_box', 'cardboard_bowl', 'plastic_bottle', 'plastic_bottle_cap', 'plastic_box',
    'plastic_cup', 'plastic_cup_lid', 'plastic_spoon', 'plastic_cultery', 'can', 'light_bulb',
    'reusable_paper', 'scrap_paper', 'scrap_plastic', 'stick'
}
non_recycle = {'plastic_bag', 'snack_bag', 'straw', 'coltello', 'paint_bucket'}
dangerous = {'battery', 'chemical_plastic_bottle', 'chemical_plastic_gallon', 'chemical_spray_can'}

# Màu cho từng nhóm
group_colors = {
    'Recycle': (0, 255, 0),
    'Non-Recycle': (0, 0, 255),
    'Dangerous': (0, 255, 255),
    'Unknown': (200, 200, 200)
}

# Hàm tiền xử lý ảnh (tăng chất lượng ảnh)
def preprocess_image(img):
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

# Đường dẫn ảnh
image_path = "can3.png"

# Đọc ảnh
frame = cv2.imread(image_path)
if frame is None:
    print("Không thể đọc ảnh. Kiểm tra lại đường dẫn.")
    exit()

# Tiền xử lý ảnh để tăng chất lượng
frame = preprocess_image(frame)

# Dự đoán bằng YOLO
results = model(frame)
result = results[0]

# Chọn box có độ tin cậy cao nhất
best_box = None
best_conf = -1
best_label = ""
best_coords = ()

for box in result.boxes:
    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
    cls_id = int(box.cls[0].item())
    conf = float(box.conf[0].item())
    label = result.names[cls_id]

    if conf > best_conf:
        best_conf = conf
        best_label = label
        best_coords = (x1, y1, x2, y2)

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
        group = 'Unknown'

    color = group_colors[group]
    text = f"{best_label} ({best_conf:.2f})"
    print(f"{text} {group}")

    x1, y1, x2, y2 = best_coords
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
else:
    print("Không phát hiện được vật thể nào đáng tin cậy.")

# Hiển thị ảnh kết quả
cv2.imshow("YOLOv8 Trash Classification", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
