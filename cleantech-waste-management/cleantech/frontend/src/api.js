async function req(url, opts) {
  let res;
  try { res = await fetch(url, opts); } catch { throw new Error("Cannot reach the server. Is the backend running?"); }
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(typeof body.detail === "string" ? body.detail : "Request failed.");
  return body;
}
export const classify = (file) => { const f = new FormData(); f.append("file", file); return req("/api/classify", { method: "POST", body: f }); };
export const getHistory = (p) => req("/api/history?" + new URLSearchParams(p));
export const getRecord = (id) => req(`/api/history/${id}`);
export const deleteRecord = (id) => req(`/api/history/${id}`, { method: "DELETE" });
export const getStats = () => req("/api/statistics");
