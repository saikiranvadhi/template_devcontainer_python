FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Adding path to system environment variable
ENV BASEPATH="/crm_ai"
ENV PYTHONPATH="$PYTHONPATH:$BASEPATH"

# Install Git
RUN apt-get update \
  && apt-get install -y --no-install-recommends git \
  && apt-get purge -y --auto-remove \
  && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt requirements.txt
# COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your project files
# COPY . .

# Expose port (if needed)
# EXPOSE 8000

# Run your application
# CMD ["python", "app.py"]
