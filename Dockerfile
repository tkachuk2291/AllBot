FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requiremnt.txt .
RUN pip install --no-cache-dir -r requiremnt.txt qrcode
COPY *.py .
WORKDIR /data
CMD ["python", "/app/main.py"]