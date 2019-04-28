# Robot Streaming de Video con Django, CV2 en Rasberry Pi 3
## Descripción 
Este proyecto consiste el diseño y desarrollo en un robot controlado via internet desde una pagina web, el cual tenga la capacidad de moverse en todas las direcciones, subir rampas, pasar tuneles, transmitir video, enviar su ubicación en su entorno según sensores de distancia, tomar y lanzar una pelota. El proyecto incorpora una Rasberry pi 3, PSOC 5 LP, una camara GO PRO y una estructura impresa en 3D. 

#Diseño 

#Transmisión de Video

Se crea un canal de comunicación con un WebSocket 


## Instalación de paquetes necesarios
- pip3 
- django
- channels
- opencv2
- Actualizar Pyrebase `$ pip3 install --upgrade Pyrebase`
* Si se quiere instalar todo de una `$ pip3 install -r requirements.txt`


- Añadir carpeta donde se guarda los paquetes para el servidor de produccion
-- Instalar daphne `$ pip3 install daphne`
-- Ejecutar comando 'daphne'
-- Si no reconoce este comando, modifique el la variable PATH: 
	0. Mirar contenido de PATH `$ echo $PATH` si no esta la carpeta /home/pi/.local/bin que contiene daphne 
	1. Añadir la carpeta `$ export PATH="$HOME/pi/.local/bin:$PATH"`
	2. Cargar PATH `$ source ~/.bashrc`
	3. Verificar `$ echo $PATH`
	4. Forma permanente copiar comando de 1 en :
		- Para abrir con nano: '$ sudo nano ~/.bash_profile'
		- /etc/profile (Para todos los usuarios)
		- ~/.bash_profile (Para un usuario concreto)
		- ~/.bash_login (Para un usuario concreto)
		- ~/.profile (Para un usuario concreto)
	5. Reiniciar.

## Tener en cuenta 
El proyecto de django se llama eventos teclado y la aplicación se llama eventos. Los archivos SignalofLive, PruebaSerial son usados para comprobar la conexión a internet y para probral la comunicación serial con PSoC,Arduino o cualquier microcontrolador. Por otro lado, el archivo rc.txt es la configuración del archivo para ejecutar servidor, el archivo requeriments.txt es para instalar los paquetes de forma automatica.


## Pasos para ejecutar proyecto

0 Clonar el repositorio 
	`$ cd home/pi/Documents/`
	`$ git clone https://github.com/LASER-UD/Streaming-Video-with-Django`

1. Abrir el archivo etc/rc.local
	`$ sudo nano rc.local` o `$ sudo geany rc.local`
2. Copiar el cntendido del archivo rc.txt en rc.local según la preferencia de terminal o sin terminal
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

9. Ejecutar UWSGI: `$ uwsgi --socket :8001 --chdir /home/pi/Documents/Streaming-Video-with-Django/eventos_teclado -w eventos_teclado.wsgi`f
8. Ejecutar Daphne y trabajador: 
	*  Cambiar carpeta `$ cd Documents/Streaming-Video-with-Django/eventos_teclado/`
	* `$ daphne -b 0.0.0.0 -p 9000 eventos_teclado.asgi:application`
	* `$ python3 manage.py runworker v2`
10. Cambiar permisos para correr el proyecto: `$ chwn -R www-data /home/pi/Documents/Streaming-Video-with-Django`
11. Configurar supervisor: `$ uwsgi --ini /etc/uwsgi/eventos_teclado.ini`
	* Correr .ini para verificar el sock 
	* Agregar los .sock
        * correr archivo de configuración`$ sudo supervisord -c /etc/supervisor/conf.d/eventos_teclado.conf`

## Posibles Errores
1. Nginx no arranca 
	* Eliminar Nginx: `$ sudo apt-get remove nginx nginx-common`
	* Eliminar Nginx: `$ sudo apt-get purge nginx nginx-common`
	* Intalar de nuevo : `$ sudo apt-get install nginx` 


- Nota: los archivos de error o de conexión se configuran en la configuracion de nginx 
