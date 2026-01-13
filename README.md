# Backend API for Food Tracker

This backend handles YOLO food detection from images.

## Setup

### Prerequisites
- Python 3.8+
- Node.js 18+ (for Express server if using Node.js wrapper)
- YOLO model files (you'll need to train or download a food detection model)

### Option 1: Python Flask/FastAPI Server (Recommended for YOLO)

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set up YOLO model:
   - Download or train a YOLO model for food detection
   - Place model files in `backend/models/` directory
   - Update `yolo_detector.py` with your model path

3. Run the server:
```bash
python app.py
```

The server will run on `http://localhost:8000`

### Option 2: Node.js/Express Server (Wrapper)

If you prefer Node.js, you can create a wrapper that calls Python YOLO service:

```bash
cd backend
npm install
npm start
```

## API Endpoints

### POST /api/detect

Detects food items in an uploaded image.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: `image` (file)

**Response:**
```json
{
  "success": true,
  "detectedItems": [
    {
      "name": "banana",
      "quantity": 2,
      "unit": "No.of",
      "confidence": 0.95
    },
    {
      "name": "apple",
      "quantity": 1,
      "unit": "No.of",
      "confidence": 0.88
    }
  ]
}
```

## Environment Variables

Create a `.env` file in the backend directory:

```
PORT=8000
YOLO_MODEL_PATH=./models/food_detection.pt
```

## Notes

- For Phase 1 MVP, the backend uses mock data if YOLO model is not available
- Update `EXPO_PUBLIC_YOLO_API_URL` in your Expo app to point to your backend URL
- For production, deploy this backend to a cloud service (AWS, Heroku, etc.)

