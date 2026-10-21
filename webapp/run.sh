#!/bin/bash
# Один скрипт: готує окреме середовище, навчає модель, створює базу і запускає сайт.
# Запуск:  bash run.sh
cd "$(dirname "$0")" || exit 1

if [ ! -d ".venv" ]; then
  echo ">>> Створюю окреме середовище Python (.venv)..."
  python3 -m venv .venv || { echo "Не вдалося створити середовище. Перевірте, що встановлено Python 3."; exit 1; }
fi
source .venv/bin/activate

echo ">>> Встановлюю бібліотеки (перший раз це може тривати кілька хвилин)..."
pip install -q -r requirements.txt || { echo "Не вдалося встановити бібліотеки."; exit 1; }

echo ">>> Навчаю модель..."
python train_model.py || { echo "Помилка під час навчання моделі."; exit 1; }

echo ">>> Готую базу даних..."
python manage.py makemigrations predictor
python manage.py migrate

echo ">>> Запускаю сайт. Відкрийте в браузері: http://127.0.0.1:8000/"
echo ">>> Зупинити сайт: Ctrl + C"
python manage.py runserver
