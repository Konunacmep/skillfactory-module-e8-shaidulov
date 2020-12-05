FROM python:3.9.0

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SECRET_KEY=never-guess

ENV FLASK_APP=counter.py

ENV DATABASE_URL=postgresql://postgres:123456@postgres:5432/queue

ENV BROKER_URL=redis://redis:6379/0

RUN chmod u+x ./entrypoint.sh
