"""Streamlit game app. Run with:  streamlit run app.py"""
import os
import streamlit as st

from config import APP_NAME, APP_NAME_EN, DISCLAIMER, DOMAINS, TAGLINE
from engine.levels import load_levels
from engine.scoring import build_report, score_answers

# تحديد مسار الصورة تلقائياً بجانب ملف app.py
LOGO_PATH = os.path.join(os.path.dirname(__file__), "logo.png")

st.set_page_config(page_title=f"{APP_NAME} | {APP_NAME_EN}", page_icon=LOGO_PATH, layout="centered")

st.markdown(
    """
    <style>
    @font-face {
      font-family: 'Cairo';
      font-style: normal;
      font-weight: 400;
      src: url(https://gstatic.com) format('truetype');
    }
    @font-face {
      font-family: 'Cairo';
      font-style: normal;
      font-weight: 700;
      src: url(https://gstatic.com) format('truetype');
    }

    /* تثبيت المظهر الداكن واتجاه اليمين لليسار على الجوال والآيباد واللابتوب */
    html, body, [class*="css"], .stApp, [data-testid="stHeader"] { 
        font-family: 'Cairo', sans-serif !important;
        background-color: #0f172a !important;
        color: #f8fafc !important;
        direction: rtl !important;
    }

    /* ضبط حاوية المحتوى لتتجاوب بسلاسة مع شاشة الجوال */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 760px !important;
    }

    /* الشريط الجانبي */
    [data-testid="stSidebar"] {
        background-color: #1e293b !important;
        direction: rtl !important;
        text-align: center !important;
    }

    /* البطاقات ذات الحدود */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 14px !important;
        padding: 0.5rem !important;
        direction: rtl !important;
    }

    /* توسيط العناوين الرئيسية */
    h1, h2, h3 {
        color: #f8fafc !important;
        text-align: center !important;
        direction: rtl !important;
    }

    /* محاذاة النصوص والأسئلة والخيارات لليمين لراحة القراءة على الجوال */
    p, label, .stMarkdown, .stCaption, div[role="radiogroup"] label {
        color: #f8fafc !important;
        text-align: right !important;
        direction: rtl !important;
        line-height: 1.7 !important;
    }

    /* صناديق التنبيه والملاحظات بألوان ثابتة لا تتأثر بوضع الجهاز */
    [data-testid="stAlert"] {
        background-color: #1e293b !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 10px !important;
        direction: rtl !important;
        text-align: right !important;
    }
    [data-testid="stAlert"] p {
        color: #e2e8f0 !important;
        text-align: right !important;
    }

    /* تنسيق الأزرار لتكون بعرض كامل ومريحة للمس على الجوال */
    .stButton > button, .stDownloadButton > button {
        width: 100% !important;
        background-color: #10B981 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 0.6rem 1rem !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background-color: #059669 !important;
    }

    /* توسيط الشعار */
    [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
    }

    /* إبقاء الأكواد والأدلة التقنية من اليسار لليمين مع تمرير أفقي على الجوال */
    pre, code { 
        direction: ltr !important; 
        text-align: left !important; 
        overflow-x: auto !important;
    }

    /* تحسين عرض مقاييس الدرجات على الجوال */
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        text-align: center !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

levels = load_levels()
ss = st.session_state
ss.setdefault("stage", "intro")      # intro | room | report
ss.setdefault("room", 0)
ss.setdefault("answers", {})         # question id -> chosen option index
ss.setdefault("checked", [])         # room ids already checked


def restart():
    for key in list(ss.keys()):
        del ss[key]


def render_sidebar():
    with st.sidebar:
        st.image(LOGO_PATH, width=100)
        st.header(APP_NAME)
        st.markdown(f"<p style='text-align: center !important; color: #94a3b8 !important;'>{TAGLINE}</p>", unsafe_allow_html=True)
        st.divider()
        
        st.markdown("<h3 style='color: #38bdf8 !important; font-size: 1.1rem;'>إعداد وتصميم:<br>حصه بنت فهد المسيب</h3>", unsafe_allow_html=True)
        st.divider()
        
        if ss.stage == "room":
            st.metric("التقدم الحالي", f"الغرفة {ss.room + 1} من {len(levels)}")
            st.metric("الغرف المكتملة", f"{len(ss.checked)} / {len(levels)}")
            st.divider()
        elif ss.stage == "report":
            st.success("اكتملت جميع المهام بنجاح!")
            st.divider()

        if ss.stage != "intro":
            st.button("🔄 إعادة تشغيل اللعبة", on_click=restart)


def show_intro():
    with st.container(border=True):
        st.image(LOGO_PATH, width=140)
        st.title(APP_NAME)
        st.markdown(f"<p style='text-align: center !important; color: #38bdf8 !important; font-weight: 600;'>{TAGLINE}</p>", unsafe_allow_html=True)
        st.divider()
        st.write(
            "أنت مسؤول الأمن في شركة وهمية. في كل غرفة موقف من مواقف العمل، "
            "وعليك أن تتصرف كما يتصرف المحترفون، وفي النهاية تحصل على تقرير بدرجتك لكل مجال."
        )
        st.info(
            "مشروع تعليمي مستوحى من مبادئ الضوابط الأساسية للأمن السيبراني (NCA ECC)، "
            "وهو ليس أداة امتثال رسمية ولا بديلًا عن التقييم المتخصص، وجميع البيانات والسيناريوهات الواردة فيه وهمية."
        )
        st.write("")
        if st.button("🚀 ابدأ اللعبة الآن", type="primary"):
            ss.stage = "room"
            st.rerun()


def show_room():
    level = levels[ss.room]
    st.progress((ss.room + 1) / len(levels), text=f"الغرفة {ss.room + 1} من {len(levels)}")

    with st.container(border=True):
        st.header(f"🚪 {level['title']}")
        st.write(level["story"])
        if level.get("evidence"):
            st.caption("🔍 الدليل التقني / سجل النظام:")
            st.code(level["evidence"], language="text")

    checked = level["id"] in ss.checked
    for idx, q in enumerate(level["questions"], 1):
        with st.container(border=True):
            st.markdown(f"**السؤال {idx}: {q['prompt']}**")
            st.caption(f"المجال: {DOMAINS[q['domain']]} | النقاط: {q['points']}")
            choice = st.radio(
                "اختر إجابة", q["options"], index=None,
                key=f"radio_{q['id']}", disabled=checked, label_visibility="collapsed",
            )
            if choice is not None:
                ss.answers[q["id"]] = q["options"].index(choice)
            if not checked:
                with st.expander("💡 تلميح"):
                    st.write(q["hint"])
            else:
                if ss.answers.get(q["id"]) == q["answer"]:
                    st.success(f"✅ صحيح! {q['explain']}")
                else:
                    st.error(f"❌ الإجابة الصحيحة: {q['options'][q['answer']]}. {q['explain']}")

    if not checked:
        if st.button("✔️ تحقق من إجاباتي", type="primary"):
            if all(q["id"] in ss.answers for q in level["questions"]):
                ss.checked.append(level["id"])
                st.toast("تم تسجيل إجاباتك!", icon="✅")
                st.rerun()
            else:
                st.warning("⚠️ أجب عن جميع الأسئلة أولاً.")
    else:
        last = ss.room == len(levels) - 1
        btn_label = "📊 عرض التقرير النهائي" if last else "➡️ الانتقال للغرفة التالية"
        if st.button(btn_label, type="primary"):
            if last:
                ss.stage = "report"
            else:
                ss.room += 1
            st.rerun()


def show_report():
    result = score_answers(levels, ss.answers)
    if result["total_percent"] >= 80:
        st.balloons()

    with st.container(border=True):
        st.title("📋 تقريرك الأمني النهائي")
        st.metric("الدرجة الكلية", f"{result['total_percent']}%", result["grade"])
        st.divider()
        cols = st.columns(len(DOMAINS))
        for col, (key, label) in zip(cols, DOMAINS.items()):
            pct = result["domains"][key]["percent"]
            col.metric(label, "لم يُختبر" if pct is None else f"{pct}%")

    with st.expander("📄 نص التقرير الكامل", expanded=bool(result["mistakes"])):
        report = build_report(result, APP_NAME)
        st.markdown(report)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📥 تحميل التقرير (Markdown)", report, file_name="report.md", mime="text/markdown")
    with col2:
        st.button("🔄 العب من جديد", on_click=restart, type="primary")


render_sidebar()
{"intro": show_intro, "room": show_room, "report": show_report}[ss.stage]()
