import json
from pathlib import Path
from typing import List

class MemoryManager:
    def __init__(self, base_dir: str = "memory"):
        self.base_path = Path(base_dir)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _file_for_asset(self, asset: str) -> Path:
        safe_name = asset.replace(" ", "_").lower()
        return self.base_path / f"{safe_name}.json"

    def append_entry(self, asset: str, entry: str) -> None:
        file_path = self._file_for_asset(asset)
        history = []
        if file_path.exists():
            with file_path.open("r", encoding="utf-8") as f:
                history = json.load(f)
        history.append(entry)
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

    def get_history(self, asset: str) -> List[str]:
        file_path = self._file_for_asset(asset)
        if not file_path.exists():
            return []
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)
