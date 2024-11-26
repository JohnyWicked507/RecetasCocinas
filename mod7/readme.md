## 1. Instalar dependencias necesarias

1. Actualiza el sistema e instala Python y pip:

   ```bash
   sudo apt update
   sudo apt install python3 python3-pip -y
   ```

2. Instala Gunicorn y las dependencias de tu proyecto:
   ```bash
   pip install flask gunicorn redis
   ```

## 2. Configurar Gunicorn

Prueba ejecutar tu aplicación con Gunicorn para asegurarte de que funcione correctamente:

```bash
gunicorn -w 3 -b 0.0.0.0:8000 app:app
```

- `-w 3`: Define el número de trabajadores.
- `-b 0.0.0.0:8000`: Escucha en todas las interfaces en el puerto 8000.
- `app:app`: Especifica el archivo `app.py` y la instancia `app` dentro de él.

Si todo está funcionando correctamente, puedes proceder con la configuración de Nginx.

## 3. Instalar y configurar Nginx

1. Instala Nginx:

   ```bash
   sudo apt install nginx -y
   ```

2. Crea un nuevo archivo de configuración para tu aplicación en `/etc/nginx/sites-available`:

   ```bash
   sudo nano /etc/nginx/sites-available/recetas
   ```

   Contenido del archivo:

   ```nginx
   server {
       listen 80;
       server_name your_domain_or_ip;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       error_page 404 /404.html;
       location = /404.html {
           root /var/www/html;
       }
   }
   ```

   Cambia `your_domain_or_ip` por tu dominio o dirección IP pública.

3. Enlaza el archivo de configuración:

   ```bash
   sudo ln -s /etc/nginx/sites-available/recetas /etc/nginx/sites-enabled/
   ```

4. Verifica la configuración de Nginx:

   ```bash
   sudo nginx -t
   ```

5. Reinicia Nginx:
   ```bash
   sudo systemctl restart nginx
   ```

## 4. Crear un servicio de systemd para Gunicorn

1. Crea un archivo de servicio en `/etc/systemd/system/recetas.service`:

   ```bash
   sudo nano /etc/systemd/system/recetas.service
   ```

   Contenido del archivo:

   ```ini
   [Unit]
   Description=Gunicorn instance to serve Recetas App
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/your/app
   ExecStart=/usr/bin/gunicorn -w 3 -b 127.0.0.1:8000 app:app

   [Install]
   WantedBy=multi-user.target
   ```

   Cambia `/path/to/your/app` al directorio donde se encuentra tu archivo `app.py`.

2. Recarga los servicios de systemd:

   ```bash
   sudo systemctl daemon-reload
   ```

3. Inicia y habilita el servicio:
   ```bash
   sudo systemctl start recetas
   sudo systemctl enable recetas
   ```

## 5. Verificar el despliegue

- Accede a tu dominio o dirección IP pública (por ejemplo, [http://localhost](http://localhost) si es local).
- Si todo está correctamente configurado, deberías ver la página de tu aplicación Flask.
