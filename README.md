# Full Stack Notes: React + FastAPI + SQLite (separate servers)

- `backend/`  FastAPI + SQLite, runs on EC2 #1, port 8000
- `frontend/` React (Vite), `dist/` is the committed build, served by Apache on EC2 #2, port 80

Backend EC2:  `cd backend/scripts && ./setup_backend.sh`
Frontend EC2: `cd frontend/scripts && ./setup_frontend.sh http://<BACKEND_PUBLIC_IP>:8000`
Rebuild frontend: `cd frontend && npm install && npm run build`
