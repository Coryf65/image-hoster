FROM python:3.12-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV IMAGE_HOSTER_DIR=/app/images

RUN mkdir -p /app/images

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./

EXPOSE 8000

CMD ["python", "main.py"]
