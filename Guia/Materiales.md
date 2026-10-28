# Materiales para la guía fácil

| Cantidad | Material | Especificación |
| --- | --- | --- |
| 1 | ESP32-C3 SuperMini | USB-C, 16 pines, flash 4 MB; no S3 ni ESP32 clásico. |
| 1 | Cable USB-C de datos | Debe permitir programar, no solo cargar. |
| 1 | Protoboard + cables | 400/830 puntos; Dupont M-M y M-H. |
| 1 + 1 | LED rojo + 330 ohm | LED 3 mm; resistencia 1/4 W. |
| 1 | Botón | Pulsador normalmente abierto. |
| 1 | MPU6050 / GY-521 | Módulo compatible con alimentación y pull-ups de 3.3 V. |
| 1 | INMP441 | Micrófono digital I2S; no módulo analógico. |
| 1 | 100 kohm para SD | Resistencia entre SD del micrófono y GND. |
| 2 | 100 nF para sensores | Añadir cerca de VDD-GND si el módulo no los incorpora. |
| 1 juego | Pines de cabecera | Paso 2.54 mm; soldados con la placa desconectada. |
| 1 | Multímetro | Compartido; medir voltaje CC antes de energizar. |
| Disponibles | PC + Android BLE | Arduino IDE 2.x; nRF Connect for Mobile. |

## Solo para la prueba opcional de voltaje

| Cantidad | Material | Uso |
| --- | --- | --- |
| 1 | 150 kohm, 1% | Arriba del divisor. |
| 1 | 100 kohm, 1% | Abajo del divisor; adicional a la resistencia de SD. |
| 1 | 100 nF | Entre GPIO0 y GND. |

Las cinco prácticas funcionan por USB. Las tres AAA, su portapilas protegido y el motor pertenecen a extensiones del manual completo; no son necesarios para terminar esta guía.

| Función | Conexión |
| --- | --- |
| LED | 10 -> 330 ohm -> LED -> GND |
| Botón | 3 -> pulsador -> GND |
| MPU6050 | 3V3 a VCC; GND a GND/AD0; 4 a SDA; 5 a SCL |
| INMP441 | 3V3 a VDD; GND a GND/LR; 6 a SCK; 7 a WS; 1 a SD |
| SD definido | 100 kohm de SD a GND |
| ADC opcional | 0 al nodo 150k/100k; capacitor 100nF a GND |
