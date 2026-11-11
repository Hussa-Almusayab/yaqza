"""Load and validate game levels (rooms) from the levels/ folder."""
import json
from pathlib import Path

from config import DOMAINS

LEVELS_DIR = Path(__file__).resolve().parent.parent / "levels"


class LevelError(ValueError):
    """Raised when a level file does not follow the expected schema."""


def validate_level(level: dict) -> None:
    for key in ("id", "title", "story", "questions"):
        if key not in level:
            raise LevelError(f"المفتاح المفقود: {key}")
    if not level["questions"]:
        raise LevelError(f"الغرفة {level['id']} بلا أسئلة")
    for q in level["questions"]:
        for key in ("id", "domain", "prompt", "options", "answer", "points", "explain"):
            if key not in q:
                raise LevelError(f"السؤال {q.get('id', '?')}: المفتاح المفقود {key}")
        if q["domain"] not in DOMAINS:
            raise LevelError(f"السؤال {q['id']}: مجال غير معروف {q['domain']}")
        if not 0 <= q["answer"] < len(q["options"]):
            raise LevelError(f"السؤال {q['id']}: رقم الإجابة خارج الخيارات")
        if q["points"] <= 0:
            raise LevelError(f"السؤال {q['id']}: النقاط يجب أن تكون موجبة")


def load_levels(directory: Path = LEVELS_DIR) -> list:
    levels = []
    for path in sorted(directory.glob("room*.json")):
        with open(path, encoding="utf-8") as f:
            level = json.load(f)
        validate_level(level)
        levels.append(level)
    ids = [q["id"] for lv in levels for q in lv["questions"]]
    if len(ids) != len(set(ids)):
        raise LevelError("معرّفات الأسئلة يجب أن تكون فريدة")
    return levels
