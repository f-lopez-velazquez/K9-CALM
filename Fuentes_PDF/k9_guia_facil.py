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
LESSONS=[
 dict(title='Luz y botón',goal='Encender una luz, cambiar su velocidad y usar un botón.',
 connections=[['GPIO10','330 ohm -> ánodo LED; cátodo -> GND'],['GPIO3','Botón normalmente abierto -> GND']],
 functions=[['iniciar(1)','Prepara LED, botón y monitor serie.'],['actualizar()','Atiende el botón; conserva el programa en marcha.'],['parpadear(...)','En AUTO, cambia la luz cada cierto tiempo.'],['mostrar()','Escribe modo:1 (AUTO) o modo:0 (MANUAL).']],
 tests=['Sube el programa. Abre Monitor serie a 115200. El LED parpadea.','Pulsa y suelta el botón: aparece modo:0. Es MANUAL.','Envía l (ele minúscula) desde el monitor: la luz cambia.','Pulsa otra vez: regresa a AUTO y vuelve el parpadeo.'],
 changes=[['PARPADEO_MS','500 -> 250','Cambia más rápido; ciclo completo de 0.5 s.'],['PARPADEO_MS','500 -> 1000','Cambia más lento; ciclo completo de 2 s.']],
 trouble='¿No enciende? Revisa la polaridad del LED, la resistencia y GPIO10. ¿Siempre MANUAL? Revisa qué patas del botón están unidas.',
 diagram='13_led_boton',caption='LED con resistencia en serie y botón a tierra. El dibujo representa conexiones, no una fotografía.'),
 dict(title='Medir movimiento',goal='Encender el LED cuando el objeto se mueve lo suficiente.',
 connections=[['Conserva P1','LED y botón quedan en sus pines.'],['GY-521 / MPU6050','VCC -> 3V3; GND y AD0 -> GND; SDA -> 4; SCL -> 5']],
 functions=[['iniciar(2)','Agrega el sensor de movimiento.'],['actividad()','Devuelve cuánto cambia la aceleración; unidad: m/s².'],['> UMBRAL_MOV','Pregunta si la actividad supera el número elegido.'],['encender(seMueve)','En AUTO, prende el LED cuando la respuesta es sí.']],
 tests=['Sube P2 y espera 5 s sobre la mesa. Busca I2C 0x68 y a cerca de 9.81.','Sujeta el sensor al objeto o peluche; muévelo suave, sin golpear.','Observa act: aumenta. El LED enciende si supera 0.70.','Prueba el botón: MANUAL y la letra l siguen funcionando.'],
 changes=[['UMBRAL_MOV','0.70 -> 0.30','Puede encender con movimientos menores.'],['UMBRAL_MOV','0.70 -> 1.20','Requiere una actividad mayor.']],
 trouble='¿No aparece 0x68? Revisa SDA=4, SCL=5 y AD0=GND. IMU:0 indica que no hay lecturas recientes; no significa reposo.',
 diagram='H2_conexiones',caption='Se agregan solo las conexiones del MPU6050. El micrófono todavía no se monta.'),
 dict(title='Detectar un sonido',goal='Encender una alerta al detectar un sonido brusco, conservando el movimiento.',
 connections=[['Conserva P2','No cambies los cables anteriores.'],['INMP441','VDD -> 3V3; GND y L/R -> GND; SCK -> 6; WS -> 7; SD -> 1'],['Resistencia de SD','100 kohm entre SD y GND; desacoplo 100 nF si falta en módulo.']],
 functions=[['ajustarSonido(...)','Fija el mínimo de sonido para la prueba.'],['iniciar(3)','Agrega el micrófono digital al montaje anterior.'],['impulso()','Responde sí durante la detección de un sonido brusco.'],['alertar(ALERTA_MS)','Mantiene la luz por ese tiempo sin detener sensores.']],
 tests=['Sube P3 y espera 3 s con ambiente tranquilo.','Habla suave: rms y pico cambian. No deben quedar en cero siempre.','Reproduce una palmada grabada a volumen moderado; espera 3 s entre intentos.','Mueve el objeto: act sigue cambiando. El botón conserva AUTO/MANUAL.'],
 changes=[['UMBRAL_SONIDO','0.004 -> 0.008','Sube el mínimo: puede detectar menos eventos.'],['UMBRAL_SONIDO','0.004 -> 0.002','Baja el mínimo; el filtro de ruido también influye.'],['ALERTA_MS','1000 -> 1500','La luz de alerta dura 1.5 s.']],
 trouble='¿rms siempre cero? Revisa SD=1 y L/R=GND. ¿pico cerca de 1 siempre? Baja volumen y revisa conexiones. rms no representa dB.',
 diagram='H3_conexiones',caption='SCK y WS son relojes; SD trae el audio digital. I2S ya viene configurado en la biblioteca de aula.'),
 dict(title='Ver datos en el teléfono',goal='Consultar el modo y las alertas por Bluetooth Low Energy (BLE).',
 connections=[['Conserva P3','Todo sigue por USB. No conectes el portapilas.'],['GPIO0 / divisor','Déjalo sin conectar en esta primera prueba; MEDIR_DIVISOR=false.']],
 functions=[['iniciar(4)','Agrega BLE a las funciones anteriores.'],['prepararMedicion(false,...)','Deja apagada la medición de voltaje mientras usas USB normal.'],['enviar()','Publica estado y permite consultarlo desde nRF Connect.'],['mostrar()','También mantiene los datos en el monitor de la computadora.']],
 tests=['Sube P4. Instala y abre nRF Connect for Mobile de Nordic.','Scan -> K9-CALM -> Connect. Expande el servicio 0001.','Lee 0002 como texto; activa su suscripción a notificaciones.','Pulsa el botón: cambia A/M. Lee 0003: debe decir USB; NA.'],
 changes=[['UMBRAL_SONIDO','0.004 -> 0.008','Compara cuántos eventos E1 llegan al teléfono.'],['ALERTA_MS','1000 -> 500','La luz dura medio segundo; BLE sigue actualizando.']],
 trouble='¿No aparece? Revisa permisos Bluetooth/dispositivos cercanos y que otro teléfono no esté conectado. ¿No llegan cambios? Activa la suscripción en 0002.',
 diagram='14_laboratorio',caption='Montaje completo por USB. El divisor de GPIO0 se prueba después, con la guía de medición.'),
 dict(title='El detector completo',goal='Comparar sonido y movimiento antes y después; mostrar una categoría experimental.',
 connections=[['Conserva P4','Mismo montaje, mismos pines y USB como única fuente.'],['Sin motor','Esta guía no conecta motores ni coloca el prototipo en animales.']],
 functions=[['ajustarCambio(...)','Fija la diferencia mínima de actividad para comparar.'],['iniciar(5)','Conserva sensores, botón, LED, BLE y ADC opcional.'],['compararEvento()','Guarda 2 s previos y observa 1.5 s posteriores.'],['evento() == 2','Pregunta si hubo un posible cambio de reacción.'],['enviar() / mostrar()','Presentan E0, E1, E2 o E3 y una puntuación de ensayo.']],
 tests=['Sube P5 y espera 5 s sin mover el objeto.','Sonido moderado sin mover: espera E1 si se detecta impulso.','Repite y mueve el objeto después del sonido: puede aparecer E2.','Pon MANUAL: sigue midiendo y enviando, pero deja de clasificar.'],
 changes=[['CAMBIO_MOV','0.70 -> 0.30','Reduce el mínimo de cambio; la variación previa también cuenta.'],['CAMBIO_MOV','0.70 -> 1.20','Aumenta el mínimo: exige más cambio de actividad.'],['UMBRAL_SONIDO','0.004 -> 0.008','Sube el mínimo acústico; compara sin cambiar volumen.']],
 trouble='¿Siempre E1? Observa act y mueve el objeto después del sonido. ¿E3? Espera 5 s y revisa IMU/MIC. No elimines los controles de calidad.',
 diagram='08_estados',caption='Espera datos, observa después del sonido y deja 2 s de reposo para no contar varias veces el mismo evento.'),
]
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
 for i,(name,data) in enumerate(zip(NAMES,LESSONS),1):
  code=(public/'Codigo'/name/(name+'.ino')).read_text()
  txt=f'# {i:02d} · {data["title"]}\n\n{data["goal"]}\n\n[Inicio](../README.md) · [Configuración](00_Empezar.md) · [Archivo listo para abrir](../Codigo/{name}/{name}.ino)\n\n'
  txt+='## 1. Conecta sin USB\n\n'+markdown_table([['Terminal','Conexión'],*data['connections']])+'\n\n'
  txt+='## 2. Copia todo o abre el archivo\n\nBorra el programa anterior del editor. Usa un solo sketch.\n\n```cpp\n'+code+'```\n\n'
  txt+='## 3. Qué hace cada cosa\n\n'+markdown_table([['Código','Qué hace'],*data['functions']])+'\n\n'
  txt+='## 4. Haz la prueba\n\n'+'\n'.join(f'{j}. {step}' for j,step in enumerate(data['tests'],1))+'\n\n'
  txt+='## 5. Cambia un valor y vuelve a subir\n\n'+markdown_table([['Valor','Cambio','Qué observar'],*data['changes']])+'\n\n**Si falla:** '+data['trouble']+'\n\n'
  txt+=f'![Diagrama de la práctica](../Diagramas/{data["diagram"]}.png)\n\n{data["caption"]}\n'
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
 public=Path(public);root=Path(root);docs(public)
 fp=public/'Fuentes_PDF/fonts'
 for name in ['Body','Bold','Mono']:pdfmetrics.registerFont(TTFont(name,str(fp/(name+'.ttf'))))
 pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
 styles={
  'title':ParagraphStyle('title',fontName='Bold',fontSize=25,leading=30,textColor=colors.HexColor(NAVY),spaceAfter=12),
  'h':ParagraphStyle('h',fontName='Bold',fontSize=12,leading=16,textColor=colors.HexColor(TEAL),spaceBefore=10,spaceAfter=6,keepWithNext=True),
  'p':ParagraphStyle('p',fontName='Body',fontSize=10.2,leading=14.2,spaceAfter=8,textColor=colors.HexColor('#223d50')),
  'small':ParagraphStyle('small',fontName='Body',fontSize=8.2,leading=11,spaceAfter=6,textColor=colors.HexColor('#3a5362')),
  'cell':ParagraphStyle('cell',fontName='Body',fontSize=9,leading=12),
  'code':ParagraphStyle('code',fontName='Mono',fontSize=8.8,leading=11.3,textColor=colors.HexColor(NAVY)),
 }
 story=[];record={}
 def p(t,small=False):story.append(Paragraph(t,styles['small' if small else 'p']))
 def h(t):story.append(Paragraph(t,styles['h']))
 def page(title,kicker='GUÍA FÁCIL / CONECTA · PEGA · PRUEBA'):
  if story:story.append(PageBreak())
  story.append(Paragraph(kicker,styles['h']));story.append(Paragraph(title,styles['title']))
 def table(rows,widths):
  data=[[Paragraph(html.escape(str(v)),styles['cell']) for v in row] for row in rows]
  t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dcebf0')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f3f6f8')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));story.append(t);story.append(Spacer(1,7))
 def image(name,width=512):
  from PIL import Image as PI
  file=public/'Diagramas'/(name+'.png');w,hh=PI.open(file).size
  story.append(Image(str(file),width=width,height=hh*width/w,hAlign='LEFT'))
 def notice(t):
  txt=Paragraph(t,styles['p']);t=Table([[txt]],colWidths=[512]);t.setStyle(TableStyle([('LINEBEFORE',(0,0),(0,-1),3,colors.HexColor(TEAL)),('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#edf4f6')),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),1)]));story.append(t);story.append(Spacer(1,8))
 def steps(items):
  for j,t in enumerate(items,1):p(f'<b>{j}.</b> {t}')

 page('K9 CALM','ZOLVEK / LABORATORIO DE ELECTRÓNICA')
 p('<b>GUÍA FÁCIL PARA PREPARATORIA</b>')
 p('Cinco prácticas para conectar, copiar código, probar y cambiar valores.')
 cover=public/'Ilustraciones/K9_Calm_concepto.png';story.append(Image(str(cover),width=450,height=300,hAlign='CENTER'))
 p('Ilustración conceptual generada con IA sobre un maniquí. No representa un prototipo probado ni sus conexiones eléctricas.',True)
 h('Descarga todo aquí')
 p(f'<link href="{REPO_URL}" color="{TEAL}">{REPO_URL}</link>')
 p('En GitHub: <b>Code > Download ZIP</b>. Extrae la carpeta completa.')
 p('<b>'+AUTHOR+'</b><br/><link href="https://'+WEBSITE+'" color="'+TEAL+'">'+WEBSITE+'</link>')
 notice('Trabaja por USB, sobre mesa o peluche y sin animales. El prototipo detecta coincidencias; no diagnostica ni trata miedo.')

 page('Materiales: compra estas piezas')
 table([['Cant.','Pieza','Qué pedir'],*MATERIALS],[44,155,313])
 h('Solo para la medición opcional de la página 16')
 table([['Cant.','Pieza','Uso'],*DIVIDER],[44,155,313])
 p('No necesitas pilas, motor ni pantalla para completar las cinco prácticas. Las AAA y el montaje portátil se estudian después en el manual completo.',True)

 page('Instala Arduino y selecciona la placa')
 steps(['Instala <b>Arduino IDE 2.x</b> desde arduino.cc/en/software.','Abre <b>Archivo > Preferencias</b>. Agrega la URL oficial de abajo.','En el <b>Gestor de placas</b>, busca <b>esp32 by Espressif Systems</b>. Instala <b>3.3.4</b>. Se necesita internet.','Conecta la placa con un <b>cable USB de datos</b>, sin pilas.'])
 notice('<font size="8.4">https://espressif.github.io/arduino-esp32/package_esp32_index.json</font>')
 table([['Ajuste','Selecciona'],['Placa','ESP32C3 Dev Module'],['USB CDC On Boot','Enabled'],['Flash','4 MB'],['Puerto','El que aparece al conectar la placa'],['Monitor serie','115200 baudios']],[175,337])
 image('11_ide',width=430)
 p('Representación de Arduino IDE 2.x. Los menús pueden variar con el idioma.',True)

 page('Instala las bibliotecas incluidas')
 steps(['Descarga y extrae el ZIP del repositorio.','En <b>Archivo > Preferencias</b>, mira la <b>Ubicación del sketchbook</b>. Usa esa ruta; no la adivines.','Extrae <b>Librerias/Instalar_todas.zip dentro del sketchbook</b>. Se crea la carpeta libraries con siete bibliotecas.','Reinicia Arduino IDE. Abre <b>Programa/Sketch > Incluir biblioteca</b>: debe aparecer <b>K9CalmAula</b>.'])
 h('La ruta debe verse así')
 story.append(Preformatted('Arduino/\n  libraries/\n    K9CalmAula/\n      src/\n        K9CalmAula.h\n    Adafruit_MPU6050.../\n    NimBLE_Arduino.../',styles['code']))
 table([['Incluido','Versión'],['K9CalmAula','1.0.0'],['Adafruit MPU6050 / BusIO','2.2.9 / 1.17.4'],['Adafruit Unified Sensor','1.1.15'],['Adafruit GFX / SSD1306','1.13.0 / 2.5.17; dependencias, sin pantalla'],['NimBLE-Arduino','2.5.2']],[265,247])
 p('<b>Alternativa:</b> Programa/Sketch > Incluir biblioteca > Añadir biblioteca .ZIP. Instala los siete de Librerias/ZIP uno por uno. No importes Instalar_todas.zip con ese menú: ese archivo se extrae en el sketchbook.')
 notice('Las bibliotecas evitan escribir la parte difícil al comenzar. Su código está incluido y explicado en Guia/Biblioteca_por_dentro.md. Arduino IDE y el core ESP32 se instalan aparte desde sus fuentes oficiales.')

 page('Los mismos pines en todo el curso')
 image('01_pinout',width=512)
 table([['Función','Conexión'],*PINS],[100,412])
 notice('Desconecta USB antes de mover cables. Nunca conectes 5 V a un GPIO o a 3V3. No uses GPIO2, 8 o 9: intervienen en el arranque. LED integrado no se usa.')

 for i,(name,data) in enumerate(zip(NAMES,LESSONS),1):
  page(f'{i:02d} / {data["title"]}',f'PRÁCTICA {i} / CONECTA Y COPIA')
  p(data['goal'])
  h('1. Conecta sin USB')
  table([['Terminal','Conexión'],*data['connections']],[112,400])
  h('2. Copia el programa completo')
  p(f'Archivo: <b>Codigo/{name}/{name}.ino</b>. También puedes abrirlo directamente. Verificar > Subir > Monitor serie a 115200.',True)
  lines=(public/'Codigo'/name/(name+'.ino')).read_text().splitlines()
  # Código sin números de línea, seleccionable para copiar y pegar.
  story.append(Preformatted('\n'.join(lines),styles['code']))
  page(f'{i:02d} / Prueba y cambia',f'PRÁCTICA {i} / OBSERVA EL RESULTADO')
  h('3. Haz estas pruebas')
  steps(data['tests'])
  h('4. ¿Qué hace cada cosa?')
  table([['Código','Qué hace'],*data['functions']],[170,342])
  h('5. Cambia un solo valor y vuelve a subir')
  table([['Valor','Prueba','Qué observar'],*data['changes']],[120,105,287])
  notice('<b>Si falla:</b> '+data['trouble'])
  p('<b>Antes de avanzar:</b> el programa sube, obtienes el resultado esperado y sabes explicar qué cambió al modificar el valor.')
  # Esquema compacto en las páginas con suficiente espacio; mapa maestro conserva todas las redes.
  if i==1:image('13_led_boton',width=380)
  elif i==2:image('H2_conexiones',width=300)
  elif i==3:image('H3_conexiones',width=300)
  elif i==4:image('14_laboratorio',width=280)
  elif i==5:image('08_estados',width=260)

 page('Opcional: medir un voltaje seguro')
 p('Haz esta prueba al terminar P4. La placa sigue por USB. <b>No conectes pilas ni otra fuente.</b> Necesitas 150k, 100k, 100 nF y multímetro.')
 image('17_divisor_usb',width=512)
 table([['Desde','Hasta'],['3V3','R1 de 150 kohm'],['Otro extremo de R1','Nodo: GPIO0 + extremo superior R2 + capacitor'],['R2 de 100 kohm','GND'],['Otro extremo del capacitor de 100 nF','GND']],[150,362])
 steps(['Con USB retirado, arma el divisor. Revisa con el profesor.','Conecta USB. Mide el nodo: debe estar cerca de <b>1.32 V</b> si 3V3 mide 3.30 V.','En P4 cambia <b>MEDIR_DIVISOR = true</b>. Compila y sube. Lee V: debe aproximarse a 3.3 V.','Si el multímetro marca 3.30 V y el programa 3.20 V: CALIBRACION = 3.30/3.20 = <b>1.03125</b>. Cambia y repite.'])
 notice('Este valor prueba el ADC, no mide una batería. La alarma puede indicar crítico porque 3.3 V está debajo de los umbrales didácticos de pilas. Al terminar, restaura MEDIR_DIVISOR=false. Para AAA se requiere validar el regulador: consulta H4 del manual completo.')

 page('Bluetooth: lee el estado en Android')
 steps(['Instala <b>nRF Connect for Mobile</b> de <b>Nordic Semiconductor</b>.','Activa Bluetooth y concede permiso de dispositivos cercanos. En Android antiguo puede pedir ubicación para escanear.','Abre <b>Scanner > Scan</b>. Busca <b>K9-CALM</b> y pulsa <b>Connect</b>.','Expande el servicio que comienza en <b>8d6c0001</b>. Lee <b>0002</b> como texto UTF-8 y activa su notificación.','Pulsa el botón físico. Observa el cambio <b>A / M</b>. Lee <b>0003</b>: en USB normal dice <b>USB; NA</b>.'])
 notice('<b>A E2 B0 Q80</b><br/>A: automático. E2: posible cambio de reacción. B0: alimentación normal o USB. Q80: puntuación experimental; no es porcentaje de miedo.')
 table([['Dato','Qué significa'],['A / M','Automático / Manual'],['E0 / E1 / E2 / E3','Sin evento / sonido / posible reacción / faltan datos'],['B0 / B1 / B2 / B3','Normal o USB / bajo / crítico / ADC inválido'],['Q','Puntuación para comparar ensayos, no diagnóstico']],[110,402])
 p('UUID del servicio: <font size="8">8d6c0001-3d68-4b85-9b71-4d3943414c4d</font>. Para estado usa 0002 y para voltaje 0003; conservan el resto de la UUID.',True)
 p('Una notificación BLE actualiza datos dentro de la app; no crea por sí sola una alerta del sistema operativo. No hace falta emparejar desde Ajustes para esta prueba.')

 page('Prueba final: cuatro resultados')
 p('Usa P5. Espera 5 s al encender. Repite cada caso tres veces, dejando 5 s entre ensayos. Mantén volumen y distancia iguales. Sin animales.')
 table([['Caso','Qué haces','Qué esperas'],['1','Sin sonido ni movimiento','E0'],['2','Sonido moderado sin mover el objeto','E1 si detecta el impulso'],['3','Mismo sonido y movimiento posterior durante 1.5 s','E2 si cambia suficiente'],['4','Sonido justo tras arrancar, antes de reunir historia','E3 si logra detectar impulso'],['5','Modo MANUAL, con sonido y movimiento','M y E0; no clasifica']],[42,270,200])
 p('Para intentar E3, reproduce el sonido entre 1.2 y 1.8 s tras reiniciar. Si no se detecta, no concluyas que falló la regla: repite. Nunca sueltes cables con USB conectado.',True)
 table([['Ensayo','Resultado','¿Qué valor cambiaste?'],['Sonido solo 1 / 2 / 3','____ / ____ / ____','_________________'],['Sonido + movimiento 1 / 2 / 3','____ / ____ / ____','_________________']],[210,130,172])
 h('Tres ideas que debes recordar')
 p('<b>setup()</b> prepara una vez. <b>loop()</b> repite. <b>if</b> ejecuta algo solo si se cumple una condición. Los valores <b>const</b> se cambian en el editor y requieren volver a subir.')
 notice('Para aprobar: explica qué mide cada sensor, cambia dos valores con una predicción y muestra los resultados. Una coincidencia de sonido y movimiento no demuestra miedo.')
 p('Verificación de esta entrega: consulta Verificacion/compilacion_aula.json. Las cinco prácticas se compilan con las bibliotecas del paquete. No se han ensayado con hardware físico.',True)

 page('¿La vibración debe ir en el pecho?')
 notice('<b>No hay evidencia suficiente para recomendar pecho, espalda o ambos como sitio para calmar perros.</b> K9 CALM mantiene el motor fuera de las pruebas con animales.')
 table([['Lo que se estudió','Qué permite decir'],['Vibración en chalecos','Algunos perros aprenden señales táctiles; eso no demuestra que se calmen.'],['Presión en chalecos','Es diferente de vibración; evidencia limitada e inconsistente para ansiedad.'],['Raza, peso y pelo','Pueden cambiar el ajuste y la transmisión; no hay dosis terapéutica validada por kg o raza en las fuentes revisadas.'],['Motor de 3 V','3 V es alimentación eléctrica: no mide fuerza sobre piel ni garantiza comodidad.']],[170,342])
 h('Papers para consultar')
 p('Chaleco háptico: estudio de caso, IEEE 2019.<br/><link href="https://doi.org/10.1109/WHC.2019.8816079" color="'+TEAL+'">doi.org/10.1109/WHC.2019.8816079</link>',True)
 p('Comunicación háptica: revisión, Animals 2026.<br/><link href="https://doi.org/10.3390/ani16020323" color="'+TEAL+'">doi.org/10.3390/ani16020323</link>',True)
 p('Presión: revisión sistemática, Animals 2024.<br/><link href="https://doi.org/10.3390/ani14233445" color="'+TEAL+'">doi.org/10.3390/ani14233445</link>',True)
 p('Informe con estudios, límites y respuestas: <link href="'+REPO_URL+'/blob/main/Guia/Evidencia_vibracion_y_bienestar.md" color="'+TEAL+'">Guia/Evidencia_vibracion_y_bienestar.md</link>. Búsqueda dirigida del 27 de octubre de 2026; no es una revisión sistemática nueva.',True)
 p('La caja de la portada es un alojamiento conceptual para electrónica, no una indicación de dónde aplicar vibración. Menos movimiento no prueba calma. El motor opcional se estudia solamente en mesa o peluche.')

 page('Si no sale: revisa esto primero')
 table([['Síntoma','Comprueba','Haz esto'],['PC no detecta placa','Cable y puerto','Usa cable de datos y otro puerto.'],['No sube el código','Placa y puerto','C3 Dev Module; BOOT + RESET; selecciona el nuevo puerto.'],['No encuentra K9CalmAula.h','Ruta del sketchbook','Revisa Arduino/libraries/K9CalmAula/src; reinicia IDE.'],['Falta otra biblioteca','Siete carpetas del paquete','Extrae Instalar_todas.zip en el sketchbook.'],['Serial vacío','Velocidad y USB CDC','115200; CDC Enabled; sube de nuevo y pulsa RESET.'],['LED apagado','Polaridad y GPIO','330 ohm en serie; GPIO10; prueba MANUAL + l.'],['MPU ausente / IMU:0','I2C y 3V3','4 SDA, 5 SCL, AD0 GND. Apaga, corrige y reinicia.'],['Audio siempre cero','L/R y SD','L/R a GND; SD=1; SCK=6; WS=7.'],['No llegan datos BLE','Suscripción','Conecta a K9-CALM y suscríbete a 0002.'],['Se reinicia','Alimentación o corto','Retira pilas; vuelve a USB y revisa montaje.'],['Demasiadas alertas','Ruido o piezas sueltas','Fija sensores; prueba un umbral mayor, un valor por vez.'],['Siempre E3','Historia o lecturas faltantes','Espera 5 s; revisa IMU/MIC y cables sin energía.']],[115,142,255])
 p('Esquemas y programas completos: <link href="'+REPO_URL+'" color="'+TEAL+'">'+REPO_URL+'</link>. El manual completo amplía alimentación AAA, FFT y el código sin biblioteca de aula.',True)
 p('Fuentes: documentación oficial de Arduino/Espressif, bibliotecas de Adafruit y NimBLE, ficha INMP441 y Nordic nRF Connect. Los enlaces y licencias se encuentran en Referencias.md y dentro de los ZIP de bibliotecas.',True)

 out=root/'output/pdf/K9_Calm';out.mkdir(parents=True,exist_ok=True)
 dest=out/'Manual_K9_Calm_Guia_Facil.pdf'
 class Doc(SimpleDocTemplate):
  def afterFlowable(self,f):
   if isinstance(f,Paragraph) and f.style.name=='title':
    title=f.getPlainText();record[title]=self.page
    key='p'+str(self.page);self.canv.bookmarkPage(key);self.canv.addOutlineEntry(title,key,level=0)
 doc=Doc(str(dest),pagesize=(612,792),leftMargin=50,rightMargin=50,topMargin=54,bottomMargin=55,author='Profesor Francisco López Velázquez | zolvek.com.mx',title='K9 CALM - Guía fácil para preparatoria')
 doc.build(story,onFirstPage=lambda c,d:furniture(c,d,'GUÍA FÁCIL / PREPARATORIA'),onLaterPages=lambda c,d:furniture(c,d,'GUÍA FÁCIL / PREPARATORIA'))
 (public/'Fuentes_PDF/paginacion_guia.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
 print(dest)
