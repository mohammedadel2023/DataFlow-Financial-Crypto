# 1. Use Python 3.11 Slim
FROM python:3.11-slim

# 2. Set environment variables to prevent python from buffering logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy requirements from the ROOT folder and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the 'src' folder into the container
COPY src/ /app/src/

# 6. CRITICAL: Add /app/src to PYTHONPATH 
# This allows main.py to say "from helper import config" without errors
ENV PYTHONPATH="${PYTHONPATH}:/app/src"

# 7. Run the main script
CMD ["python", "src/main.py"]