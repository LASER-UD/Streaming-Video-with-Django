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
- Si se quiere instalar todo de una `$ pip3 install -r requirements.txt`


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



## Pasos para ejecutar proyecto

0 Clonar el repositorio 
	`$ cd home/pi/Documents/`
	`$ git clone https://github.com/LASER-UD/Streaming-Video-with-Django`

1. Abrir el archivo etc/rc.local
	`$ sudo nano rc.local` o `$ sudo geany rc.local`
2. Copiar el cntendido del archivo rc.txt en rc.local según la preferencia de terminal o sin terminal
3. Entrar a carpeta eventos teclado
	`$ cd home/pi/Documents/Streaming-Video-with-Django/eventos_teclado`
4. Ejecutar 
	`$ python3 manage.py runser 0:8000`
5. Servidor de producción:
	Ejecutar Daphne: `$ daphne -b 0.0.0.0 -p 8001 eventos_teclado.asgi:application &`
	Ejecutar Trabajador: `$ python3 manage.py runworker v2 &`


