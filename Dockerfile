FROM python:3.10-slim

WORKDIR /usr/src/app

COPY src/pontedera.py ./src/pontedera.py
COPY src/routes/ ./src/routes/
COPY src/static/ ./src/static/
COPY src/templates/ ./src/templates/
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./src/pontedera.py"]
