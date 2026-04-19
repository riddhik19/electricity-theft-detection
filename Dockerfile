FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for LightGBM
RUN apt-get update && apt-get install -y libgomp1

COPY . .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Default = run pipeline (for CI)
CMD ["python", "run_full_test.py"]