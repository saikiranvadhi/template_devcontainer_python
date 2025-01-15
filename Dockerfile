FROM python:3.12-slim

# Set working directory
WORKDIR /proj_base_path

# Adding path to system environment variable
ENV BASEPATH="/proj_base_path"
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
RUN pip install --no-cache-dir notebook==7.2.2

WORKDIR /proj_base_path

# Make port 8888 available to the world outside the container
EXPOSE 8888

# Run Jupyter Notebook when the container launches
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--IdentityProvider.token=''", "--ServerApp.password=''"]
