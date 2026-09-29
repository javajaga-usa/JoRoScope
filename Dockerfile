# JoRoScope in a container, for any host that runs Docker images (Fly.io, Railway, a VPS).
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt requirements-ai.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV JOROSCOPE_HOST=0.0.0.0 PORT=8080 PYTHONUNBUFFERED=1
EXPOSE 8080
CMD ["python", "server.py", "--no-browser"]
