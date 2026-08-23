#!/usr/bin/env python3
"""
BioSentinel-X Object Detection Model Training Script.
Trains a YOLOv8 custom object detector on biomedical waste images.
Command to execute: python ml/scripts/train.py --epochs 50 --imgsz 640
"""

import argparse
import sys
import os

def train_yolo(data_yaml="ml/data.yaml", epochs=50, imgsz=640, weights="yolov8n.pt"):
    print(f"Starting BioSentinel-X YOLO Training on {data_yaml}...")
    try:
        from ultralytics import YOLO
        model = YOLO(weights)
        results = model.train(
            data=data_yaml,
            epochs=epochs,
            imgsz=imgsz,
            project="ml/runs",
            name="biosentinel_yolo",
            save=True
        )
        print("Training complete! Model saved to ml/runs/biosentinel_yolo/weights/best.pt")
        return results
    except ImportError:
        print("[WARNING] ultralytics package not installed. Run: pip install -r ml/requirements.txt")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train BioSentinel-X Object Detector")
    parser.add_argument("--data", default="ml/data.yaml", help="Path to data.yaml")
    parser.add_argument("--epochs", type=int, default=50, help="Number of training epochs")
    parser.add_argument("--imgsz", type=int, default=640, help="Image resolution")
    args = parser.parse_args()
    
    train_yolo(args.data, args.epochs, args.imgsz)
