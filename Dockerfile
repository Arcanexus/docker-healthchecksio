# Stage 1: Build stage
FROM python:3.12-alpine AS build

# Install build dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

# Set work directory
WORKDIR /app

# Copy requirements.txt
COPY src/requirements.txt .

# Install dependencies
RUN pip install -U pip && pip install --no-cache-dir -r requirements.txt

# Stage 2: Run stage
FROM python:3.12-alpine

# Copy only the necessary files from the build stage
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

# Set work directory
WORKDIR /app

# Copy the source code
COPY src/main.py ./main.py
COPY src/config ./config

# Command to run the script
CMD ["python", "main.py"]
