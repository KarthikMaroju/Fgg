# Cleantech: Transforming Waste Management with Transfer Learning
Upload a waste image, get a predicted category with confidence, disposal guidance, and a history/statistics dashboard.
Stack: React+Vite, FastAPI, SQLAlchemy/SQLite, TensorFlow/Keras MobileNetV2 (transfer learning).

## Status (honest)
No model is bundled. **No training or evaluation has been run and no accuracy is claimed.** Until you train, `/api/classify`
returns 503 "Model not trained yet". The code was written but not executed, so run the tests yourself.

## Quick start
1. **Dataset:** put class folders in `ml/data/<class>/` (see `ml/data/README.md`, e.g. TrashNet; check its licence).
2. **Train:** `cd ml && pip install -r requirements.txt && python train.py --data-dir data --epochs 10 [--fine-tune]`
   - Needs internet once for ImageNet weights; offline: `--no-pretrained` (random init, much weaker, development only).
   - Outputs `ml/models/{waste_model.keras, classes.json, metrics.json}` (accuracy, precision/recall/F1, confusion matrix on a held-out 15% test split).
   - Re-evaluate: `python train.py --data-dir data --evaluate-only`
3. **Backend:** `cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload` (docs at :8000/docs)
4. **Frontend:** `cd frontend && npm install && npm run dev` → http://localhost:5173
5. **Tests:** `cd backend && pytest` (a stub classifier is used only inside tests)

Settings (CORS, upload limit, low-confidence threshold) are environment variables; see `.env.example`.

## API
| Endpoint | Description |
|---|---|
| `GET /api/health` | status + `model_available` |
| `GET /api/classes` | classes from `classes.json` |
| `POST /api/classify` | multipart `file` (JPEG/PNG) → `{record, recommendation, notice}` |
| `GET /api/history?page&page_size&category&q` | `{items,total,page,pages}` |
| `GET/DELETE /api/history/{id}` | one record / delete |
| `GET /api/statistics` | computed from stored records |

Errors: 413 too large, 415 wrong type, 422 corrupt image, 404 not found, 503 model unavailable.

## Design notes
- MobileNetV2 preprocessing is inside the saved model, so training and inference cannot drift apart.
- Classes come from dataset folders and are saved with the model; none are assumed.
- Uploaded images are **not stored**; only category, confidence, sanitized filename and timestamp.
- Guidance lives in `backend/app/services/recommendations.py`; local municipal rules always take precedence.
- Predictions are AI-assisted estimates, not guaranteed material identification.
