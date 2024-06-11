# Gunakan image dasar Python 3.8
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Salin file requirements.txt ke dalam container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file aplikasi ke dalam container
COPY . .

# Expose port yang digunakan aplikasi
ENV LISTEN_PORT=5000
EXPOSE 5000


# Jalankan aplikasi
CMD ["python", "app.py","--host=0.0.0.0"]
