# Bibliotecas incluidas

Ruta más sencilla: extrae `Instalar_todas.zip` **dentro de la carpeta del sketchbook** que aparece en Archivo > Preferencias de Arduino IDE. Quedará `Arduino/libraries/K9CalmAula/`, junto con las seis bibliotecas de terceros. Reinicia el IDE. No lo extraigas dentro de otra carpeta `libraries` porque se duplicaría ese nivel.

Alternativa: Programa/Sketch > Incluir biblioteca > Añadir biblioteca .ZIP; instala **cada uno de los siete ZIP** de `ZIP/`, primero las dependencias y K9CalmAula al final. Si el IDE ofrece descargar dependencias, las copias de esta carpeta ya fijan las versiones.

Incluidas: K9CalmAula 1.0.0; MPU6050 2.2.9; BusIO 1.17.4; Unified Sensor 1.1.15; GFX 1.13.0; SSD1306 2.5.17; NimBLE-Arduino 2.5.2. GFX/SSD1306 son dependencias declaradas de esta versión de MPU6050; **no se necesita una pantalla**.

ZIP de terceros: copias de los archivos originales descargados por Arduino CLI desde el índice oficial; se conservan código, avisos y licencias. `SHA256.json` permite verificar las copias. No se incluyen ejecutables ni entornos instalados. Arduino IDE y el core ESP32 (con herramientas por sistema operativo) requieren instalación oficial; consulta `Guia/00_Empezar.md`.
