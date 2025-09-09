FROM python:3.10-slim

# dependencias del sistema que necesitan algunas librerías
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 wget -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copiar archivos de la carpeta backend
COPY . .

# instalar paquetes de Python
RUN pip install --no-cache-dir -r requirements.txt

# exponer puerto de Render/Railway
EXPOSE 8000

# arrancar servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]