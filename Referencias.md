# Referencias K9 CALM · edición 3

Hecho por el profesor Francisco López Velázquez. https://zolvek.com.mx

Versiones fijadas: core ESP32 3.3.4, Adafruit MPU6050 2.2.9, BusIO 1.17.4, Unified Sensor 1.1.15 y NimBLE-Arduino 2.5.2. No se presentan como las últimas versiones disponibles.

## R1 · ESP32-C3, Espressif

[R1 · ESP32-C3, Espressif](https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf)

Datos electricos, GPIO, strapping y radio. Complementar con guia de hardware.

## R2 · Arduino-ESP32

[R2 · Arduino-ESP32](https://github.com/espressif/arduino-esp32)

Core 3.3.4; LGPL-2.1. Se usan API GPIO/ADC y driver estandar incluido.

## R3 · Instalacion oficial

[R3 · Instalacion oficial](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html)

Gestor de placas y URL oficial.

## R4 · ADC oficial

[R4 · ADC oficial](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/adc.html)

analogReadMilliVolts, resolucion y rangos por chip.

## R5 · I2S ESP-IDF

[R5 · I2S ESP-IDF](https://docs.espressif.com/projects/esp-idf/en/v5.5/esp32c3/api-reference/peripherals/i2s.html)

Controlador std, ranuras Philips, DMA y lectura con timeout.

## R6 · INMP441, InvenSense

[R6 · INMP441, InvenSense](https://www.invensense.com/wp-content/uploads/2015/02/INMP441.pdf)

Formato de 24 bits, 64 relojes, L/R y pulldown SD 100k.

## R7 · Adafruit MPU6050

[R7 · Adafruit MPU6050](https://github.com/adafruit/Adafruit_MPU6050)

2.2.9; BSD-3-Clause (license.txt). API getEvent, rangos y unidades.

## R8 · Adafruit BusIO

[R8 · Adafruit BusIO](https://github.com/adafruit/Adafruit_BusIO)

1.17.4; MIT. Dependencia de comunicacion.

## R9 · Unified Sensor

[R9 · Unified Sensor](https://github.com/adafruit/Adafruit_Sensor)

1.1.15; Apache-2.0. Estructuras de lecturas.

## R10 · NimBLE-Arduino

[R10 · NimBLE-Arduino](https://github.com/h2zero/NimBLE-Arduino)

2.5.2; Apache-2.0 y avisos de terceros. Servidor/advertising/callbacks.

## R11 · Fritzing

[R11 · Fritzing](https://github.com/fritzing/fritzing-app)

Aplicacion revisada; codigo GPLv3 y otras licencias por componente. No instalada; no se ejecutaron scripts ni se distribuye la aplicacion.

## R12 · Adafruit Fritzing Library

[R12 · Adafruit Fritzing Library](https://github.com/adafruit/Fritzing-Library)

CC BY-SA 3.0 segun LICENSE. Revisada como referencia de representacion; no se copiaron piezas graficas ni imagenes.

## R13 · SuperMini, esquema de distribuidor

[R13 · SuperMini, esquema de distribuidor](https://dl.artronshop.co.th/ESP32-C3%20SuperMini%20datasheet.pdf)

Referencia secundaria para columnas de 16 pines. No identifica de forma universal el regulador ni reemplaza el esquema de la unidad real.

## R14 · MPU6050, guia Adafruit

[R14 · MPU6050, guia Adafruit](https://learn.adafruit.com/mpu6050-6-dof-accelerometer-and-gyro)

Explicacion de aceleracion/giro y uso de biblioteca; no asumir que breakout Adafruit y GY-521 sean electricamente identicos.

## R15 · Nordic nRF Connect

[R15 · Nordic nRF Connect](https://www.nordicsemi.com/Products/Development-tools/nRF-Connect-for-mobile)

App BLE Android; controles pueden cambiar entre versiones.

## R16 · Arduino IDE

[R16 · Arduino IDE](https://www.arduino.cc/en/software)

Descarga del entorno; usar distribucion oficial.

## R17 · Guia hardware C3

[R17 · Guia hardware C3](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/schematic-checklist.html)

Recomendacion de fuente y desacoplo del chip.

## Evidencia sobre vibración y presión

[Informe de papers, ubicación, raza/tamaño y límites](Guia/Evidencia_vibracion_y_bienestar.md). No se encontró respaldo suficiente para prescribir ubicación ni dosis calmante en perros.

## Bibliotecas redistribuidas

Los ZIP originales se incluyen en Librerias/ZIP con código fuente y sus avisos legales. Se distribuyen como recursos explícitos del curso, no como un entorno instalado ni una caché. Adafruit MPU6050: BSD-3-Clause; BusIO: MIT; Unified Sensor: Apache-2.0; GFX/SSD1306: avisos BSD incluidos; NimBLE: Apache-2.0 y avisos de componentes. Los autores originales conservan sus derechos. GFX/SSD1306 se incluyen por las dependencias declaradas del paquete MPU6050; no se necesita pantalla.

## Imágenes y tipografías

La portada es una ilustración conceptual generada y editada con imagegen sobre un maniquí. Se identifica como tal; no es fotografía ni diagrama de cableado. [Prompts y procedencia](Ilustraciones/Prompts_y_procedencia.md). Los esquemas de conexiones son SVG originales deterministas. Las gráficas son sintéticas y la representación del IDE no es una captura real. Noto Sans y DejaVu Sans Mono conservan sus avisos en Fuentes_PDF/Licencias.

## Repositorios de ilustración revisados

Fritzing y Adafruit Fritzing-Library se inspeccionaron en la preparación inicial. No se ejecutaron scripts externos ni se copiaron piezas gráficas. Fritzing: código GPLv3, partes/documentación CC BY-SA 3.0; Adafruit Fritzing Library: CC BY-SA 3.0. Se usaron esquemas por redes para hacer auditables los terminales de la variante de placa seleccionada.
