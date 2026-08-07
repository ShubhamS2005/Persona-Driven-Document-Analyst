# ============================================================
# Persona RAG - Backend
# Dockerfile
# ============================================================

FROM python:3.12-slim

# Prevent Python from writing .pyc files
# and ensure logs appear immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Application directory
WORKDIR /app

# System dependencies
#
# build-essential:
#   Required by some Python packages during installation.
#
# libgl1 / libglib2.0-0:
#   Useful for OpenCV-based document/image processing.
#
# git:
#   Useful if a dependency is installed from a Git repository.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first so Docker can cache
# the dependency installation layer.
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY . .

# Create runtime directories if they do not already exist.
#
# These directories are intentionally empty in Git.
# Uploaded documents and generated vector stores should
# normally be supplied/generated at runtime.
RUN mkdir -p data/uploads data/vector_store

# Flask API port
EXPOSE 5000

# Start Persona RAG backend
CMD ["python", "app.py"]