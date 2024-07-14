from pathlib import Path

from src.service.fix_runner import run_client


if __name__ == "__main__":
    config_path = Path(__file__).resolve().parents[1] / "resources" / "client.cfg"
    run_client(config_path)
