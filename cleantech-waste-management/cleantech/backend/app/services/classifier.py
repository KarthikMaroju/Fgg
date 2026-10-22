import io, json, logging
import numpy as np
from PIL import Image
from app.core import config
log = logging.getLogger("cleantech")

class ModelNotAvailable(Exception): pass

class Classifier:
    def __init__(self):
        meta, path = config.MODEL_DIR / "classes.json", config.MODEL_DIR / "waste_model.keras"
        if not (meta.exists() and path.exists()):
            raise ModelNotAvailable("Model not trained yet. Run ml/train.py (see README).")
        import tensorflow as tf  # lazy import
        self.meta = json.loads(meta.read_text()); self.model = tf.keras.models.load_model(path)
        self.classes, self.size, self.version = self.meta["classes"], self.meta["img_size"], self.meta["version"]

    def predict(self, data: bytes, top_k=3):
        img = Image.open(io.BytesIO(data)).convert("RGB").resize((self.size, self.size))
        x = np.expand_dims(np.asarray(img, dtype="float32"), 0)  # 0-255; scaling is inside the model
        p = self.model.predict(x, verbose=0)[0]
        return [(self.classes[i], float(p[i])) for i in np.argsort(p)[::-1][:top_k]]

_instance = None
def get_classifier() -> Classifier:
    global _instance
    if _instance is None: _instance = Classifier()
    return _instance
