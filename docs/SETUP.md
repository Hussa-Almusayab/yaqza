# إعداد المشروع على Windows (مرة واحدة)

## 1) البرامج المطلوبة
تأكدي في Terminal (PowerShell) من وجودها:

    python --version     (يجب أن يظهر 3.10 أو أحدث)
    git --version
    code --version       (VS Code)

إن غاب أحدها: ثبّتي Python من python.org (فعّلي خيار Add python.exe to PATH)، وGit من git-scm.com، وVS Code من code.visualstudio.com، ثم أغلقي PowerShell وافتحيه من جديد.

## 2) هوية Git (مرة واحدة على الجهاز)

    git config --global user.name "Hussa Almusayab"
    git config --global user.email "بريدك المرتبط بحساب GitHub"

## 3) تشغيل اللعبة

    cd المجلد\yaqza
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    streamlit run app.py

إن منع PowerShell تفعيل البيئة: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` ثم أعيدي الأمر.

## 4) الاختبارات

    pip install -r requirements-dev.txt
    pytest -q
