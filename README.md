# Word Stats API

## Функционал

- Принимает текстовый файл (.txt)
- Считает частоту слов (с приведением к начальной форме)
- Показывает, в каких строках встречалось каждое слово
- Возвращает результат в формате .xlsx

## Как запустить

### 1. Клонировать репозиторий
git clone https://github.com/XuGIN/word_stats.git
cd word_stats

### 2. Создать виртуальное окружение
python -m venv venv
. venv/bin/activate

### 3. Установить зависимости
pip install -r requirements.txt

### 4. Запустить сервер
uvicorn app.main:app --reload

## Использование

-  Открой в браузере http://127.0.0.1:8000/docs
-  Найди эндпоинт POST /public/report/export Process File
-  Нажми на него и нажми Try it out
-  Выбери текстовый файл для проверки и нажми Execute
-  Скачай файл в формате xlsx с результатом

## Технологии

- FastAPI
- pymorphy3 (для лемматизации)
- openpyxl (для Excel)

