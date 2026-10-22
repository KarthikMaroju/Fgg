export const Status = ({ s, empty }) => s.loading ? <p role="status">Loading…</p> : s.error ? <p className="err" role="alert">{s.error}</p> : empty ? <p className="muted">{empty}</p> : null;
export const pct = (x) => (x * 100).toFixed(1) + "%";
export function Result({ record, recommendation, notice }) {
  return (<section className="card" aria-live="polite">
    <h2>{record.category} <small>{pct(record.confidence)}</small></h2>
    {record.low_confidence && <p className="warn">⚠ Low confidence prediction. Verify manually.</p>}
    {record.alternatives.length > 0 && <p className="muted">Alternatives: {record.alternatives.map((a) => `${a.category} (${pct(a.confidence)})`).join(", ")}</p>}
    <h3>Guidance</h3>
    <ul><li><b>Disposal:</b> {recommendation.disposal}</li><li><b>Recycling:</b> {recommendation.recycling}</li>
      <li><b>Preparation:</b> {recommendation.preparation}</li><li><b>Warning:</b> {recommendation.warning}</li></ul>
    <p className="muted">{recommendation.disclaimer} {notice}</p></section>);
}
