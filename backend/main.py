import sqlite3
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DB_FILE = Path(__file__).resolve().parent / "app.db"

app = FastAPI(title="Notes API")

# Allow the frontend (on another server) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


with get_conn() as conn:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS notes ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "text TEXT NOT NULL)"
    )


class Note(BaseModel):
    text: str


@app.get("/")
def root():
    return {"message": "Notes API is running. See /docs"}


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/notes")
def list_notes():
    with get_conn() as conn:
        rows = conn.execute("SELECT id, text FROM notes ORDER BY id DESC").fetchall()
    return [dict(r) for r in rows]


@app.post("/api/notes")
def add_note(note: Note):
    if not note.text.strip():
        raise HTTPException(status_code=400, detail="Text is empty")
    with get_conn() as conn:
        conn.execute("INSERT INTO notes (text) VALUES (?)", (note.text.strip(),))
    return list_notes()


@app.delete("/api/notes/{note_id}")
def delete_note(note_id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    return list_notes()
