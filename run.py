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

class Ai:
    def predict():
        frame = cv2.imread("uploaded_cam.jpg")
        if frame is None:
            return "Fail"

        results = model(frame)
        result = results[0]
        group = "None"

        for box in result.boxes:
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
        return group

