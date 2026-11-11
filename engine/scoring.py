"""Scoring and Arabic report generation."""
from config import DOMAINS, GRADES


def grade_for(percent: float) -> str:
    for threshold, label in GRADES:
        if percent >= threshold:
            return label
    return GRADES[-1][1]


def score_answers(levels: list, answers: dict) -> dict:
    """answers maps question id -> chosen option index. Missing = wrong."""
    per_domain = {d: {"earned": 0, "max": 0} for d in DOMAINS}
    mistakes = []
    for level in levels:
        for q in level["questions"]:
            d = per_domain[q["domain"]]
            d["max"] += q["points"]
            if answers.get(q["id"]) == q["answer"]:
                d["earned"] += q["points"]
            else:
                chosen = answers.get(q["id"])
                mistakes.append({
                    "room": level["title"],
                    "prompt": q["prompt"],
                    "your_answer": q["options"][chosen] if chosen is not None else "لم تُجيبي",
                    "correct_answer": q["options"][q["answer"]],
                    "explain": q["explain"],
                })
    for d in per_domain.values():
        d["percent"] = round(100 * d["earned"] / d["max"]) if d["max"] else None
    total_earned = sum(d["earned"] for d in per_domain.values())
    total_max = sum(d["max"] for d in per_domain.values())
    total_percent = round(100 * total_earned / total_max) if total_max else 0
    return {
        "domains": per_domain,
        "total_earned": total_earned,
        "total_max": total_max,
        "total_percent": total_percent,
        "grade": grade_for(total_percent),
        "mistakes": mistakes,
    }


def build_report(result: dict, app_name: str) -> str:
    lines = [f"# تقرير {app_name}", ""]
    lines.append(f"**الدرجة الكلية:** {result['total_percent']}% ({result['grade']})")
    lines.append(f"**النقاط:** {result['total_earned']} من {result['total_max']}")
    lines += ["", "## الدرجة لكل مجال"]
    for key, label in DOMAINS.items():
        d = result["domains"][key]
        if d["percent"] is None:
            lines.append(f"- {label}: لم يُختبر بعد")
        else:
            lines.append(f"- {label}: {d['percent']}% ({grade_for(d['percent'])})")
    lines += ["", "## ما يحتاج مراجعة"]
    if not result["mistakes"]:
        lines.append("لا أخطاء. أحسنت!")
    for m in result["mistakes"]:
        lines += [
            f"### {m['room']}",
            f"- السؤال: {m['prompt']}",
            f"- إجابتك: {m['your_answer']}",
            f"- الإجابة الصحيحة: {m['correct_answer']}",
            f"- لماذا: {m['explain']}",
            "",
        ]
    return "\n".join(lines)
