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
	
	


