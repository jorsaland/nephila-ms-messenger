FROM python:3.13-alpine

WORKDIR /usr/src

COPY app app/
COPY dist dist/

COPY waitress.serve.py .
COPY requirements.docker.w.txt .

RUN pip install -r requirements.docker.w.txt

CMD ["python", "waitress.serve.py"]