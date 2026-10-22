"""Transfer learning with MobileNetV2. Usage:
  python train.py --data-dir data --epochs 10 [--fine-tune] [--no-pretrained]
  python train.py --data-dir data --evaluate-only
Preprocessing (MobileNetV2 scaling) lives INSIDE the saved model, so inference just feeds 0-255 RGB pixels."""
import argparse, json, random, datetime
from pathlib import Path
import numpy as np, tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix

EXT = {".jpg", ".jpeg", ".png"}
OUT = Path(__file__).parent / "models"

def split_files(data_dir, seed=42, val=0.15, test=0.15):
    classes = sorted(d.name for d in Path(data_dir).iterdir() if d.is_dir())
    if len(classes) < 2: raise SystemExit(f"Need >=2 class folders in {data_dir}. See ml/data/README.md")
    sp = {"train": [], "val": [], "test": []}; rng = random.Random(seed)
    for i, c in enumerate(classes):
        fs = sorted(p for p in (Path(data_dir) / c).iterdir() if p.suffix.lower() in EXT); rng.shuffle(fs)
        nv, nt = int(len(fs) * val), int(len(fs) * test)
        sp["val"] += [(str(p), i) for p in fs[:nv]]; sp["test"] += [(str(p), i) for p in fs[nv:nv + nt]]
        sp["train"] += [(str(p), i) for p in fs[nv + nt:]]
    return classes, sp

def make_ds(items, size, bs, num, shuffle=False):
    paths, labels = zip(*items)
    ds = tf.data.Dataset.from_tensor_slices((list(paths), list(labels)))
    if shuffle: ds = ds.shuffle(len(items), seed=1)
    def load(p, y):
        img = tf.image.decode_image(tf.io.read_file(p), channels=3, expand_animations=False)
        img.set_shape([None, None, 3])
        return tf.image.resize(img, (size, size)), tf.one_hot(y, num)
    return ds.map(load, num_parallel_calls=tf.data.AUTOTUNE).batch(bs).prefetch(tf.data.AUTOTUNE)

def build(n, size, pretrained):
    base = tf.keras.applications.MobileNetV2((size, size, 3), include_top=False,
                                             weights="imagenet" if pretrained else None)
    base.trainable = False
    x = inp = tf.keras.Input((size, size, 3))
    x = tf.keras.layers.RandomFlip("horizontal")(x); x = tf.keras.layers.RandomRotation(0.1)(x)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
    x = base(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x); x = tf.keras.layers.Dropout(0.3)(x)
    out = tf.keras.layers.Dense(n, activation="softmax")(x)
    return tf.keras.Model(inp, out), base

def evaluate(model, test_ds, classes):
    y_true = np.concatenate([y.numpy().argmax(1) for _, y in test_ds]); y_pred = model.predict(test_ds).argmax(1)
    rep = classification_report(y_true, y_pred, labels=list(range(len(classes))), target_names=classes, output_dict=True, zero_division=0)
    m = {"accuracy": rep["accuracy"], "per_class": {c: rep[c] for c in classes}, "macro_avg": rep["macro avg"],
         "confusion_matrix": confusion_matrix(y_true, y_pred, labels=list(range(len(classes)))).tolist(), "classes": classes,
         "test_samples": int(len(y_true))}
    (OUT / "metrics.json").write_text(json.dumps(m, indent=2)); print(json.dumps({k: m[k] for k in ("accuracy", "macro_avg")}, indent=2))

if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--data-dir", default="data"); a.add_argument("--epochs", type=int, default=10)
    a.add_argument("--img-size", type=int, default=224); a.add_argument("--batch-size", type=int, default=32)
    a.add_argument("--fine-tune", action="store_true"); a.add_argument("--unfreeze", type=int, default=30)
    a.add_argument("--no-pretrained", action="store_true"); a.add_argument("--evaluate-only", action="store_true")
    a = a.parse_args(); OUT.mkdir(exist_ok=True)
    classes, sp = split_files(a.data_dir); NUM = len(classes)
    test_ds = make_ds(sp["test"], a.img_size, a.batch_size, NUM)
    if a.evaluate_only:
        evaluate(tf.keras.models.load_model(OUT / "waste_model.keras"), test_ds, classes); raise SystemExit
    train_ds = make_ds(sp["train"], a.img_size, a.batch_size, NUM, True); val_ds = make_ds(sp["val"], a.img_size, a.batch_size, NUM)
    model, base = build(NUM, a.img_size, not a.no_pretrained)
    cb = [tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True),
          tf.keras.callbacks.ModelCheckpoint(OUT / "waste_model.keras", save_best_only=True)]
    model.compile(tf.keras.optimizers.Adam(1e-3), "categorical_crossentropy", ["accuracy"])
    model.fit(train_ds, validation_data=val_ds, epochs=a.epochs, callbacks=cb)
    if a.fine_tune:
        base.trainable = True
        for l in base.layers[:-a.unfreeze]: l.trainable = False
        model.compile(tf.keras.optimizers.Adam(1e-5), "categorical_crossentropy", ["accuracy"])
        model.fit(train_ds, validation_data=val_ds, epochs=a.epochs, callbacks=cb)
    model = tf.keras.models.load_model(OUT / "waste_model.keras")
    ver = datetime.datetime.now().strftime("mobilenetv2-%Y%m%d-%H%M")
    (OUT / "classes.json").write_text(json.dumps({"classes": classes, "img_size": a.img_size, "version": ver}, indent=2))
    evaluate(model, test_ds, classes)
