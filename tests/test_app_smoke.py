from pathlib import Path

from streamlit.testing.v1 import AppTest

from engine.levels import load_levels

APP = str(Path(__file__).resolve().parent.parent / "app.py")


def test_app_starts_without_error():
    at = AppTest.from_file(APP).run(timeout=30)
    assert not at.exception
    assert any("ابدأ اللعبة" in b.label for b in at.button)


def test_play_through_to_report():
    at = AppTest.from_file(APP).run(timeout=30)
    at.button[0].click().run()                    # start
    for _ in range(len(load_levels())):           # every room
        for radio in at.radio:
            radio.set_value(radio.options[0])
        at.run()
        at.button[0].click().run()                # check
        at.button[0].click().run()                # next / report
    assert not at.exception
    assert any("تقريرك" in t.value for t in at.title)
