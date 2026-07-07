FROM python:3.11-slim

# System deps (sqlite3 already comes with python, but keep pip clean/updated)
RUN pip install --no-cache-dir --upgrade pip

WORKDIR /app

# Install Python dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Hugging Face containers run as a non-root user (UID 1000) and only
# /app (and /tmp) are writable by default, so make sure the db folder
# is writable by that user.
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# HF Spaces routes public traffic to this port (see app_port in README.md)
ENV PORT=7860
EXPOSE 7860

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:7860", "--workers", "2", "--timeout", "120"]
