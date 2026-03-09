"""
Lancez tout avec : python run.py
- Active automatiquement le venv si présent
- Lance FastAPI + Streamlit en parallèle
- Ctrl+C pour tout stopper proprement
"""
import subprocess
import sys
import threading
from pathlib import Path
import time 

# ── Couleurs terminal ──────────────────────────────────────────
CYAN  = "\033[96m"
GREEN = "\033[92m"
RED   = "\033[91m"
RESET = "\033[0m"
BOLD  = "\033[1m"

# ── CONFIGUREZ VOTRE VENV ICI ─────────────────────────────────
# Exemples :
#   VENV_PATH = "venv"                          # venv/ à la racine du projet
#   VENV_PATH = ".venv"                         # .venv/ à la racine
#   VENV_PATH = "~/monprojet/venv"              # chemin absolu avec ~
#   VENV_PATH = None                            # pas de venv, utilise le python courant
VENV_PATH = "venv"  # ← modifiez cette ligne
# ─────────────────────────────────────────────────────────────


def find_python() -> str:
    """Résout le python à utiliser selon VENV_PATH."""
    if VENV_PATH is not None:
        # expanduser gère le ~ correctement
        venv = Path(VENV_PATH).expanduser().resolve()
        candidates = [
            venv / "bin" / "python",
            venv / "bin" / "python3",
            venv / "Scripts" / "python.exe",  # Windows
        ]
        for candidate in candidates:
            if candidate.exists():
                print(f"{GREEN}✓ Venv trouvé : {candidate}{RESET}")
                return str(candidate)
        print(f"{RED}✗ Venv introuvable : {venv}{RESET}")
        print(f"{RED}  Vérifiez VENV_PATH dans run.py{RESET}")
        sys.exit(1)

    print(f"{CYAN}ℹ Pas de venv configuré, utilisation de : {sys.executable}{RESET}")
    return sys.executable


def stream_logs(label: str, proc: subprocess.Popen, color: str):
    for line in proc.stdout:
        print(f"{color}[{label}]{RESET} {line}", end="", flush=True)


def main():
    python = find_python()
    processes = []

    print(f"\n{BOLD}🚀 Démarrage de smart-doc-search{RESET}\n")

    try:
        api = subprocess.Popen(
            [python, "-m", "uvicorn", "src.api.main:app", "--reload", "--port", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        processes.append(("API", api, CYAN))
        print(f"{CYAN}▶ FastAPI   → http://localhost:8000{RESET}")

        st = subprocess.Popen(
            [python, "-m", "streamlit", "run", "app.py", "--server.port", "8501"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        processes.append(("UI ", st, GREEN))
        print(f"{GREEN}▶ Streamlit → http://localhost:8501{RESET}")
        print(f"\n{BOLD}Ctrl+C pour tout stopper{RESET}\n")

        for label, proc, color in processes:
            t = threading.Thread(target=stream_logs, args=(label, proc, color), daemon=True)
            t.start()

        while all(p.poll() is None for _, p, _ in processes):
            time.sleep(0.5)
            pass

    except KeyboardInterrupt:
        print(f"\n{RED}⏹ Arrêt demandé...{RESET}")

    finally:
        for label, proc, _ in processes:
            if proc.poll() is None:
                proc.terminate()
                print(f"{RED}✗ {label.strip()} arrêté{RESET}")
        print(f"{BOLD}Bye !{RESET}\n")


if __name__ == "__main__":
    main()