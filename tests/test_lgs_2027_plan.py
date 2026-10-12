from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_lgs_2027_plan", ROOT / "tools" / "build_lgs_2027_plan.py"
)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def built_plan() -> dict:
    return builder.build_plan(load(builder.INVENTORY), load(builder.REGISTRY))


def test_committed_plan_matches_inventory() -> None:
    expected = builder.render(built_plan(), builder.INVENTORY)
    assert builder.PLAN.read_text(encoding="utf-8") == expected


def test_inventory_covers_every_question_of_three_exams() -> None:
    inventory = load(builder.INVENTORY)
    assert len(inventory["questions"]) == 3 * 90
    for subject, definition in inventory["subjects"].items():
        for year in builder.YEARS:
            numbers = sorted(
                q["qNo"] for q in inventory["questions"] if q["subject"] == subject and str(q["year"]) == year
            )
            assert numbers == list(range(1, definition["questionsPerExam"] + 1)), (subject, year)


def test_answers_follow_the_recorded_answer_keys() -> None:
    inventory = load(builder.INVENTORY)
    for label, key in inventory["answerKeys"].items():
        year, rest = label.split(" ", 1)
        subject, booklet = rest.rsplit(" ", 1)
        answers = [
            q["answer"]
            for q in sorted(inventory["questions"], key=lambda q: q["qNo"])
            if str(q["year"]) == year and q["subject"] == subject and q["booklet"] == booklet
        ]
        assert "".join(answers) == key, label


def test_predicted_exam_form_and_bank_quotas_add_up() -> None:
    plan = built_plan()
    assert sum(subject["bankQuota"] for subject in plan["subjects"].values()) == plan["bankSize"]
    for name, subject in plan["subjects"].items():
        assert sum(unit["predictedPerExam"] for unit in subject["units"]) == subject["questionsPerExam"], name
        assert sum(unit["bankQuota"] for unit in subject["units"]) == subject["bankQuota"], name
        for unit in subject["units"]:
            assert sum(row["bankQuota"] for row in unit["kazanimlar"]) == unit["bankQuota"], (name, unit["key"])
        for mix in ("itemTypeMix", "difficultyMix"):
            assert sum(item["bankQuota"] for item in subject[mix]) == subject["bankQuota"], (name, mix)


def test_math_task_quotas_cover_every_current_task() -> None:
    plan = built_plan()
    math = plan["subjects"]["Matematik"]
    assert len(math["taskQuotas"]) == 28
    assert sum(math["taskQuotas"].values()) == math["bankQuota"]


def test_untestable_kazanimlar_receive_no_quota() -> None:
    plan = built_plan()
    for subject in plan["subjects"].values():
        for unit in subject["units"]:
            for row in unit["kazanimlar"]:
                if row["testability"] == "none":
                    assert row["bankQuota"] == 0
