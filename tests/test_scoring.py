from engine.levels import load_levels
from engine.scoring import build_report, grade_for, score_answers


def all_correct(levels):
    return {q["id"]: q["answer"] for lv in levels for q in lv["questions"]}


def test_perfect_score():
    levels = load_levels()
    result = score_answers(levels, all_correct(levels))
    assert result["total_percent"] == 100
    assert result["mistakes"] == []


def test_empty_answers_score_zero_and_list_mistakes():
    levels = load_levels()
    result = score_answers(levels, {})
    assert result["total_percent"] == 0
    assert len(result["mistakes"]) == sum(len(lv["questions"]) for lv in levels)


def test_one_wrong_answer_lowers_only_its_domain():
    levels = load_levels()
    answers = all_correct(levels)
    answers["r1q1"] = (answers["r1q1"] + 1) % 4   # wrong on a defense question
    result = score_answers(levels, answers)
    assert result["domains"]["defense"]["percent"] < 100
    assert result["domains"]["governance"]["percent"] == 100


def test_grade_thresholds():
    assert grade_for(90) == "ممتاز"
    assert grade_for(70) == "جيد"
    assert grade_for(50) == "يحتاج تحسينًا"
    assert grade_for(10).startswith("ضعيف")


def test_report_mentions_app_name():
    levels = load_levels()
    report = build_report(score_answers(levels, {}), "اسم")
    assert "تقرير اسم" in report
