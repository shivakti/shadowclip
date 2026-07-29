import { Routes, Route, Link } from "react-router-dom";
import Auth from "./pages/Auth";

function Home() {
  return (
    <div style={{ textAlign: "center", marginTop: 100 }}>
      <h1>Welcome to ShadowClip ⚡</h1>
      <Link to="/auth">Go to Auth Page</Link>
    </div>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/auth" element={<Auth />} />
    </Routes>
  );
}
