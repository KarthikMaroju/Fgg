import io, os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
from fastapi.testclient import TestClient
from PIL import Image
from app.main import app
from app.api import routes

client = TestClient(app)

def png():
    b = io.BytesIO(); Image.new("RGB", (32, 32), "green").save(b, "PNG"); return b.getvalue()

class Stub:  # test double only; never used at runtime
    classes, version = ["paper", "plastic"], "test"
    def predict(self, data, top_k=3): return [("plastic", 0.9), ("paper", 0.1)]

def test_health(): assert client.get("/api/health").json()["status"] == "ok"

def test_rejects_bad_type():
    assert client.post("/api/classify", files={"file": ("a.txt", b"x", "text/plain")}).status_code == 415

def test_rejects_corrupt():
    assert client.post("/api/classify", files={"file": ("a.png", b"notimage", "image/png")}).status_code == 422

def test_missing_model(monkeypatch, tmp_path):
    from app.services import classifier
    monkeypatch.setattr(classifier, "_instance", None)
    monkeypatch.setattr(classifier.config, "MODEL_DIR", tmp_path)
    assert client.post("/api/classify", files={"file": ("a.png", png(), "image/png")}).status_code == 503

def test_classify_history_stats(monkeypatch):
    monkeypatch.setattr(routes.clf, "get_classifier", lambda: Stub())
    r = client.post("/api/classify", files={"file": ("a.png", png(), "image/png")})
    assert r.status_code == 200 and r.json()["record"]["category"] == "plastic"
    rid = r.json()["record"]["id"]
    assert client.get(f"/api/history/{rid}").status_code == 200
    assert client.get("/api/statistics").json()["total"] >= 1
    assert client.delete(f"/api/history/{rid}").status_code == 200
