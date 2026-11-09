#!/usr/bin/env bash
# اجرای سریع ربات: نصب وابستگی‌ها و شروع
set -e
cd "$(dirname "$0")"

if [ ! -f .env ]; then
    echo "خطا: فایل .env پیدا نشد. .env.example را به .env تغییر نام دهید و توکن را وارد کنید."
    exit 1
fi

python3 -m venv venv 2>/dev/null || true
source venv/bin/activate
pip install -q -r requirements.txt
python bot.py
