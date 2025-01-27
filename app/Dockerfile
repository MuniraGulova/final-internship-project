# минимальный образ python (slim) для сокращения размера
FROM python:3.12.5-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# добавление всех файлов с текущей директории в папку app на контейнере
COPY requirements.txt requirements.txt

# Устанавливаем зависимости
RUN pip install -r requirements.txt

COPY . .

# Порт который приложение будет использовать
EXPOSE 5000

CMD ["python", "web_app.py"]
