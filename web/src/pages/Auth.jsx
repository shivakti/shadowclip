import React, { useState } from "react";
import axios from "axios";

export default function Auth() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLogin, setIsLogin] = useState(true);
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const endpoint = isLogin ? "/login" : "/register";
      const response = await axios.post(`http://127.0.0.1:8000${endpoint}`, {
        email,
        password,
      });
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data?.detail || "Something went wrong");
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: "0 auto", textAlign: "center" }}>
      <h2>{isLogin ? "Login" : "Register"}</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{ display: "block", marginBottom: 10, width: "100%" }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{ display: "block", marginBottom: 10, width: "100%" }}
        />
        <button type="submit" style={{ width: "100%" }}>
          {isLogin ? "Login" : "Register"}
        </button>
      </form>

      <button onClick={() => setIsLogin(!isLogin)} style={{ marginTop: 20 }}>
        {isLogin ? "Create an account" : "Already have an account? Login"}
      </button>

      <p style={{ marginTop: 15 }}>{message}</p>
    </div>
  );
}
