import { NavLink, Route, Routes } from "react-router-dom";
import Home from "./pages/Home"; import Classify from "./pages/Classify"; import Dashboard from "./pages/Dashboard"; import { History, Detail } from "./pages/History";
export default function App() {
  return (<><nav aria-label="Main"><b>♻ Cleantech</b>
    {[["/", "Home"], ["/classify", "Classify"], ["/dashboard", "Dashboard"], ["/history", "History"]].map(([to, l]) => <NavLink key={to} to={to} end={to === "/"}>{l}</NavLink>)}</nav>
    <main><Routes><Route path="/" element={<Home />} /><Route path="/classify" element={<Classify />} /><Route path="/dashboard" element={<Dashboard />} />
      <Route path="/history" element={<History />} /><Route path="/history/:id" element={<Detail />} /><Route path="*" element={<p>Page not found.</p>} /></Routes></main></>);
}
