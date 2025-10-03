import React, { useState } from "react";
import { login, getMe } from "../lib/api";

export default function Debug() {
  const [email, setEmail] = useState("test@example.com");
  const [password, setPassword] = useState("password123");
  const [result, setResult] = useState("");

  const testLogin = async () => {
    try {
      console.log("Testing login...");
      const loginResult = await login({ email, password });
      console.log("Login result:", loginResult);
      setResult(`Login successful: ${JSON.stringify(loginResult)}`);
      
      // wait a bit then test /me
      setTimeout(async () => {
        try {
          console.log("Testing /me...");
          const meResult = await getMe();
          console.log("Me result:", meResult);
          setResult(prev => prev + `\n/me successful: ${JSON.stringify(meResult)}`);
        } catch (error) {
          console.error("Me failed:", error);
          setResult(prev => prev + `\n/me failed: ${error.message}`);
        }
      }, 1000);
      
    } catch (error) {
      console.error("Login failed:", error);
      setResult(`Login failed: ${error.message}`);
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>Debug Login</h2>
      <div>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
        />
        <button onClick={testLogin}>Test Login</button>
      </div>
      <pre style={{ background: "#f5f5f5", padding: "1rem", marginTop: "1rem" }}>
        {result}
      </pre>
    </div>
  );
}
