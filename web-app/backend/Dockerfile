FROM python:3.11.11-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --progress-bar=on --timeout=1000 --retries=5 -r requirements.txt

EXPOSE 5000

ENV FLASK_ENV=development

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]