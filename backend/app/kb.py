"""Tiny knowledge base: loads verified procedure JSON files from data/procedures/."""
import json
from pathlib import Path
from typing import Dict
from .schemas import Procedure

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "procedures"


def load_all() -> Dict[str, Procedure]:
    procs: Dict[str, Procedure] = {}
    for f in sorted(DATA_DIR.glob("*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        p = Procedure(**data)          # raises if the file breaks the schema
        procs[p.id] = p
    return procs
