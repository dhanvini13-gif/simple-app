import { useEffect, useState } from "react";

const API = window.API_URL || "http://localhost:8000";

export default function App() {
  const [notes, setNotes] = useState([]);
  const [text, setText] = useState("");

  useEffect(() => {
    fetch(`${API}/api/notes`).then((r) => r.json()).then(setNotes);
  }, []);

  const add = async () => {
    if (!text.trim()) return;
    const res = await fetch(`${API}/api/notes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    setNotes(await res.json());
    setText("");
  };

  const remove = async (id) => {
    const res = await fetch(`${API}/api/notes/${id}`, { method: "DELETE" });
    setNotes(await res.json());
  };

  return (
    <div style={{ maxWidth: 480, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>Notes: React + FastAPI + SQLite</h1>
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && add()}
        placeholder="Write a note"
        style={{ padding: 8, width: "65%" }}
      />
      <button onClick={add} style={{ padding: 8, marginLeft: 8 }}>Add</button>
      <ul style={{ paddingLeft: 20 }}>
        {notes.map((n) => (
          <li key={n.id} style={{ margin: "8px 0" }}>
            {n.text}
            <button onClick={() => remove(n.id)} style={{ marginLeft: 10 }}>
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
