# Usar una imagen base de Python
FROM python:3.9-slim
# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requisitos (si tienes uno)
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido de la carpeta src al contenedor
COPY src/ ./src/

# Copia el archivo .env
COPY .env .

ENV STREAMLIT_SERVER_PORT=8501

# Instala Streamlit si no está en requirements.txt
RUN pip install streamlit

# Expone el puerto que usa Streamlit
EXPOSE 8501

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "src/app.py"]