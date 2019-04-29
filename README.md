
## Pasos para ejecutar proyecto

0 Clonar el repositorio 
	`$ cd home/pi/Documents/`
	`$ git clone https://github.com/LASER-UD/Streaming-Video-with-Django`
1. Instalar archivos:
	* Archivos de Linux `$ sh Requerimientos.sh`
	* Archivos de Python `$ pip install -r requirements.txt`
2. Configurar arranque 
	* Abrir el archivo etc/rc.local`$ sudo nano rc.local` o `$ sudo geany rc.local`
	* Copiar el contendido del archivo rc.txt en rc.local según la preferencia de terminal o sin terminal
3. Entrar a carpeta eventos teclado
	`$ cd home/pi/Documents/Streaming-Video-with-Django/eventos_teclado`
4. Colectar Archivos estaticos en la carpeta eventos_teclado/static
	`$ python3 manage.py colectstatic`
5. Migrar base de datos:
	`$ python3 manage.py migrate`
6. Ejecutar servidor de pruebas 
	`$ python3 manage.py runserver 0:8000`
7. Configurar Nginx
	* Crear archivo de configuración de Nginx: `$ sudo geany /etc/nginx/sites-avaible/eventos_teclado`
	* Copiar contenido de Nginxv1 en el archivo anterior
	* Crear el vinculo con los sitios habilitados: `$ sudo ln -s /etc/nginx/sites-avaible/eventos_teclado /etc/nginx/sites-enabled`
	* Eliminar archivo por defecto `$ sudo rm /etc/nginx/sites-enabled/default`
	* Verificar configuracion de Nginx: `$ nginx -t`
	* Reiniciar servidor: `$ service nginx restart`

9. Ejecutar UWSGI: `$ uwsgi --socket :8001 --chdir /home/pi/Documents/Streaming-Video-with-Django/eventos_teclado -w eventos_teclado.wsgi`
8. Ejecutar Daphne y trabajador: 
	*  Cambiar carpeta `$ cd Documents/Streaming-Video-with-Django/eventos_teclado/`
	* `$ daphne -b 0.0.0.0 -p 9000 eventos_teclado.asgi:application`
	* `$ python3 manage.py runworker v2`
10. Cambiar permisos para correr el proyecto: `$ sudo chown -R www-data /home/pi/Documents/Streaming-Video-with-Django`
11. Copiar uwsgi.txt en /etc/uwsgi/eventos_teclado.ini y ejecutar
	* `$ sudo geany /etc/uwsgi/eventos_teclado.ini`
	* `$ uwsgi --ini /etc/uwsgi/eventos_teclado.ini`
12. Configurar supervisor:
	* Crear carpeta de Notificaciones`$ mkdir /home/pi/Documents/log`
	* Copiar archivo supervisor.txt en `$ mkdir /etc/supervisor/confi.d/eventos_teclado.conf`
        * Correr archivo de configuración `$ sudo supervisord -c /etc/supervisor/conf.d/eventos_teclado.conf`
	* Verificar estado `$ sudo /etc/supervisor/conf.d/supervisorctl status`
	* Reiniciar `$ sudo /etc/supervisor/conf.d/supervisorctl reload`
## Posibles Errores
1. Nginx no arranca 
	* Eliminar Nginx: `$ sudo apt-get remove nginx nginx-common`
	* Eliminar Nginx: `$ sudo apt-get purge nginx nginx-common`
	* Intalar de nuevo : `$ sudo apt-get install nginx` 

- Nota: los archivos de error o de conexión se configuran en la configuracion de nginx 
	* cambiar permisos de camara y puerto `$ sudo chmod 777 /dev/ttyACM0` `$ sudo chmod 777 /dev/video0`
