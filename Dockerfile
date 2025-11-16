FROM python:3.14.0-slim-bookworm

WORKDIR /app

RUN apt update -y && \
	apt install -y procps && \
	rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]