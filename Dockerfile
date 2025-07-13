FROM python:3.11-slim

WORKDIR /CV-Algs-Apps-2ED

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["pytest"]
