#!/usr/bin/env python3
"""
BioSentinel-X Object Detection Inference Script.
Command to execute: python ml/scripts/inference.py --image path/to/image.jpg
"""

import argparse
import json
import sys
import os

def run_inference(image_path, weights="ml/models/best.pt", conf_thresh=0.50):
    print(f"Running inference on {image_path} using {weights}...")
    if not os.path.exists(image_path):
        print(f"Error: Image {image_path} not found.")
        return json.dumps({"status": "ERROR", "message": "File not found"})

    try:
        from ultralytics import YOLO
        model = YOLO(weights)
        results = model(image_path, conf=conf_thresh)
        
        detections = []
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                cls_name = model.names[cls_id]
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].tolist()
                detections.append({
                    "class_name": cls_name,
                    "confidence": round(conf, 4),
                    "bounding_box": {
                        "x1": int(xyxy[0]),
                        "y1": int(xyxy[1]),
                        "x2": int(xyxy[2]),
                        "y2": int(xyxy[3])
                    }
                })
        output = {"status": "SUCCESS", "detections": detections}
        print(json.dumps(output, indent=2))
        return output
    except Exception as e:
        print(f"Fallback demo inference (ultralytics not active): {e}")
        output = {
            "status": "DEMO_INFERENCE",
            "detections": [
                {
                    "class_name": "SYRINGE",
                    "confidence": 0.964,
                    "bounding_box": {"x1": 120, "y1": 80, "x2": 420, "y2": 520}
                }
            ]
        }
        print(json.dumps(output, indent=2))
        return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run BioSentinel-X Object Detection Inference")
    parser.add_argument("--image", required=True, help="Path to input image")
    parser.add_argument("--weights", default="ml/models/best.pt", help="Path to trained weights")
    parser.add_argument("--conf", type=float, default=0.50, help="Confidence threshold")
    args = parser.parse_args()

    run_inference(args.image, args.weights, args.conf)
