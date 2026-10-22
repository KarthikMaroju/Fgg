import { useEffect, useState } from "react";
export function useAsync(fn, deps) {
  const [s, set] = useState({ loading: true, data: null, error: null });
  useEffect(() => { let on = true; set({ loading: true, data: null, error: null });
    fn().then((data) => on && set({ loading: false, data, error: null })).catch((e) => on && set({ loading: false, data: null, error: e.message }));
    return () => { on = false; }; }, deps);
  return s;
}
