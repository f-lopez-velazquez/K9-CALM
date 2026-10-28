# Qué contiene K9CalmAula

La biblioteca evita que tengas que escribir la configuración I2C, I2S, la FFT y el servidor BLE al comenzar. No es un servicio externo: todo su código está en `Biblioteca/K9CalmAula/src/` y funciona en el ESP32.

| Etapa | Se agrega | Se conserva |
|---|---|---|
| 1 | Botón, LED, monitor | - |
| 2 | MPU6050, actividad a 50 lecturas/s | Etapa 1 |
| 3 | Micrófono I2S a 16 kHz, RMS, pico e impulso | Etapas 1-2 |
| 4 | BLE y ADC opcional | Etapas 1-3 |
| 5 | Comparación de actividad y categorías | Etapas 1-4 |

`actualizar()` lee el botón con antirrebote y atiende sensores sin `delay()`. `actividad()` es la desviación filtrada de la magnitud de aceleración respecto de la gravedad. `impulso()` combina un mínimo de RMS, ruido ambiental, ataque y pico/RMS; bajar UMBRAL_SONIDO no garantiza una detección si las demás condiciones no se cumplen.

`compararEvento()` conserva 100 medidas previas (2 s), acumula 1.5 s posteriores y compara: media posterior > media previa + max(CAMBIO_MOV, 3 × desviación previa). Pide datos recientes y suficientes y deja 2 s de reposo. La FFT se usa dentro del motor para una puntuación de ensayo; el alumno no necesita modificarla para completar las prácticas.

E0 = sin evento pendiente; E1 = impulso sin cambio suficiente; E2 = posible cambio de reacción; E3 = faltan datos tras un impulso. “Normal” no certifica bienestar. La puntuación no es porcentaje de miedo.

BLE usa el servicio `8d6c0001-3d68-4b85-9b71-4d3943414c4d`; estado en `0002` con READ/NOTIFY y voltaje en `0003` con READ. Todas comparten el resto de la UUID. Se envía cada 500 ms un texto de menos de 20 bytes. No publica un porcentaje de batería no validado.

`MEDIR_DIVISOR` habilita la medida ADC y sus avisos. Los umbrales internos 4.00/3.80 V son didácticos: no aprueban una alimentación AAA. En la prueba con 3V3 del USB se verá un aviso crítico esperado. `CALIBRACION` multiplica la lectura reconstruida; Ventrada = Vadc × 2.5 × calibración.

IMU:1 y MIC:1 significan lecturas recientes, no calibración física ni audio correcto. Revisar siempre que `rms` cambie y que la magnitud en reposo sea razonable. Sin micrófono operativo puede no haber impulso y el detector permanecer E0; E0 no sustituye comprobar sensores.

Para estudiar sin la biblioteca de aula, abre `Codigo_Referencia/` y el manual completo. No juntes sus sketches con los de `Codigo/`.
