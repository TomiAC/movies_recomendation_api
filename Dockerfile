FROM python:3.12-slim

# Instala las dependencias de compilación del sistema para librerías como bcrypt
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Ahora pip debería poder compilar bcrypt correctamente
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]