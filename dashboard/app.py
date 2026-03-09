from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import subprocess
import os
import sys
import threading
import time
from collections import deque
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

processes = {}
logs = {
    "kernel": deque(maxlen=100),
    "sim": deque(maxlen=100),
    "sdk": deque(maxlen=100)
}

def monitor_process(name, proc):
    def read_stream(stream, is_stderr):
        for line in iter(stream.readline, ''):
            if line:
                logs[name].append(line.strip())
            else:
                break
        stream.close()

    if proc.stdout:
        t_out = threading.Thread(target=read_stream, args=(proc.stdout, False))
        t_out.daemon = True
        t_out.start()
    
    if proc.stderr:
        t_err = threading.Thread(target=read_stream, args=(proc.stderr, True))
        t_err.daemon = True
        t_err.start()

# API Endpoints FIRST
@app.post("/start_kernel")
def start_kernel():
    if "kernel" in processes and processes["kernel"].poll() is None:
        return {"status": "already running"}
    
    cwd = os.path.abspath("kernel_rust")
    # Check if cargo exists
    try:
        proc = subprocess.Popen(
            ["cargo", "run"], 
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        processes["kernel"] = proc
        monitor_process("kernel", proc)
        return {"status": "started", "pid": proc.pid}
    except FileNotFoundError:
        logs["kernel"].append("Error: 'cargo' not found. Is Rust installed?")
        return {"status": "error", "message": "cargo not found"}

@app.post("/start_sim")
def start_sim():
    if "sim" in processes and processes["sim"].poll() is None:
        return {"status": "already running"}
    
    cwd = os.path.abspath("q_sim")
    # Using sys.executable to ensure we use the same python environment
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "sim_server:app", "--host", "0.0.0.0", "--port", "8001"], 
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    processes["sim"] = proc
    monitor_process("sim", proc)
    return {"status": "started", "pid": proc.pid}

@app.post("/run_sdk")
def run_sdk():
    cwd = os.path.abspath("q_sim/sdk_python")
    try:
        # Run SDK and capture output
        proc = subprocess.Popen(
            [sys.executable, "example.py"],
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        monitor_process("sdk", proc)
        processes["sdk"] = proc
        return {"status": "started", "pid": proc.pid}
    except Exception as e:
        return {"error": str(e)}

@app.get("/status")
def get_status():
    status = {}
    for name in ["kernel", "sim", "sdk"]:
        proc = processes.get(name)
        if proc and proc.poll() is None:
            status[name] = "running"
        else:
            status[name] = "stopped"
    return status

@app.get("/logs")
def get_logs():
    return {k: list(v) for k, v in logs.items()}

@app.post("/stop_all")
def stop_all():
    for name, proc in processes.items():
        if proc.poll() is None:
            proc.terminate()
    return {"status": "stopped all"}

# Mount StaticFiles LAST to catch-all
# We mount the 'dashboard' directory to root so that /index.html and /image.png work
app.mount("/", StaticFiles(directory="dashboard", html=True), name="static")

if __name__ == "__main__":
    # Bind to all interfaces at port 8080
    print("Starting Dashboard Server at http://0.0.0.0:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)
