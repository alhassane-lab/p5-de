FROM python:3.9-slim

WORKDIR /app

# Copy everything
COPY . .

# Install dependencies via Poetry
RUN pip install poetry && poetry install --no-root

# Run the main script
CMD ["poetry", "run", "python", "-m", "src.main"]
