import os
from pathlib import Path


def _load_env_file() -> None:
	env_path = Path(__file__).with_name(".env")
	if not env_path.exists():
		return

	for raw_line in env_path.read_text(encoding="utf-8").splitlines():
		line = raw_line.strip()
		if not line or line.startswith("#") or "=" not in line:
			continue

		key, value = line.split("=", 1)
		key = key.strip()
		value = value.strip().strip('"').strip("'")
		os.environ.setdefault(key, value)


_load_env_file()

TOKEN = os.getenv("TOKEN")
API_TOKEN = os.getenv("API_TOKEN")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
MY_ID = int(os.getenv("myID", "0"))