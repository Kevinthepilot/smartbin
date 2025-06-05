import torch
import cv2
import os
from ultralytics import YOLO

model = YOLO("finaloffinal.pt")
model.conf = 0.3

image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')

recycle = {
    'cardboard_box', 'cardboard_bowl', 'plastic_bottle', 'plastic_bottle_cap', 'plastic_box',
    'plastic_cup', 'plastic_cup_lid', 'plastic_spoon', 'plastic_cultery', 'can', 'light_bulb',
    'reusable_paper', 'scrap_paper', 'scrap_plastic', 'stick'
}
non_recycle = {'plastic_bag', 'snack_bag', 'straw', 'coltello', 'paint_bucket'}
dangerous = {'battery', 'chemical_plastic_bottle', 'chemical_plastic_gallon', 'chemical_spray_can'}

group_colors = {
    'Recycle': (0, 255, 0),
    'Non-Recycle': (0, 0, 255),
    'Dangerous': (255, 0, 0),
    'Unknown': (200, 200, 200)
}

# Directory containing images
image_dir = 'images'  # <-- Change this

# List all image files in directory
image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(image_extensions)]
fixed_width, fixed_height = 1280, 720
for image_name in image_files:
    image_path = os.path.join(image_dir, image_name)
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Failed to load image {image_path}")
        continue

    frame = cv2.resize(frame, (fixed_width, fixed_height))
    results = model(frame)
    result = results[0]

    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        cls_id = int(box.cls[0].item())
        label = result.names[cls_id]

        if label in recycle:
            group = 'Recycle'
        elif label in non_recycle:
            group = 'Non-Recycle'
        elif label in dangerous:
            group = 'Dangerous'
        else:
            group = 'Unknown'

        color = group_colors[group]
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        text = f"{label} ({group})"
        cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow("YOLOv8 Image Detection", frame)

    # Wait for key press, 'q' to quit, any other key to continue to next image
    key = cv2.waitKey(0)
    if key & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
