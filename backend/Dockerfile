FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    xz-utils \
    libgomp1 \
    libxi6 \
    libxrender1 \
    libxkbcommon0 \
    libsm6 \
    libgl1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Blender
RUN wget -q https://download.blender.org/release/Blender3.6/blender-3.6.5-linux-x64.tar.xz \
    && tar -xf blender-3.6.5-linux-x64.tar.xz \
    && mv blender-3.6.5-linux-x64 /opt/blender \
    && ln -s /opt/blender/blender /usr/local/bin/blender \
    && rm blender-3.6.5-linux-x64.tar.xz

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/outputs /app/temp

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
