FROM python:3.11-slim

# Prevents Python from writing .pyc files & enables unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything (but overridden later by volume in docker-compose)
COPY . /app

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit with auto-reload enabled
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.runOnSave=true"]
