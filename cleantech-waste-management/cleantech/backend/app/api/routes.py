import io, logging, re
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from PIL import Image, UnidentifiedImageError
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.core import config
from app.db.database import Record, get_db
from app.schemas.schemas import ClassifyOut, HistoryOut, RecordOut
from app.services import classifier as clf
from app.services.recommendations import get_recommendation

router = APIRouter(prefix="/api"); log = logging.getLogger("cleantech")
NOTICE = "AI-assisted estimate only; not a guaranteed identification of the material."

def _classifier():
    try: return clf.get_classifier()
    except clf.ModelNotAvailable as e: raise HTTPException(503, str(e))
    except Exception: log.exception("model load failed"); raise HTTPException(503, "Model could not be loaded.")

@router.get("/health")
def health():
    return {"status": "ok", "model_available": (config.MODEL_DIR / "waste_model.keras").exists()}

@router.get("/classes")
def classes():
    c = _classifier(); return {"classes": c.classes, "model_version": c.version}

@router.post("/classify", response_model=ClassifyOut)
async def classify(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in config.ALLOWED_TYPES: raise HTTPException(415, "Only JPEG and PNG images are supported.")
    data = await file.read(config.MAX_UPLOAD_BYTES + 1)
    if len(data) > config.MAX_UPLOAD_BYTES: raise HTTPException(413, f"File exceeds {config.MAX_UPLOAD_BYTES // 1048576} MB limit.")
    try: Image.open(io.BytesIO(data)).verify()
    except (UnidentifiedImageError, OSError, SyntaxError): raise HTTPException(422, "File is not a valid image.")
    c = _classifier()
    try: preds = c.predict(data)
    except Exception: log.exception("inference failed"); raise HTTPException(500, "Classification failed.")
    top, conf = preds[0]
    name = re.sub(r"[^\w.\-]", "_", file.filename or "upload")[:100]
    rec = Record(category=top, confidence=conf, low_confidence=conf < config.LOW_CONFIDENCE, filename=name,
                 model_version=c.version, alternatives=[{"category": k, "confidence": v} for k, v in preds[1:]])
    db.add(rec); db.commit(); db.refresh(rec)
    notice = NOTICE + (" Confidence is low; verify manually." if rec.low_confidence else "")
    return {"record": rec, "recommendation": get_recommendation(top), "notice": notice}

@router.get("/history", response_model=HistoryOut)
def history(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), category: str | None = None,
            q: str | None = Query(None, max_length=100), db: Session = Depends(get_db)):
    stmt = select(Record)
    if category: stmt = stmt.where(Record.category == category)
    if q: stmt = stmt.where(Record.filename.ilike(f"%{q}%"))
    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    items = db.scalars(stmt.order_by(Record.created_at.desc()).offset((page - 1) * page_size).limit(page_size)).all()
    return {"items": items, "total": total, "page": page, "pages": max(1, -(-total // page_size))}

@router.get("/history/{rid}")
def one(rid: int, db: Session = Depends(get_db)):
    r = db.get(Record, rid)
    if not r: raise HTTPException(404, "Record not found.")
    return {"record": RecordOut.model_validate(r), "recommendation": get_recommendation(r.category)}

@router.delete("/history/{rid}")
def delete(rid: int, db: Session = Depends(get_db)):
    r = db.get(Record, rid)
    if not r: raise HTTPException(404, "Record not found.")
    db.delete(r); db.commit(); return {"deleted": rid}

@router.get("/statistics")
def stats(db: Session = Depends(get_db)):
    total = db.scalar(select(func.count(Record.id))) or 0
    by = db.execute(select(Record.category, func.count()).group_by(Record.category)).all()
    return {"total": total, "average_confidence": db.scalar(select(func.avg(Record.confidence))) or 0,
            "low_confidence_count": db.scalar(select(func.count()).where(Record.low_confidence)) or 0,
            "by_category": {k: v for k, v in by}}
