# 00 · Empieza aquí

Hecho por el profesor Francisco López Velázquez. [zolvek.com.mx](https://zolvek.com.mx)

1. Descarga el proyecto: **Code > Download ZIP** en el [repositorio](https://github.com/f-lopez-velazquez/K9-CALM). Extrae todo; no abras los programas dentro del ZIP.
2. Instala **Arduino IDE 2.x** desde [arduino.cc/en/software](https://www.arduino.cc/en/software). No hace falta instalar Python para hacer las prácticas.
3. En Archivo > Preferencias agrega esta URL a “URLs adicionales del Gestor de tarjetas”:

```text
https://espressif.github.io/arduino-esp32/package_esp32_index.json
```

4. Gestor de placas > busca **esp32 by Espressif Systems** > elige **3.3.4** > Instalar. Se necesita internet para este paso: el paquete descarga herramientas distintas para Windows, Linux o macOS.
5. Vuelve a Archivo > Preferencias y mira **Ubicación del sketchbook**. Puede ser Documentos/Arduino o una carpeta en OneDrive. Esa ruta es la que debes usar.
6. Extrae `Librerias/Instalar_todas.zip` **dentro de esa carpeta del sketchbook**. Debe quedar `Arduino/libraries/K9CalmAula/src/K9CalmAula.h`; las otras seis carpetas quedan a su lado. Si ya tenías versiones diferentes, haz copia antes de reemplazarlas. Reinicia Arduino IDE.
7. En Programa/Sketch > Incluir biblioteca debe aparecer **K9CalmAula**, junto con las de Adafruit y NimBLE. Si prefieres importar ZIP desde el IDE, instala los siete de `Librerias/ZIP/` uno por uno.
8. Conecta la placa por USB **sin pilas**. Selecciona **ESP32C3 Dev Module**, flash **4 MB**, **USB CDC On Boot: Enabled** y el puerto que acaba de aparecer.
9. Abre `Codigo/01_Luz_y_boton/01_Luz_y_boton.ino`. Pulsa **Verificar** y después **Subir**. Abre Monitor serie a **115200**.
10. Si no sube: mantén BOOT, pulsa y suelta RESET y luego suelta BOOT. Selecciona el puerto de arranque y vuelve a subir. BOOT no es el pulsador del proyecto.

**Sí está incluido:** código de las cinco prácticas, biblioteca K9CalmAula y seis bibliotecas de terceros con sus licencias, esquemas, manuales y valores para probar. GFX/SSD1306 son dependencias declaradas de MPU6050 2.2.9; no necesitas una pantalla.

**Instalación externa:** Arduino IDE, core ESP32 con sus herramientas y nRF Connect para Android. No se distribuye un instalador universal del IDE ni controladores desconocidos. El USB nativo del C3 normalmente no necesita CH340/CP210x; instala controladores solo si tu placa realmente lleva ese puente.

Fuentes: [instalación oficial de ESP32](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html), [bibliotecas en Arduino IDE](https://docs.arduino.cc/software/ide-v2/tutorials/ide-v2-installing-a-library/).
