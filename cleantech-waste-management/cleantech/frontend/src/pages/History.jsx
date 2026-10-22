import { useState } from "react"; import { Link, useParams, useNavigate } from "react-router-dom";
import { getHistory, getRecord, deleteRecord } from "../api"; import { useAsync } from "../hooks"; import { Status, Result, pct } from "../components/Parts";
export function History() {
  const [q, setQ] = useState(""), [cat, setCat] = useState(""), [page, setPage] = useState(1), [n, setN] = useState(0);
  const s = useAsync(() => getHistory({ page, q, ...(cat && { category: cat }) }), [page, q, cat, n]), d = s.data;
  return (<><h1>History</h1>
    <div className="row"><input aria-label="Search filename" placeholder="Search filename" value={q} onChange={(e) => { setQ(e.target.value); setPage(1); }} />
      <input aria-label="Filter category" placeholder="Category" value={cat} onChange={(e) => { setCat(e.target.value.toLowerCase()); setPage(1); }} /></div>
    <Status s={s} empty={d && d.items.length === 0 && "No records found."} />
    {d && d.items.length > 0 && <table><thead><tr><th>File</th><th>Category</th><th>Confidence</th><th>Date</th><th /></tr></thead><tbody>
      {d.items.map((r) => (<tr key={r.id}><td><Link to={`/history/${r.id}`}>{r.filename}</Link></td><td>{r.category}</td><td>{pct(r.confidence)}</td>
        <td>{new Date(r.created_at + "Z").toLocaleString()}</td>
        <td><button onClick={async () => { if (confirm("Delete this record?")) { await deleteRecord(r.id); setN(n + 1); } }}>Delete</button></td></tr>))}</tbody></table>}
    {d && <div className="row"><button disabled={page <= 1} onClick={() => setPage(page - 1)}>Prev</button><span>Page {d.page} / {d.pages}</span>
      <button disabled={page >= d.pages} onClick={() => setPage(page + 1)}>Next</button></div>}</>);
}
export function Detail() {
  const { id } = useParams(), nav = useNavigate(), s = useAsync(() => getRecord(id), [id]);
  return (<><button onClick={() => nav("/history")}>← Back</button><Status s={s} />
    {s.data && <><p className="muted">{s.data.record.filename} · {s.data.record.model_version}</p><Result {...s.data} notice="" /></>}</>);
}
