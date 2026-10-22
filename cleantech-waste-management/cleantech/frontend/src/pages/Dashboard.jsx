import { getStats } from "../api"; import { useAsync } from "../hooks"; import { Status, pct } from "../components/Parts";
export default function Dashboard() {
  const s = useAsync(getStats, []), d = s.data;
  return (<><h1>Dashboard</h1><Status s={s} empty={d && d.total === 0 && "No classifications yet. Upload an image to get started."} />
    {d && d.total > 0 && <><div className="grid"><div className="card"><b>{d.total}</b><br />Classifications</div>
      <div className="card"><b>{pct(d.average_confidence)}</b><br />Avg confidence</div>
      <div className="card"><b>{d.low_confidence_count}</b><br />Low-confidence</div></div>
      <h2>By category</h2>{Object.entries(d.by_category).map(([k, v]) => (
        <div key={k} className="bar"><span>{k} ({v})</span><i style={{ width: (v / d.total) * 100 + "%" }} /></div>))}</>}</>);
}
