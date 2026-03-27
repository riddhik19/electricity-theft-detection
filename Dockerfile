FROM python:3.10-slim

WORKDIR /app

# Install system dependencies needed for LightGBM
RUN apt-get update && apt-get install -y libgomp1

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]