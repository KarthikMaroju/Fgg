import { useState, useRef } from "react"; import { classify } from "../api"; import { Result } from "../components/Parts";
const OK = ["image/jpeg", "image/png"], MAX = 5 * 1024 * 1024;
export default function Classify() {
  const [file, setFile] = useState(null), [url, setUrl] = useState(null), [err, setErr] = useState(null);
  const [busy, setBusy] = useState(false), [res, setRes] = useState(null), [drag, setDrag] = useState(false), input = useRef();
  const pick = (f) => { setRes(null); setErr(null);
    if (!f) return; if (!OK.includes(f.type)) return setErr("Please choose a JPEG or PNG image.");
    if (f.size > MAX) return setErr("Image must be under 5 MB.");
    setFile(f); setUrl(URL.createObjectURL(f)); };
  const run = async () => { setBusy(true); setErr(null); try { setRes(await classify(file)); } catch (e) { setErr(e.message); } setBusy(false); };
  return (<><h1>Classify waste</h1>
    <div className={"drop" + (drag ? " on" : "")} tabIndex={0} role="button" aria-label="Choose or drop an image"
      onClick={() => input.current.click()} onKeyDown={(e) => e.key === "Enter" && input.current.click()}
      onDragOver={(e) => { e.preventDefault(); setDrag(true); }} onDragLeave={() => setDrag(false)}
      onDrop={(e) => { e.preventDefault(); setDrag(false); pick(e.dataTransfer.files[0]); }}>
      {url ? <img src={url} alt="Selected waste preview" /> : "Drag & drop an image here, or click to browse"}
      <input ref={input} type="file" accept="image/jpeg,image/png" hidden onChange={(e) => pick(e.target.files[0])} /></div>
    <button className="btn" disabled={!file || busy} onClick={run}>{busy ? "Classifying…" : "Classify"}</button>
    {err && <p className="err" role="alert">{err}</p>}{res && <Result {...res} />}</>);
}
