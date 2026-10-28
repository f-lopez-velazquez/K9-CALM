"""Guía breve de aula y páginas Markdown, con una única fuente de lecciones."""
from pathlib import Path
import json,html,textwrap,shutil
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Preformatted,Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from k9_identidad import furniture,REPO_URL,AUTHOR,WEBSITE,NAVY,TEAL
from k9_aula_fuentes import NAMES
MATERIALS=[
 ['1','ESP32-C3 SuperMini','USB-C, 16 pines, flash 4 MB; no S3 ni ESP32 clásico.'],
 ['1','Cable USB-C de datos','Debe permitir programar, no solo cargar.'],
 ['1','Protoboard + cables','400/830 puntos; Dupont M-M y M-H.'],
 ['1 + 1','LED rojo + 330 ohm','LED 3 mm; resistencia 1/4 W.'],
 ['1','Botón','Pulsador normalmente abierto.'],
 ['1','MPU6050 / GY-521','Módulo compatible con alimentación y pull-ups de 3.3 V.'],
 ['1','INMP441','Micrófono digital I2S; no módulo analógico.'],
 ['1','100 kohm para SD','Resistencia entre SD del micrófono y GND.'],
 ['2','100 nF para sensores','Añadir cerca de VDD-GND si el módulo no los incorpora.'],
 ['1 juego','Pines de cabecera','Paso 2.54 mm; soldados con la placa desconectada.'],
 ['1','Multímetro','Compartido; medir voltaje CC antes de energizar.'],
 ['Disponibles','PC + Android BLE','Arduino IDE 2.x; nRF Connect for Mobile.'],
]
DIVIDER=[['1','150 kohm, 1%','Arriba del divisor.'],['1','100 kohm, 1%','Abajo del divisor; adicional a la resistencia de SD.'],['1','100 nF','Entre GPIO0 y GND.']]
PINS=[['LED','10 -> 330 ohm -> LED -> GND'],['Botón','3 -> pulsador -> GND'],['MPU6050','3V3 a VCC; GND a GND/AD0; 4 a SDA; 5 a SCL'],['INMP441','3V3 a VDD; GND a GND/LR; 6 a SCK; 7 a WS; 1 a SD'],['SD definido','100 kohm de SD a GND'],['ADC opcional','0 al nodo 150k/100k; capacitor 100nF a GND']]
SETUP='''# 00 · Empieza aquí

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
'''

def markdown_table(rows):
 return '\n'.join(['| '+' | '.join(map(str,row))+' |' for row in [rows[0],['---']*len(rows[0]),*rows[1:]]])

def docs(public):
 g=public/'Guia';g.mkdir(exist_ok=True);(g/'00_Empezar.md').write_text(SETUP)
 from k9_guia_editorial import TOPICS
 for i,(name,data) in enumerate(zip(NAMES,TOPICS),1):
  code=(public/'Codigo'/name/(name+'.ino')).read_text()
  txt=f'# {i:02d} · {data["title"]}\n\n{data["action"]}\n\n[Inicio](../README.md) · [Configuración](00_Empezar.md) · [Archivo listo](../Codigo/{name}/{name}.ino)\n\n'
  txt+='## A · Conecta y comprueba\n\nCon USB retirado: '+data['new']+'\n\n'
  txt+=f'![Circuito](../Diagramas/{data["diagram"]}.png)\n\n'
  txt+=markdown_table([['Desde','Conecta hasta'],*data['wires']])+'\n\n'+data['why']+'\n\n'+data['check']+'\n\n**Comprobación:** '+data['before']+'\n\n'
  txt+='## B · Copia el programa completo\n\nAbre el archivo o borra el editor y pega todo. No lo agregues debajo del código anterior.\n\n```cpp\n'+code+'```\n\n'
  txt+=markdown_table([['Línea o función','Qué hace'],*data['explain']])+'\n\n'
  txt+='### Ejemplo antes de probar\n\n'+markdown_table([['Caso','Cómo se interpreta'],*[list(t) for t in data['trace']]])+'\n\n'
  txt+='## C · Observa, predice y cambia\n\n'
  for j,(title,body) in enumerate(data['test'],1):txt+=f'{j}. **{title}.** {body}\n'
  txt+='\nFragmentos ilustrativos de salida; tus números pueden variar:\n\n```text\n'+'\n'.join(data['output'])+'\n```\n\n'
  txt+='### Cambia '+data['change']+'\n\n'+markdown_table([['Prueba','Qué comparar'],*data['numbers']])+'\n\n'+data['reason']+'\n\n**Si falla:** '+data['failure']+'\n\n'
  txt+='**Registra:** cambié ___; predije ___; observé ___. Avanza cuando puedas repetirlo y explicar por qué cambió la salida.\n'
  (g/(name+'.md')).write_text(txt)
 (g/'Materiales.md').write_text('# Materiales para la guía fácil\n\n'+markdown_table([['Cantidad','Material','Especificación'],*MATERIALS])+'\n\n## Solo para la prueba opcional de voltaje\n\n'+markdown_table([['Cantidad','Material','Uso'],*DIVIDER])+'\n\nLas cinco prácticas funcionan por USB. Las tres AAA, su portapilas protegido y el motor pertenecen a extensiones del manual completo; no son necesarios para terminar esta guía.\n\n'+markdown_table([['Función','Conexión'],*PINS])+'\n')
 (g/'Biblioteca_por_dentro.md').write_text('''# Qué contiene K9CalmAula

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
''')


def build(root,public):
 docs(Path(public))
 from k9_guia_editorial import build as editorial
 editorial(root,public)
