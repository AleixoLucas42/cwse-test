FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    LANG=C.UTF-8 \
    PATH=/home/botuser/.local/bin:$PATH

RUN apt-get update && apt-get install -y --no-install-recommends \
    binutils \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash botuser

RUN mkdir -p /app/alerts /app/downloads /app/session \
    && chown -R botuser:botuser /app

WORKDIR /app
USER botuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir pyinstaller

COPY --chown=botuser:botuser main.py .

RUN pyinstaller --onefile main.py --name cwse-bot

VOLUME ["/app/alerts", "/app/session"]

CMD ["./dist/cwse-bot"]
