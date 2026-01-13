"""
Flask server for YOLO food detection
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import base64
from io import BytesIO
from PIL import Image
from ultralytics import YOLO # Ensure you have ultralytics installed
from collections import defaultdict # For counting detected items
import json

# Load YOLOv8 model once at startup
model = YOLO("yolov8n.pt")

app = Flask(__name__)
CORS(app)  # Enable CORS for Expo app

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# def detect_food_items_yolo(image_path):
#     """
#     Detect food items using YOLO model
#     TODO: Implement actual YOLO detection
#     For now, returns mock data for Phase 1 MVP
#     """
#     # Mock detection for Phase 1
#     # Replace this with actual YOLO model inference
    
#     # Example: Using ultralytics YOLO
#     # from ultralytics import YOLO
#     # model = YOLO('models/food_detection.pt')
#     # results = model(image_path)
#     # ... process results ...
    
#     # Mock response
#     return [
#         {
#             "name": "banana",
#             "quantity": 2,
#             "unit": "No.of",
#             "confidence": 0.95
#         },
#         {
#             "name": "apple",
#             "quantity": 1,
#             "unit": "No.of",
#             "confidence": 0.88
#         }
#     ]

# def detect_food_items_yolo(image_path):
#     results = model(image_path)

#     detected_items = []

#     for r in results:
#         for box in r.boxes:
#             cls_id = int(box.cls[0])
#             confidence = float(box.conf[0])

#             if confidence < 0.5:
#                 continue

#             name = model.names[cls_id]

#             detected_items.append({
#                 "name": name,
#                 "quantity": 1,
#                 "unit": "No.of",
#                 "confidence": round(confidence, 2)
#             })

#     return detected_items


def detect_food_items_yolo(image_path):
    results = model(image_path)

    grouped = defaultdict(list)

    for r in results:
        for box in r.boxes:
            conf = float(box.conf[0])
            if conf < 0.5:
                continue

            cls_id = int(box.cls[0])
            name = model.names[cls_id]
            grouped[name].append(conf)

    detected_items = []

    for name, confidences in grouped.items():
        detected_items.append({
            "name": name,
            "quantity": len(confidences),
            "unit": "No.of",
            "confidence": round(max(confidences), 2)
        })

    return detected_items

# @app.route('/api/detect', methods=['POST'])
# def detect_food():
#     """
#     Detect food items in uploaded image
#     """
#     try:
#         if 'image' not in request.files:
#             return jsonify({
#                 'success': False,
#                 'message': 'No image file provided'
#             }), 400

#         file = request.files['image']
        
#         if file.filename == '':
#             return jsonify({
#                 'success': False,
#                 'message': 'No file selected'
#             }), 400

#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)

#             # Detect food items
#             detected_items = detect_food_items_yolo(filepath)

#             # Clean up uploaded file
#             os.remove(filepath)

#             return jsonify({
#                 'success': True,
#                 'detectedItems': detected_items
#             })

#         return jsonify({
#             'success': False,
#             'message': 'Invalid file type'
#         }), 400

#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'message': f'Error processing image: {str(e)}'
#         }), 500
@app.route('/api/detect', methods=['POST'])
def detect_food():
    """
    Detect food items in uploaded image
    """
    try:
        # 🔍 DEBUG (TEMPORARY — VERY IMPORTANT)
        print("==== /api/detect called ====")
        print("Headers:", dict(request.headers))
        print("Files:", request.files)
        print("Form:", request.form)

        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No image file provided'
            }), 400

        file = request.files['image']

        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No file selected'
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'message': 'Invalid file type'
            }), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Detect food items (YOLO or mock)
        detected_items = detect_food_items_yolo(filepath)

        # Cleanup
        os.remove(filepath)

        return jsonify({
            'success': True,
            'detectedItems': detected_items
        })

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({
            'success': False,
            'message': f'Error processing image: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'YOLO Food Detection API'
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)

