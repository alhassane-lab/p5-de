FROM python:3.11-slim

WORKDIR /app

# Copy everything
COPY . .

# Install dependencies via Poetry
RUN pip install poetry && poetry install
# Run the main script
#CMD ["poetry", "run", "python", "-m", "src.main"]