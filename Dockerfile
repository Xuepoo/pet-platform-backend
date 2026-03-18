FROM python:3.12-slim

WORKDIR /app

# Copy dependency files
COPY pyproject.toml .

# Install dependencies using pip (which reads pyproject.toml)
RUN pip install --no-cache-dir .

# Copy source code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Expose port
EXPOSE 8000

# Run with production settings (no reload)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
