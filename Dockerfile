FROM python:3.10-slim

WORKDIR /usr/src/app

COPY src/pontedera.py ./src/pontedera.py
COPY src/wsgi.py ./src/wsgi.py
COPY src/wsgi.ini ./src/wsgi.ini
COPY src/routes/ ./src/routes/
COPY src/static/ ./src/static/
COPY src/templates/ ./src/templates/
COPY requirements.txt requirements.txt

RUN apt update
RUN apt install -y build-essential python-dev
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./src/pontedera.py"]
