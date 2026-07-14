FROM python:3.13-alpine

WORKDIR /usr/src

COPY app app/
COPY dist dist/

COPY gunicorn.conf.py .
COPY requirements.docker.g.txt .

RUN pip install -r requirements.docker.g.txt

CMD ["gunicorn", "app.builder:build_app()"]