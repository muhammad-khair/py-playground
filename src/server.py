from pathlib import Path

from src.service.fix_runner import run_server


if __name__ == "__main__":
    config_path = Path(__file__).resolve().parents[1] / "resources" / "server.cfg"
    run_server(config_path)
