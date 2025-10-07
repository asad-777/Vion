"use client";

import { useState } from "react";

export default function Home() {
  const [inputValue, setInputValue] = useState(""); // text from input
  const [ans, setAns] = useState(null);            // API response
  const [loading, setLoading] = useState(false);   // loading state

  const handleFetch = async () => {
    if (!inputValue) return; // don't fetch empty input
    setLoading(true);
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/input/${encodeURIComponent(inputValue)}`
      );
      const data = await res.json();
      setAns(data);
    } catch (err) {
      console.error("Fetch error:", err);
      setAns({ error: "Failed to fetch" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>FastAPI Input Tester</h1>

      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        placeholder="Type something..."
        className="border-2 p-4 w-1/3"
      />

      <button onClick={handleFetch} style={{ padding: "0.5rem 1rem" }}>
        Send
      </button>

      <div style={{ marginTop: "1rem" }}>
        {loading && <p>Loading...</p>}
        {ans && <p>Response: {JSON.stringify(ans)}</p>}
      </div>
    </div>
  );
}
