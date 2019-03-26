# Robot Streaming de Video con Django, CV2 en Rasberry Pi 3
## Descripción 
Este proyecto consiste el diseño y desarrollo en un robot controlado via internet desde una pagina web, el cual tenga la capacidad de moverse en todas las direcciones, subir rampas, pasar tuneles, transmitir video, enviar su ubicación en su entorno según sensores de distancia, tomar y lanzar una pelota. El proyecto incorpora una Rasberry pi 3, PSOC 5 LP, una camara GO PRO y una estructura impresa en 3D. 

#Diseño 

#Transmisión de Video

Se crea un canal de comunicación con un WebSocket 


## Instalación de paquetes necesarios
- django
- channels
- opencv2


## Pasos para ejecutar proyecto

0 Clonar el repositorio 
	`cd home/pi/Documents/`
	`git clone https://github.com/LASER-UD/Streaming-Video-with-Django`

1 Abrir el archivo etc/rc.local
	`$ sudo nano rc.local`
2 Copiar antes de la linea exit
	`setsid python3 /home/pi/Documents/Streaming-Video-with-Django/SignalofLive.py &`


