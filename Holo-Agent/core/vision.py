import os

import cv2
import mss
import numpy as np
import onnxruntime as ort

from config import CLASSES, CONF_THRESHOLD, MODEL_PATH


class Vision:
    def __init__(self, model_path=MODEL_PATH, device=None, use_android=False):
        self.device = device
        self.use_android = use_android
        self.model_path = model_path
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"YOLO model not found: {self.model_path}")
        self.session = ort.InferenceSession(self.model_path, providers=["CPUExecutionProvider"])
        self.input_name = self.session.get_inputs()[0].name

    def capture(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            frame = np.array(sct.grab(monitor))[:, :, :3]
            return frame

    def detect(self, frame=None):
        if frame is None:
            frame = self.capture()

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(rgb, (640, 640), interpolation=cv2.INTER_LINEAR)
        normalized = resized.astype(np.float32) / 255.0
        blob = normalized.transpose(2, 0, 1)
        blob = np.expand_dims(blob, axis=0)

        outputs = self.session.run(None, {self.input_name: blob})
        prediction = outputs[0]
        if prediction.ndim == 3:
            prediction = prediction[0]

        detections = []
        for row in prediction:
            if row.size < 6:
                continue

            if row.shape[0] >= 85:
                scores = row[4:]
                class_id = int(np.argmax(scores))
                conf = float(scores[class_id])
                if conf < CONF_THRESHOLD:
                    continue

                x_center = float(row[0])
                y_center = float(row[1])
                width = float(row[2])
                height = float(row[3])
                x1 = (x_center - width / 2.0) * (1920 / 640.0)
                y1 = (y_center - height / 2.0) * (1080 / 640.0)
                x2 = (x_center + width / 2.0) * (1920 / 640.0)
                y2 = (y_center + height / 2.0) * (1080 / 640.0)
                cls_name = CLASSES[class_id] if class_id < len(CLASSES) else "unknown"
                detections.append({
                    "class": cls_name,
                    "bbox": [float(x1), float(y1), float(x2), float(y2)],
                    "center": ((x1 + x2) / 2.0, (y1 + y2) / 2.0),
                    "conf": float(conf),
                })
                continue

            if row.shape[0] >= 6:
                x1 = float(row[0])
                y1 = float(row[1])
                x2 = float(row[2])
                y2 = float(row[3])
                conf = float(row[4])
                class_id = int(row[5])
                if conf < CONF_THRESHOLD:
                    continue
                cls_name = CLASSES[class_id] if class_id < len(CLASSES) else "unknown"
                detections.append({
                    "class": cls_name,
                    "bbox": [x1 * (1920 / 640.0), y1 * (1080 / 640.0), x2 * (1920 / 640.0), y2 * (1080 / 640.0)],
                    "center": (((x1 + x2) / 2.0) * (1920 / 640.0), ((y1 + y2) / 2.0) * (1080 / 640.0)),
                    "conf": conf,
                })

        return detections
