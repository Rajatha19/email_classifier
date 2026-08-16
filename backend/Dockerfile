FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY scripts ./scripts
COPY training ./training
COPY streaming ./streaming
COPY models ./models
ENV PYTHONUNBUFFERED=1 PORT=8044 FORWARDED_ALLOW_IPS="*"
EXPOSE 8044
CMD ["sh", "-c", "python -m scripts.seed_if_empty && uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --proxy-headers"]
