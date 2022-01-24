FROM python:3.8-slim-bullseye as BASE_IMAGE

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN apt update && apt install -y\
    build-essential \
    iputils-ping \
    libffi-dev \
    openssh-client \
    python-dev \
    wakeonlan \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


FROM BASE_IMAGE
WORKDIR /usr/src/app
COPY src/pontedera.py ./src/pontedera.py
COPY src/pontedera.ini ./src/pontedera.ini
COPY src/routes/ ./src/routes/
COPY src/services/ ./src/services/
COPY src/static/ ./src/static/
COPY src/templates/ ./src/templates/
COPY src/utils/ ./src/utils/

CMD ["wsgi", "--ini", "./src/pontedera.ini"]
