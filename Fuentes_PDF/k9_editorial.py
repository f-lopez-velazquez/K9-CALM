"""Contenido y composicion editorial de K9 CALM; sin conexion a la red."""
from pathlib import Path
import csv, json, html, math, shutil, zipfile, subprocess, textwrap
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle, Preformatted, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT
from k9_texto import accent
from k9_identidad import furniture, REPO_URL, AUTHOR, cover_asset
NAVY='#12334d'; CYAN='#087f99'; GREEN='#237252'; ORANGE='#a64d12'
# Precios: asignaciones de planeacion, no cotizaciones ni precios observados.
BOM=[
('Obligatorio','ESP32-C3 SuperMini',1,'USB-C; 16 terminales; ESP32-C3 con flash 4 MB','Control',100,'ESP32 C3 SuperMini USB C 4MB',1),
('Obligatorio','MPU6050 GY-521',1,'Modulo con regulador y pull-ups a 3.3 V verificables','Movimiento',65,'GY 521 MPU6050 acelerometro giroscopio',2),
('Obligatorio','INMP441',1,'Microfono I2S; VDD 3.3 V; L/R accesible','Sonido',100,'INMP441 I2S microfono digital',3),
('Obligatorio','LED rojo',1,'3 mm; Vf aproximada 1.8-2.2 V','Alerta',3,'LED rojo 3mm difuso',1),
('Obligatorio','Resistencia LED',1,'330 ohm; 1/4 W; 5%','Limitar corriente',1,'resistencia 330 ohms cuarto watt',1),
('Obligatorio','Pulsador',1,'Normalmente abierto; 2 o 4 patas','Modo',5,'pulsador tactil 6x6 normalmente abierto',1),
('Obligatorio','Protoboard',1,'400 o 830 puntos; revisar separacion de placa','Montaje',70,'protoboard 830 puntos',1),
('Obligatorio','Cables Dupont',1,'Juego M-M y M-H; cortos para I2S','Conexiones',65,'cables dupont macho hembra macho macho',1),
('Obligatorio','Cable USB-C',1,'USB datos y alimentacion, no solo carga','Programacion',70,'cable USB A USB C datos',1),
('Obligatorio','Cabeceras',1,'2 tiras 1x8 y tiras para sensores; paso 2.54 mm','Soldadura',12,'pines header macho 2.54 mm',1),
('Obligatorio','Pulldown SD',1,'100 kohm; 1/4 W; 1%','Linea I2S definida',1,'resistencia 100k 1 porciento',3),
('Portatil','Pilas AAA',3,'Alcalinas 1.5 V; mismo lote; no recargables en este diseno','Energia',18,'pilas AAA alcalinas',4),
('Portatil','Portapilas',1,'3 AAA en serie; tapa y cables con polaridad','Proteccion mecanica',35,'portapilas 3 AAA con tapa',4),
('Portatil','Interruptor',1,'SPST; >=0.5 A a 6 V CC; preferir desconexion fisica del pack','Encendido',10,'interruptor mini SPST 6V',4),
('Portatil','PTC F1',1,'Ihold 0.5 A orientativo; validar Itrip, temperatura y curva','Limitar fallas',8,'fusible rearmable PTC 0.5A',4),
('Portatil','Diodo D1',1,'Schottky SS14 o 1N5819; 1 A; respetar banda','Polaridad inversa',4,'diodo 1N5819 Schottky',4),
('Portatil','Resistencia R1',1,'150 kohm; 1%; arriba del divisor','Medir voltaje',1,'resistencia 150k 1 porciento',4),
('Portatil','Resistencia R2',1,'100 kohm; 1%; abajo del divisor','Medir voltaje',1,'resistencia 100k 1 porciento',4),
('Portatil','Capacitor ADC',1,'100 nF ceramico X7R; >=10 V','Estabilizar ADC',2,'capacitor 100nf ceramico',4),
('Portatil','Capacitor entrada',1,'100 uF electrolitico; 10 V; observar polaridad','Reserva transitorios',5,'capacitor 100uF 10V',4),
('Obligatorio','Desacoplos sensores',2,'100 nF X7R en VDD-GND si modulo no los incorpora','Filtrado local',2,'capacitor 100nf X7R',3),
('Portatil','Conector polarizado',1,'2 vias, desmontable; corriente >=0.5 A','Separar USB/pilas',12,'conector polarizado 2 pines cable',4),
('Portatil','Placa perforada',1,'Fibra; pads aislados; tamano segun caja','Montaje final',30,'placa perforada universal fibra',5),
('Portatil','Caja y fijaciones',1,'Aislante; sin bordes; tornillos, separadores, velcro','Montaje sobre maqueta',80,'caja plastica electronica pequena velcro',5),
('Portatil','Consumibles',1,'Cable flexible, termocontractil, soldadura y flux','Aislar y fijar',50,'kit termocontractil cable flexible soldadura',5),
('Compartido','Multimetro',1,'CC voltaje/corriente; fusible en entrada de corriente','Medir',250,'multimetro digital fusible corriente',1),
('Compartido','Fuente de banco',1,'0-6 V; limite de corriente ajustable; verificar salida','Validar regulador',1200,'fuente laboratorio regulable limite corriente',4),
('Compartido','Cautin y soporte',1,'Temperatura regulada; punta fina','Soldar',400,'estacion soldadura regulable',1),
('Compartido','Herramientas y proteccion',1,'Pinzas, pelacables, lentes; extractor de humo disponible','Construir',300,'kit herramientas electronica lentes',1),
('Compartido','Peluche y soporte',1,'Sin animales; base para movimientos controlados','Ensayos',100,'peluche perro',2),
('Disponible','Computadora',1,'USB y Arduino IDE 2.x; acceso a internet para instalar','Programar',0,'equipo disponible no presupuestado',1),
('Disponible','Telefono Android',1,'BLE y nRF Connect; permisos de dispositivos cercanos','Consultar',0,'telefono disponible no presupuestado',4),
('Opcional','Motor y etapa',1,'Motor 3 V + NMOS logic level + diodo + R100 + R100k + C100nF/100uF','Extension en banco',65,'motor vibrador 3V MOSFET logic level',5),
('Opcional','Fuente motor',1,'3.0 V regulados; capacidad superior a corriente de arranque','Motor',90,'fuente regulada 3V motor',5),
('Opcional','Pull-ups I2C',2,'4.7 kohm; solo si faltan o se retiran las de 5 V','I2C',1,'resistencia 4.7k',2),
]
PINS=[['Funcion','ESP32-C3','Destino y condicion'],['LED externo','GPIO10','330 ohm -> anodo; catodo -> GND'],['Boton','GPIO3','Pulsador -> GND; INPUT_PULLUP'],['I2C SDA','GPIO4','GY-521 SDA; pull-up solo a 3V3'],['I2C SCL','GPIO5','GY-521 SCL; pull-up solo a 3V3'],['I2S BCLK','GPIO6','INMP441 SCK'],['I2S WS','GPIO7','INMP441 WS'],['I2S entrada','GPIO1','INMP441 SD; 100k a GND'],['ADC bateria','GPIO0','Nodo R1=150k / R2=100k'],['Sensores','3V3 / GND','VCC o VDD / GND; AD0 y L/R a GND'],['Sin utilizar','2, 8, 9','Strapping; BOOT=9, LED comun=8'],['Reservados','20, 21','UART; 20 solo extension opcional'],['USB nativo','18, 19','D-/D+; no son puntos de conexion del curso']]

def build(root,project):
 global S,P,styles,story,sec,doc
 P=project; S=project/'Fuentes_PDF';S.mkdir(exist_ok=True)
 fp=S/'fonts';fp.mkdir(exist_ok=True)
 for name,query in [('Body','Noto Sans:style=Regular'),('Bold','Noto Sans:style=Bold'),('Mono','DejaVu Sans Mono:style=Book')]:
  path=fp/(name+'.ttf')
  if not path.exists():
   source=subprocess.check_output(['fc-match','-f','%{file}',query],text=True)
   shutil.copyfile(source,path)
  pdfmetrics.registerFont(TTFont(name,str(path)))
 pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
 styles={
 'title':ParagraphStyle('title',fontName='Bold',fontSize=25,leading=31,textColor=colors.HexColor(NAVY),spaceAfter=16),
 'h':ParagraphStyle('h',fontName='Bold',fontSize=13,leading=17,textColor=colors.HexColor(CYAN),spaceBefore=12,spaceAfter=7,keepWithNext=True),
 'p':ParagraphStyle('p',fontName='Body',fontSize=10,leading=14.2,spaceAfter=9,textColor=colors.HexColor('#253c4b')),
 'small':ParagraphStyle('small',fontName='Body',fontSize=8,leading=11,spaceAfter=6),
 'cell':ParagraphStyle('cell',fontName='Body',fontSize=8,leading=10.6),
 'code':ParagraphStyle('code',fontName='Mono',fontSize=8.6,leading=11.5,textColor=colors.HexColor('#133c50'))}
 story=[];sec='INTRODUCCION'
 pagination_file=S/'paginacion.json'
 pagination=json.loads(pagination_file.read_text()) if pagination_file.exists() else {}
 def page(title,section=None):
  nonlocal_dummy=None
  global sec
  if story:story.append(PageBreak())
  if section:sec=section
  story.append(Paragraph(accent(sec),styles['h']));story.append(Paragraph(accent(title),styles['title']))
 def p(t):story.append(Paragraph(accent(t),styles['p']))
 def h(t):story.append(Paragraph(accent(t),styles['h']))
 def note(t,kind='Precaucion'):
  col=GREEN if kind=='Verificacion' else ORANGE if kind=='Precaucion' else CYAN
  a=Paragraph('<b>'+accent(kind)+'.</b> '+accent(t),styles['p'])
  t=Table([[a]],colWidths=[512]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#f0f6f8')),('LINEBEFORE',(0,0),(0,-1),3,colors.HexColor(col)),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),3)]));story.append(t);story.append(Spacer(1,9))
 def table(rows,widths=None):
  a=[[Paragraph(html.escape(accent(v).replace('&gt;','>').replace('&lt;','<')),styles['cell']) for v in row] for row in rows]
  t=Table(a,colWidths=widths or [512/len(rows[0])]*len(rows[0]),repeatRows=1,hAlign='LEFT')
  t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#deedf2')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f4f7f9')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,0),(-1,0),.8,colors.HexColor(CYAN))]));story.append(t);story.append(Spacer(1,9))
 def fig(name,caption,width=512):
  from PIL import Image as PI
  path=P/'Diagramas'/(name+'.png');w,hh=PI.open(path).size
  story.append(Image(str(path),width=width,height=hh*width/w,hAlign='LEFT'))
  story.append(Paragraph(accent(caption),styles['small']));story.append(Spacer(1,5))
 def checklist(items):
  note(' / '.join(items),'Verificacion')
 def code(stage):
  lines=(P/('Codigo_Referencia' if (P/'Codigo_Referencia').exists() else 'Codigo')/f'Practica_{stage:02d}'/f'Practica_{stage:02d}.ino').read_text().splitlines()
  chunks=[lines[i:i+48] for i in range(0,len(lines),48)]
  for idx,ch in enumerate(chunks):
   page(f'Codigo completo {stage:02d} · {idx+1}/{len(chunks)}')
   p(f'<b>Practica_{stage:02d}.ino</b> · Lineas {idx*48+1}-{idx*48+len(ch)}. Copiar los bloques en este orden en un solo archivo; los numeros impresos son solo una guia.')
   # Line numbers outside source, no wrap/cut risk.
   numbered='\n'.join(f'{idx*48+j+1:3}  {line}' for j,line in enumerate(ch))
   story.append(Preformatted(numbered,styles['code']))
 def practice_start(n,title,goal,learn,materials):
  page(f'{n:02d} / {title}','SECCION II / SOFTWARE · CINCO PRACTICAS')
  p('<b>Objetivo.</b> '+goal);h('Lo que aprenderemos');p(learn)
  h('Materiales y punto de partida');p(materials)
  p(f'Conservar H{n-1} y agregar H{n}.' if n>1 else 'Comenzar con la placa desconectada y construir H1.')
  fig('14_laboratorio' if n==5 else '13_led_boton' if n==1 else f'H{n}_conexiones',f'Figura P{n}. Mismas redes que en hardware; cables por terminal, sin escala fisica.')
  table([['Red','Conexion'],*({'1':[['LED','10 -> 330 ohm -> LED -> GND'],['Boton','3 -> pulsador -> GND']],'2':[['Datos / reloj','4 -> SDA; 5 -> SCL'],['Energia / direccion','3V3 -> VCC; GND -> GND y AD0']],'3':[['Relojes / datos','6 -> SCK; 7 -> WS; 1 <- SD'],['Canal / energia','L/R -> GND; VDD -> 3V3; GND comun']],'4':[['Medida','Nodo S1 -> 150k -> GPIO0 -> 100k -> GND'],['Filtro','100nF: GPIO0 a GND; PILAS=false en USB']],'5':[['Conservar','GPIO 10,3,4,5,6,7,1,0 segun H1-H4'],['Energia','Sensores 3V3; USB o pilas validadas']]}[str(n)])],[90,422])
 # outputs CSV and budget
 headers=['Grupo','Componente','Cantidad','Especificacion','Funcion','MXN_unitario_planeacion_no_cotizado','Busqueda_Mercado_Libre','Practica']
 with (P/'Lista_de_Materiales.csv').open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f);w.writerow(headers);w.writerows(BOM)
 base=sum(r[2]*r[5] for r in BOM if r[0]=='Obligatorio');portable=sum(r[2]*r[5] for r in BOM if r[0]=='Portatil');shared=sum(r[2]*r[5] for r in BOM if r[0]=='Compartido');optional=sum(r[2]*r[5] for r in BOM if r[0]=='Opcional')

 page('K9 CALM')
 p('<b>MANUAL COMPLETO / CONSULTA TECNICA</b>')
 p('Pechera inteligente con ESP32-C3, sensores y Bluetooth. Para comenzar con menos teoria, utilizar la Guia Facil del mismo repositorio.')
 asset=cover_asset(P)
 if asset:
  story.append(Image(str(asset),width=450,height=300,hAlign='CENTER'))
  story.append(Paragraph('Ilustración conceptual generada con IA sobre un maniquí; no es fotografía de un prototipo probado ni un esquema eléctrico.',styles['small']))
 else:
  fig('16_concepto_pechera','Ilustración conceptual de la maqueta.')
 h('Descarga los codigos y las bibliotecas')
 p(f'<link href="{REPO_URL}" color="{CYAN}">{REPO_URL}</link>')
 p('<b>Hecho por el profesor Francisco López Velázquez.</b><br/><link href="https://zolvek.com.mx" color="'+CYAN+'">zolvek.com.mx</link>')
 note('Cinco practicas acumulativas. Pruebas en mesa o peluche, sin perros. La deteccion experimental no diagnostica ni trata miedo.','Alcance')
 p('<b>Edicion 2.0 · Identidad editorial Zolvek · Tamaño carta.</b>')

 page('Antes de conectar')
 p('Construiremos un registrador de eventos. Un microfono transforma cambios de presion del aire en muestras digitales. Un sensor inercial mide aceleracion y giro. El ESP32-C3 busca un impulso acustico, compara actividad antes y despues y comunica una categoria experimental.')
 fig('07_sistema','Figura 1. Ambas entradas llegan al microcontrolador. El telefono consulta el resultado por BLE.')
 table([['Ruta corta','Que se obtiene','Pag.'],['Introduccion','Alcance y reglas de laboratorio','1'],['Seccion I · Hardware','Materiales, placa, sensores y etapas H1-H5',str(pagination.get(accent('Comprar con criterio'),'—'))],['Practica 1','Configurar y controlar',str(pagination.get(accent('01 / Configurar y controlar'),'—'))],['Practica 2','Medir el movimiento',str(pagination.get(accent('02 / Medir el movimiento'),'—'))],['Practica 3','Escuchar y analizar',str(pagination.get(accent('03 / Escuchar y analizar'),'—'))],['Practica 4','Bateria y Bluetooth',str(pagination.get(accent('04 / Bateria y Bluetooth'),'—'))],['Practica 5','Integrar el detector',str(pagination.get(accent('05 / Integrar el detector'),'—'))],['Cierre','Pruebas, diagnostico, glosario y referencias',str(pagination.get(accent('Pruebas finales y limites'),'—'))]],[130,344,38])
 p('Al concluir: medir movimiento, caracterizar sonidos, leer voltaje, cambiar modo y consultar eventos en Android. La clasificacion admite actividad normal, evento acustico sospechoso, posible reaccion de sobresalto e informacion insuficiente.')
 note('La compilacion comprueba sintaxis y enlaces. La revision teorica comprueba coherencia electrica. Ninguna sustituye medir la placa real. El registro de verificacion al final distingue estos niveles.','Informacion')

 page('Comprar con criterio','SECCION I / HARDWARE')
 p('La lista completa CSV incluye cantidades, especificacion, funcion, busqueda en Mercado Libre y practica. Las siguientes tablas permiten comprar sin abrir archivos externos. Los importes son <b>reservas de planeacion no cotizadas</b>, no precios actuales verificados; no incluyen envio. Solicitar cotizacion antes de comprar.')
 for group,title in [('Obligatorio','Material de laboratorio por equipo'),('Portatil','Solo para modalidad portatil')]:
  if group=='Portatil': page('Completar la modalidad portatil')
  h(title)
  table([['Componente','N','Especificacion corta','MXN/u'],*[[r[1],r[2],r[3],r[5]] for r in BOM if r[0]==group]],[117,30,315,50])

 fig('15_portapilas','Portapilas e interruptor: las tres celdas internas estan en serie; el dibujo no es un plano para fabricar el portapilas.',width=320)
 page('Herramientas y presupuesto')
 for group,title in [('Compartido','Una estacion compartida'),('Disponible','Equipo existente'),('Opcional','Extensiones separadas')]:
  h(title);table([['Elemento','N','Especificacion','MXN/u'],*[[r[1],r[2],r[3],r[5]] for r in BOM if r[0]==group]],[127,30,305,50])
 table([['Escenario','1 equipo','10 equipos'],['Solo material obligatorio',f'${base}',f'${10*base}'],['Obligatorio + portatil',f'${base+portable}',f'${10*(base+portable)}'],['Con una estacion compartida',f'${base+portable+shared}',f'${10*(base+portable)+shared}'],['Reserva adicional sugerida 15%',f'${round((base+portable+shared)*.15)}',f'${round((10*(base+portable)+shared)*.15)}']],[260,126,126])
 p(f'El material opcional suma ${optional} por equipo y no esta incluido en los totales. Computadora y telefono se consideran existentes. Diez equipos comparten una estacion: planear turnos para soldadura y mediciones; ampliar instrumentos si se requiere trabajo simultaneo.')


 page('Lista de compra trazable')
 p('Busqueda literal sugerida en Mercado Libre y momento de uso. No son enlaces ni existencias verificadas. Funcion y especificacion se encuentran en las tablas previas y en el CSV.')
 table([['Pieza','Busqueda sugerida','P'],*[[r[1],r[6],r[7]] for r in BOM[:18]]],[133,350,29])

 page('Completar la lista de compra')
 table([['Pieza','Busqueda sugerida','P'],*[[r[1],r[6],r[7]] for r in BOM[18:]]],[133,350,29])
 h('Inspeccion de recepcion')
 p('Separar piezas y comprobar valores con el multimetro antes de soldar. El modulo GY-521 debe poder trabajar a 3.3 V sin elevar SDA/SCL a 5 V. El INMP441 debe exponer L/R. Solicitar al vendedor el esquema y referencia del regulador de la SuperMini; la apariencia no basta para identificarlo.')
 note('Si las cabeceras vienen sin soldar, usar cautin con soporte, ventilacion y lentes. Trabajar sin energia. No sujetar una placa conectada con pinzas metalicas.','Precaucion')

 page('La placa que usaremos')
 p('Un microcontrolador es una computadora pequeña: ejecuta instrucciones, lee entradas y controla salidas. El ESP32-C3 utiliza un nucleo RISC-V y ofrece BLE. La placa SuperMini agrega USB-C, regulador y botones para que podamos programarlo. “SuperMini” describe una familia de placas de terceros, no un modelo unico de Espressif.')
 fig('02_caras','Figura 2. Reconstruccion esquematizada de la variante comun de 16 terminales; el reverso refleja las columnas. No es una fotografia ni certifica la unidad comprada.')
 p('Referencia geometrica: USB arriba; columna izquierda 5V, GND, 3V3, 4, 3, 2, 1, 0; derecha 5, 6, 7, 8, 9, 10, 20, 21. Si no coincide, detener el cableado y elaborar la correspondencia con el esquema del proveedor. El LDO no se da por identificado: registrar su marcaje y ficha antes de H4.')
 h('GPIO, USB y limites')
 p('GPIO significa entrada/salida de proposito general. Un pin puede leer un boton o producir un nivel logico, pero no alimentar motores. Los GPIO trabajan a 3.3 V; nunca aplicarles 5 V. El USB nativo utiliza GPIO18/19. Los pines 2, 8 y 9 participan en el arranque: quedan libres en este curso. GPIO4/5 se reasignan a I2C; no se usa JTAG externo.')

 page('Mapa de pines definitivo')
 fig('01_pinout','Figura 3. Pinout de la variante de referencia. El nombre del GPIO en codigo corresponde al numero serigrafiado, no a la posicion fisica.',width=512)
 p('No conectar por posicion de memoria: leer cada etiqueta con la placa orientada como el dibujo. USB nativo usa GPIO18/19 internamente; no confundir los numeros 20 y 21 con USB. La referencia es el esquema de distribuidor R13 y la ficha C3 R1; ambas deben coincidir con la unidad comprada.')
 page('Tabla maestra de conexiones')
 table(PINS,[102,85,325])
 h('Una red, varios terminales')
 p('Una red electrica une puntos al mismo potencial. GND conecta negativos y referencias; 3V3 alimenta sensores. Compartir GND no significa unir 3V3 con 5V. Las lineas de color representan redes diferentes y siempre llevan etiqueta: el color por si solo no define la conexion. Las resistencias y capacitores de H4 no se omiten al pasar al montaje compacto.')
 note('Usamos LED externo en GPIO10 para que el curso no dependa del LED integrado, frecuentemente activo en LOW en GPIO8. Verificar la propia placa antes de usar ese LED.','Informacion')

 page('H1 · Luz y un boton')
 fig('13_led_boton','Figura 4. Dos circuitos sencillos con tierra comun. El boton se mide; el LED se controla.')
 table([['Origen','Trayecto','Destino'],['GPIO10','Resistencia 330 ohm -> anodo LED','Catodo LED -> GND'],['GPIO3','Pulsador normalmente abierto','GND']],[90,285,137])
 h('Por qué funciona')
 p('El LED conduce principalmente en un sentido. La pata larga suele ser anodo y el lado plano indica catodo: confirmar con prueba de diodo. Una resistencia limita la corriente: I=(3.3-2.0)/330=0.00394 A, aproximadamente 4 mA. Sin ella, el LED o el GPIO pueden dañarse. La resistencia puede estar antes o despues del LED porque ambos estan en serie.')
 p('INPUT_PULLUP activa una resistencia interna que mantiene el boton en HIGH cuando está abierto. Al presionarlo, conecta la entrada a GND y se lee LOW. Un pulsador de cuatro patas tiene pares unidos internamente: identificarlos con continuidad, sin energia. Si se conectan dos patas del mismo par, parecera presionado siempre.')
 h('Comprobar antes de programar')
 p('Sin USB, buscar cortos entre 3V3 y GND. En modo voltaje CC y con USB, punta negra en GND: 3V3 debe estar cerca de 3.3 V. Con P1, GPIO3 pasa de cerca de 3.3 V a 0 V al presionar. Un GPIO de LED alternante puede mostrar un promedio en el multimetro.')
 checklist(['LED con resistencia','Boton cambia al presionar','Ningun GPIO recibe 5 V'])

 page('H2 · Entender el movimiento')
 fig('03_sensores','Figura 5. Sensores esquematizados; comprobar ejes y orden de terminales en el modulo real.')
 p('El acelerometro mide aceleracion especifica en tres ejes. En reposo sobre la mesa registra aproximadamente 9.81 m/s² por el apoyo contra la gravedad; en caida libre ideal se acerca a cero. Inclinar la placa reparte la lectura entre ejes. El giroscopio mide velocidad angular: que tan rapido gira, no el angulo absoluto. Adafruit entrega rad/s: 1 rad/s equivale a unos 57.3 grados/s.')
 h('Una medida sencilla de actividad')
 p('<b>A = sqrt(ax² + ay² + az²)</b>, en m/s². Usamos <b>d = |A - 9.80665|</b> y un filtro <b>act = act + 0.15 × (d - act)</b>. Si act era 0 y d=2, el nuevo valor es 0.30 m/s². El filtro suaviza vibraciones y ruido, pero retrasa los cambios. Esta medida no elimina toda la gravedad ni detecta bien un giro suave: tambien se registra el giroscopio.')
 p('La frecuencia de muestreo de movimiento es 50 lecturas/s: una cada 20 ms. La frecuencia de un movimiento es otra cosa: dos oscilaciones por segundo son 2 Hz. Para estudiar regularidad, comparar intervalos entre picos; variaciones de montaje y golpes producen señales parecidas. No inferir conducta solo de la magnitud.')

 page('H2 · Conectar y verificar I2C')
 fig('H2_conexiones','Figura 6. H1 permanece; se añade GY-521. INMP441 todavia no se monta.')
 table([['GY-521','ESP32-C3','Motivo'],['VCC / GND','3V3 / GND','Energia compatible y referencia comun'],['SDA / SCL','4 / 5','Datos y reloj definidos por Wire.begin(4,5)'],['AD0','GND','Direccion I2C 0x68'],['XDA, XCL, INT','Sin conectar','Funciones no utilizadas']],[110,100,302])
 p('I2C es una conversacion sobre dos lineas. SDA transporta datos; SCL marca el ritmo. El ESP32 inicia las consultas y el sensor responde a su direccion, como un numero de casa. Ambas lineas requieren resistencias pull-up: los dispositivos bajan la linea y las resistencias la devuelven a 3.3 V. Muchas GY-521 ya las incluyen. No agregar mas sin revisar el esquema.')
 p('Con USB y sin intercambio, medir SDA y SCL: deben reposar cerca de 3.3 V. Si estan a 5 V, desconectar y corregir pull-ups. Si estan a 0 V, revisar cortos o sensor averiado. El escaner integrado en P2 muestra 0x68. AD0 alto daria 0x69, pero nuestro codigo espera 0x68; no cambiarlo inadvertidamente.')
 note('Medir 3V3 en el modulo y revisar el regulador GY-521: una caida excesiva al alimentarlo con 3.3 V puede impedir que el chip reciba su rango permitido. Verificar su esquema; no puentear un regulador sin identificarlo.','Precaucion')

 page('H3 · El sonido se convierte en numeros')
 p('El INMP441 es un microfono MEMS digital: una membrana responde a cambios de presion y la electronica interna produce muestras. No se conecta al ADC. I2S transmite el flujo con reloj de bits (SCK/BCLK), seleccion de ranura (WS) y datos (SD). Es distinto de I2C: SDA/SCL consultan registros; I2S entrega audio continuo.')
 fig('09_sonidos','Figura 7. Ejemplos sinteticos de envolventes, no registros ni firmas de clasificacion. La escala de cada ejemplo es relativa.')
 p('<b>Amplitud</b>: tamaño de la muestra. <b>Pico</b>: mayor valor absoluto de una ventana. <b>RMS</b>: raiz de la media de los cuadrados, una medida de intensidad sostenida. <b>Duracion</b>: tiempo por encima del umbral. <b>Tono</b>: percepcion ligada a periodicidad; <b>frecuencia</b>: ciclos por segundo. Un aplauso tiene ataque rapido y decaimiento corto; un trueno puede durar mas, pero reverberacion, distancia y grabacion alteran ambos.')
 p('Un portazo, una explosion de pirotecnia y un aplauso pueden generar impulsos de banda ancha. El prototipo solo marca eventos sospechosos. No reconoce con certeza su origen y no mide dB SPL sin calibracion acustica. Los valores normalizados son relativos a escala digital, no a la salud auditiva.')

 page('H3 · Cablear I2S sin ambigüedad')
 fig('H3_conexiones','Figura 8. Todos los sensores simultaneos: I2C y I2S usan pines distintos.')
 table([['INMP441','Destino','Comprobacion'],['VDD / GND','3V3 / GND','Medir 3.3 V; no usar 5 V'],['SCK / WS','GPIO6 / GPIO7','Salida del C3: 1.024 MHz / 16 kHz'],['SD','GPIO1','Entrada de datos; 100k a GND'],['L/R','GND','Selecciona ranura izquierda'],['CHIPEN si expuesto','3V3','Revisar modulo; habilitacion en alto']],[95,130,287])
 p('Muestreamos a 16,000 Hz. Cada trama contiene dos ranuras de 32 bits: 16,000 × 64 = 1,024,000 pulsos de BCLK/s. El microfono entrega 24 bits con signo en la ranura izquierda; el programa desplaza 8 bits y divide entre 8,388,608 para normalizar. La ranura derecha se descarta. No configurar una trama mono de 32 pulsos para este microfono.')
 p('Usar cables cortos y capacitor de 100 nF junto a VDD-GND si falta. El orificio acustico no debe taparse. La hoja de datos recomienda 100k de SD a GND porque la salida queda en alta impedancia fuera de su ranura. Sin reloj, el multimetro no demuestra que I2S funcione: con P3 revisar que RMS no sea permanentemente cero ni cercano a 1; un osciloscopio permite verificar los relojes.')
 checklist(['L/R a tierra','No confundir SD con SDA','Ventanas de audio cambian al hablar suave'])

 page('H4 · Elegir una sola fuente')
 p('<b>Laboratorio:</b> USB de datos para desarrollar H1-H3 y las cinco practicas. El voltaje del portapilas se puede simular con una fuente aislada solo para medir el divisor, sin unir su positivo al pin 5V de la placa. <b>Portatil:</b> tres AAA en serie, sin USB, despues de aprobar el ensayo del regulador. No se usa MT3608 ni litio.')
 fig('04_alimentacion','Figura 9. F1 y D1 reducen riesgos, pero añaden caida. R1 se toma despues del interruptor para no inyectar corriente al ADC apagado.')
 table([['Red','Conexion exacta'],['Positivo protegido','AAA+ -> F1 -> anodo D1; catodo D1 -> S1 -> nodo Ventrada'],['Entrada placa','Ventrada -> pin 5V/VBUS solo si esquema lo autoriza'],['Negativo','AAA- -> GND de placa, sensores, R2 y capacitores'],['Divisor','Ventrada -> R1 150k -> nodo GPIO0 -> R2 100k -> GND'],['Capacitores','100nF: GPIO0-GND; 100uF/10V: Ventrada-GND, + a Ventrada']],[125,387])
 note('Nunca conectar 4.5 V a 3V3. D1 protege polaridad inversa, pero NO aísla el VBUS de USB. Retirar fisicamente el conector del pack antes de conectar USB; apagar S1 no debe ser la unica barrera.','Precaucion')

 page('H4 · Validar el regulador real')
 p('Una pila alcalina nueva puede superar 1.5 V. Medir el conjunto; no asumir 4.5 V exactos. Un regulador lineal necesita una diferencia entre entrada y salida, llamada dropout, que depende de corriente y temperatura. Si la entrada cae demasiado, la salida deja de ser 3.3 V. El LED puede seguir encendido mientras el microcontrolador se reinicia.')
 p('<b>Condicion:</b> Vpack bajo carga - Vdiodo - VPTC - Vcables &gt;= 3.3 V + Vdropout(I,T). Ejemplo solo aritmetico: 4.0 - 0.25 - 0.05 = 3.70 V; quedaria margen de 0.40 V para el LDO. No es una especificacion del regulador comprado.')
 table([['Paso','Medicion / criterio'],['1 · Identificar','Fotografiar marcaje LDO y obtener ficha: entrada maxima, salida, dropout, corriente, capacitores y termica. Si es ilegible o no hay esquema, usar USB y no aprobar AAA.'],['2 · Continuidad','Sin fuentes: confirmar que 5V llega a entrada LDO; comprobar conexion a USB VBUS y ausencia de ORing. Confirmar polaridad y sin corto.'],['3 · Fuente limitada','Sin USB y sin pilas: alimentar entrada protegida con fuente ajustable. Limitar inicialmente a 100 mA para detectar cortos; aumentar solo con revision de consumo y capacidad de LDO/cables, hasta permitir arranque.'],['4 · Barrido','Desde voltaje real del pack nuevo, reducir en pasos de 0.1 V con BLE conectado y ambos sensores. Medir entrada y 3V3 en reposo y eventos; registrar reinicios. Detener si cae de 3.20 V o excede ficha/temperatura.'],['5 · Umbrales','Tomar la menor entrada estable, añadir margen &gt;=0.2 V y definir critica; baja &gt;=critica+0.2 V. Sustituir constantes del codigo. Si requiere umbrales mayores que el pack disponible, rechazar la modalidad.'],['6 · Pilas','Retirar fuente; conectar AAA protegidas sin USB. Repetir pruebas. Una advertencia de software no desconecta la energia: apagar al aviso critico.']],[100,412])
 p('Presupuestar picos de corriente, no solo el promedio. Para diseñar la fuente del ESP32-C3, Espressif recomienda capacidad de al menos 500 mA; verificar tambien la corriente disponible del LDO y sensores. No se promete autonomia: medir mA promedio y caidas con carga. Medir corriente EN SERIE, nunca poner el amperimetro entre + y GND.')

 page('H4 · Divisor, ADC e histeresis')
 p('El ADC convierte voltaje en un numero. A 12 bits hay 4096 niveles, pero el resultado no equivale a una medicion ideal. Usamos analogReadMilliVolts(), calibracion del chip y una comparacion adicional con multimetro. En C3, la atenuacion mayor permite medir aproximadamente hasta 2.5 V; no suponer que todo el rango de 3.3 V es medible.')
 p('<b>Vadc = Ventrada × R2/(R1+R2).</b> Con 150k y 100k, la fraccion es 0.4; 4.50 V produce 1.80 V. Para reconstruir: <b>Ventrada = Vadc × 2.50 × CAL</b>. Se mide despues de D1, por lo que no representa exactamente la tension en bornes de las pilas. La corriente permanente del divisor a 4.5 V es 4.5/250000 = 18 microamperios.')
 table([['Par arriba/abajo','4.5 V entrada','5.25 V entrada','Factor'],['120k / 100k (ejemplo)','2.045 V','2.386 V','2.20'],['150k / 100k (definitivo)','1.800 V','2.100 V','2.50']],[180,110,110,112])
 p('120k/100k puede servir tras comprobar tension maxima y tolerancias; deja menos margen. Elegimos 150k/100k al 1%. Peor caso a 5.25 V, R1 baja 1% y R2 sube 1%: 5.25 × 101/(148.5+101)=2.125 V. El maximo de alimentacion permitido por la placa se valida aparte: este calculo no autoriza alimentarla a 5.25 V.')
 p('La resistencia equivalente del divisor es 60k. Con 100nF, τ=RC=0.006 s; esperar al menos 30 ms tras energizar y promediar. El programa espera 1 s y promedia 16 lecturas. El capacitor suministra los pequeños pulsos del muestreo y reduce ruido. Confirmar estabilidad con multimetro y varios voltajes.')
 p('<b>Calibracion:</b> si el multimetro indica 4.20 V y el programa 4.10 V, CAL=4.20/4.10=1.0244. Repetir en al menos tres puntos; una constante no corrige toda no linealidad. Si el error supera 0.10 V tras calibrar, investigar antes de usar alarmas.')
 p('<b>Histeresis:</b> entrar a baja por debajo de 4.00 V y salir solo sobre 4.15 V evita parpadeos por ruido. 3.80 V critico y 4.00 V baja son ejemplos didacticos, desactivados por PILAS=false. El porcentaje de carga no se calcula: voltaje, carga, temperatura y edad no dan una relacion universal.')

 page('H5 · Del cableado a la maqueta')
 fig('14_laboratorio','Figura 10. Circuito completo de laboratorio: USB como unica alimentacion; divisor solo si se ensaya H4 con entrada aislada.')
 table([['Conexion integrada','Terminales'],['Alerta / control','10 -> 330 ohm -> LED -> GND; 3 -> boton -> GND'],['MPU6050','4 SDA, 5 SCL, 3V3 VCC, GND GND/AD0'],['INMP441','6 SCK, 7 WS, 1 SD +100k a GND; 3V3 VDD, GND GND/LR'],['Medida opcional H4','0 al divisor 150k/100k; 100nF nodo-GND'],['Energia','USB; pack retirado. AAA solo con autorizacion tecnica de H4']],[130,382])
 p('Probar primero en protoboard. Si la SuperMini tapa los agujeros vecinos, usar dos protoboards o extensiones; no doblar patas para forzarla. Pasar a placa perforada solo despues de comprobar cada red por continuidad. Mantener cables I2S cortos, GND firme y sensores separados de cables del motor. El MPU debe quedar sujeto para que mida el objeto y no un modulo colgando.')
 p('Usar caja aislante, alivio de tension y conectores polarizados. Dejar la antena libre de metal y las AAA separadas de puntos calientes. No sellar con pegamento el microfono. La propuesta de pechera solo se monta en una maqueta o peluche: peso, temperatura, humedad, bordes, desprendimientos y bienestar animal requieren validacion independiente.')

 page('Extension opcional: vibracion')
 fig('05_motor','Figura 11. Etapa conceptual low-side con diodo de rueda libre. No está conectada ni habilitada en los cinco programas.')
 table([['Elemento','Conexion / seleccion'],['Motor','+ a fuente 3.0 V regulada; - a drain NMOS'],['NMOS','Source a GND; gate por 100 ohm a GPIO20; 100k gate-GND'],['Diodo','Catodo/banda a +3 V; anodo a drain; corriente y pulso compatibles con motor'],['Fuente','3.0 V regulados externos; GND comun con C3; capacidad mayor al arranque'],['Filtrado','100nF y 100uF junto al motor/fuente; electrolitico con polaridad']],[100,412])
 p('El GPIO solo manda la compuerta; la corriente del motor circula por transistor y fuente. Elegir NMOS cuya resistencia RDS(on) este especificada a 2.5 o 3.3 V, no solo por su voltaje de umbral. Comprobar patillaje en su hoja de datos. Al apagar una bobina aparece un pico inverso; el diodo le ofrece un camino y protege el transistor. Un diodo al reves cortocircuita la fuente al encender.')
 p('No alimentar el motor desde GPIO, 3V3 de la placa ni directamente con tres AAA: podria recibir mas de 3 V y provocar reinicios. Probar por separado con fuente limitada, medir corriente de arranque y temperatura. Solo entonces integrar una temporizacion corta sin delay(). Prueba exclusivamente en banco o peluche; no implica que vibrar calme a un animal.')

 page('Vibracion: qué respalda la ciencia')
 note('No se identifico evidencia clinica suficiente para recomendar vibracion en pecho, espalda o ambos para calmar perros. No se asigna una dosis por raza o kg ni se activa un motor sobre animales.','Alcance')
 table([['Fuente','Resultado util / limite'],['IEEE WHC 2019 · DOI 10.1109/WHC.2019.8816079','Un perro aprendio ordenes con cuatro motores. Comunicacion aprendida no equivale a reduccion de miedo.'],['Animals 2026 · DOI 10.3390/ani16020323','Revision de comunicacion haptica: diferencias en protocolos y necesidad de medir percepcion y bienestar. No establece sitio calmante.'],['Pekkin 2016 · DOI 10.1016/j.applanim.2016.09.003','28 perros reclutados; chalecos de presion, no motores. Sin efecto terapeutico claro en el ensayo.'],['Animals 2024 · DOI 10.3390/ani14233445','Revision sistematica de cuatro estudios de presion: evidencia debil y limitada, con sesgos e inconsistencia.']],[190,322])
 h('Implicacion para el diseño')
 p('Se conserva LED/BLE como salida del detector. El motor es una extension de banco, no un tratamiento. El dibujo de la caja dorsal muestra alojamiento de electronica, no una ubicacion terapeutica. No se cambia al pecho sin evidencia y validacion profesional.')
 p('Inferencia de ingenieria: pelo, ajuste, masa y montaje pueden cambiar la vibracion transmitida. Tres voltios describen alimentacion electrica, no aceleracion en piel. PWM en un motor ERM no fija de forma independiente frecuencia mecanica e intensidad. La vibracion tambien puede contaminar MPU6050 y microfono.')
 p('No se identifico una pauta validada por raza, tamaño, intensidad, Hz o duracion para el objetivo de calmar. Tampoco se extrapolan ensayos humanos de chalecos vibratorios. Menor actividad no demuestra calma: se requieren medidas de bienestar y evaluacion veterinaria/etologica.')
 p('Informe y enlaces: <link href="'+REPO_URL+'/blob/main/Guia/Evidencia_vibracion_y_bienestar.md" color="'+CYAN+'">Guia/Evidencia_vibracion_y_bienestar.md</link>. Busqueda dirigida; no es una revision sistematica nueva.')

 practice_start(1,'Configurar y controlar','Instalar el entorno, subir un programa y cambiar entre automatico y manual.','Compilar frente a subir, puerto USB, niveles digitales, antirrebote y temporizacion con millis().','ESP32-C3, cable de datos, LED, 330 ohm, boton y multimetro. No conectar sensores aun.')
 page('P1 · Preparar Arduino IDE')
 p('1. Descargar Arduino IDE 2.x desde arduino.cc/en/software e instalar la version de su sistema. Abrir Archivo > Preferencias (o Settings). En “URLs adicionales del Gestor de tarjetas” agregar la direccion oficial siguiente, sin espacios ni saltos:')
 p('<font size="8">https://espressif.github.io/arduino-esp32/package_esp32_index.json</font>')
 p('2. Abrir Gestor de placas, buscar “esp32 by Espressif Systems” e instalar <b>3.3.4</b>, la version fijada para este manual. No confundir con un paquete de otro fabricante. La version mas nueva puede cambiar APIs; si se actualiza, repetir compilaciones y validacion de I2S y BLE.')
 p('3. Conectar por USB sin pilas. Seleccionar <b>ESP32C3 Dev Module</b> y el puerto que aparece al conectar. En Herramientas elegir <b>USB CDC On Boot: Enabled</b>, flash 4 MB y velocidad de subida 115200 si hay problemas. En placas con USB nativo el puerto puede reaparecer con otro nombre despues de subir.')
 fig('11_ide','Figura 12. Representacion de controles y campos de IDE 2.x; los textos y posiciones pueden variar con idioma/version. No se presenta como captura real.')
 p('4. No instalar controladores al azar. El USB nativo usa CDC/JTAG del C3; una placa con puente CH340/CP210x requiere identificar ese chip y el controlador de su fabricante. En Linux comprobar permisos del puerto con el administrador del laboratorio. Probar primero otro cable de datos y otro puerto USB.')

 page('P1 · Crear, compilar y observar')
 p('5. Archivo > Abrir: seleccionar Codigo/Practica_01/Practica_01.ino. Arduino exige que el archivo principal tenga el mismo nombre que la carpeta. Alternativamente crear un sketch nuevo, guardar como Practica_01 y copiar todo el codigo de las paginas siguientes.')
 p('6. Pulsar Verificar (check). Compilar traduce C++ y enlaza bibliotecas; puede hacerse sin placa. Leer el primer error real, no solo “exit status 1”. Pulsar Subir (flecha): ademas transmite el binario. El progreso termina con reinicio o confirmacion de subida. No desconectar durante escritura.')
 p('7. Abrir Monitor serie a 115200. Presionar RESET una vez si no se ve el mensaje inicial. Si no se conecta el cargador, mantener BOOT, pulsar RESET, soltar RESET y luego BOOT, seleccionar el puerto de arranque y volver a subir. BOOT no es el boton de control del proyecto.')
 h('Cómo leer este programa')
 p('<b>setup()</b> corre una vez y configura Serial y pines. <b>loop()</b> se repite. <b>ahora=millis()</b> mide tiempo transcurrido desde encendido. La resta sin signo ahora-cambio resiste el desbordamiento del contador; no es la hora del reloj. El LED automatico cambia cada 500 ms: el ciclo completo dura 1 s.')
 p('<b>controles()</b> distingue lectura cruda de estado estable: cuando cambia, inicia una espera de 30 ms sin detener loop(). Si el nuevo nivel persiste, acepta una pulsacion. Se conmuta el modo solo al pasar a LOW, por lo que mantener presionado no lo alterna repetidamente. En manual, enviar la letra <b>l</b> cambia la luz; el salto de linea posterior se ignora.')
 h('Prueba guiada y resultado')
 p('Encender: LED parpadea y aparece modo:1 cada 250 ms. Presionar y soltar: aparece MANUAL y modo:0. Escribir l y enviar: el LED cambia de estado. Volver a pulsar: AUTO y parpadeo. Si el LED no responde, revisar polaridad y GPIO10; si el modo oscila, revisar boton y conexiones antes de aumentar el antirrebote.')
 h('Analizar y avanzar')
 p('Cronometrar diez ciclos del LED y calcular su periodo promedio. Cambiar 500 por 250: predecir primero el periodo completo. Volver al valor original para conservar la referencia de las siguientes practicas.')
 checklist(['Compila y sube','Serial legible','Una pulsacion cambia una vez','Modo manual controla LED'])
 code(1)

 practice_start(2,'Medir el movimiento','Agregar el MPU6050 y mantener boton, modos, LED y mensajes.','Direccion I2C, lecturas con unidades, norma vectorial, filtrado y muestreo periodico.','H1 mas GY-521; objeto rigido o peluche como soporte. Alimentacion USB.')
 page('P2 · Instalar y comprender')
 p('En el Gestor de bibliotecas buscar <b>Adafruit MPU6050 2.2.9</b> e instalar con todas sus dependencias. Verificar <b>Adafruit BusIO 1.17.4</b> y <b>Adafruit Unified Sensor 1.1.15</b>. BusIO gestiona intercambios I2C; Unified Sensor define estructuras con unidades. Wire.h ya viene con el core ESP32: no descargar una copia externa.')
 p('Abrir Practica_02.ino, verificar placa y puerto, compilar y subir. El programa es autonomo y contiene las funciones de P1; no juntar archivos .ino de distintas practicas porque se duplicarian setup() y loop(). Al arrancar, el escaner consulta direcciones del bus y muestra las que reconocen el intercambio. Despues mpu.begin(0x68,&Wire) verifica el sensor.')
 p('Se configuran rangos de ±8 g y ±500 grados/s para disponer de margen. La biblioteca convierte a m/s² y rad/s. Un rango mayor evita saturacion, pero reduce detalle. El filtro interno de 21 Hz ayuda antes de leer a 50 Hz; no equivale a un filtro perfecto contra todas las frecuencias altas.')
 h('Datos y funciones nuevas')
 table([['Modulo / variable','Interpretacion y comprobacion'],['iniciarIMU()','Define 4/5, limita espera I2C y escanea. Falla sin bloquear todo el programa.'],['movimiento()','Cada 20 ms obtiene a,g,t; si getEvent falla, no actualiza historial.'],['magnitud','Norma de aceleracion: cerca de 9.81 en reposo.'],['giro','Norma de velocidad angular: cerca de cero quieto, aumenta al rotar.'],['actividad','Desviacion de la norma respecto a gravedad, suavizada. LED AUTO si >0.7.'],['historial / ultimoIMU','Conservan 100 lecturas para P5 y tiempo de ultima lectura valida.']],[140,372])
 note('Sin IMU el programa continua con boton y mensajes; no interpretar act=0 como reposo valido. Revisar “MPU AUSENTE” y volver a encender una vez reparado el cableado.','Precaucion')

 page('P2 · Medir, comparar y registrar')
 fig('10_movimiento','Figura 13. Actividad simulada antes y despues de un evento; no es una medicion de un perro.',width=360)
 p('1. Dejar el modulo fijo y quieto 5 s. Registrar a, giro y act. 2. Inclinar lentamente 90 grados sin golpear: los componentes cambian, la norma debe seguir cerca de 9.81. 3. Mover el objeto adelante y atras unas dos veces por segundo; observar picos. 4. Girarlo suavemente sin trasladarlo; comparar actividad y giro. No lanzar ni golpear sensores.')
 table([['Ensayo','Esperado','Registrar'],['Mesa fija','a ~ 9.81; giro pequeño; act baja','Promedio y variacion'],['Inclinacion lenta','Norma casi constante','Por qué un eje solo confunde'],['Sacudida moderada','Actividad sube; LED en AUTO','Valor maximo y tiempo'],['Giro suave','Giro sube aun con act baja','Limitacion de la magnitud']],[110,235,167])
 p('Abrir Herramientas > Serial Plotter a 115200 para comparar las etiquetas numericas. No abrir Monitor y Plotter simultaneamente si el puerto queda ocupado. La consola se imprime a 4 Hz para mantener legibilidad, pero el sensor se consulta a 50 Hz: la grafica serie no conserva todos los picos. Para analizar frecuencia usar registros mas rapidos y quitar texto extra, sin cambiar el periodo de muestreo.')
 h('Si algo falla')
 p('Sin 0x68: verificar GND, SDA/SCL intercambiados y AD0. 0x69 significa otra seleccion de direccion; volver AD0 a GND. Datos constantes: comprobar que el modulo realmente se mueve. Valores extremos fijos sugieren saturacion, alimentacion incorrecta o datos invalidos. Un cable suelto puede parecer un movimiento brusco.')
 h('Actividad de analisis')
 p('Hacer cinco oscilaciones lentas y cinco rapidas. Estimar frecuencia como ciclos/segundos. Explicar por que un detector de “act alta” no distingue sobresalto de juego ni reconoce todo giro.')
 story.append(Paragraph(accent('<b>Para avanzar:</b> 0x68 reconocido / unidades correctas / 50 Hz configurados / boton y modo manual conservados.'),styles['small']))
 code(2)

 practice_start(3,'Escuchar y analizar','Añadir audio I2S y conservar el MPU6050 y controles.','Muestras con signo, ventanas, RMS, pico, ataque, decaimiento y espectro.','H2 mas INMP441, 100k de SD a GND y desacoplo local. USB y sonido moderado.')
 page('P3 · Una ventana de audio')
 p('driver/i2s_std.h viene con Arduino-ESP32 3.3.4; no instalar una biblioteca I2S adicional. Abrir P3 y verificar. Esta version usa el controlador estandar de ESP-IDF, no la API heredada driver/i2s.h. No mezclarlas. El codigo fija ranuras estereo de 32 bits, aunque solo procesa el canal izquierdo.')
 p('DMA guarda muestras mientras la CPU atiende otros modulos. escuchar() pide hasta 64 pares; timeout 0 regresa sin esperar datos nuevos. Va acumulando 256 muestras izquierdas: 256/16000 = <b>16 ms</b> por ventana. Si loop se demora demasiado, DMA puede perder datos: no añadir impresiones por muestra ni tareas largas.')
 h('RMS paso a paso')
 p('Se calcula la media para quitar el componente continuo; despues <b>RMS=sqrt((x1²+...+xN²)/N)</b>. Para [0.1,-0.1,0.1,-0.1], la media es 0 y el RMS 0.1. El pico es 0.1. Un pico aislado puede tener pico alto y RMS pequeño; la relacion pico/RMS ayuda a reconocer impulsos. El silencio digital absoluto no permite dividir: se usa un minimo 0.000001.')
 p('<b>Ataque=max(0,RMSactual-RMSanterior)</b> y <b>decaimiento=max(0,RMSanterior-RMSactual)</b> son cambios entre ventanas, no pendientes en unidades por segundo. La duracion avanza mientras la señal permanece sobre el umbral; al caer, conserva el ultimo valor. Es aproximada a 16 ms y puede separar colas intermitentes.')
 h('Detector funcional antes del espectro')
 p('El ruido se estima lentamente en ventanas no fuertes. Un sonido fuerte exige RMS>max(0.004,6×ruido). Un impulso ademas exige pico/RMS>2, ataque>2×ruido y mas de 2 s desde el ultimo. El primer segundo calienta el estimador. Primero observar RMS/pico y probar el LED; la FFT solo añade una descripcion, no es necesaria para encenderlo.')
 note('Estos umbrales se ajustan con datos de banco. No reproducir pirotecnia real ni hacer sonidos intensos cerca de personas o animales. Una grabacion moderada puede no superar el umbral: ajustar con criterio, no aumentar volumen indefinidamente.','Precaucion')

 page('P3 · FFT sin magia')
 fig('12_fft','Figura 14. Espectro sintetico: las barras representan energia relativa, no una clasificacion del origen.')
 p('La FFT reorganiza las muestras para estimar cuanto contenido hay en diferentes frecuencias. Una analogia es separar los ingredientes de una mezcla. Nuestro algoritmo radix-2 necesita N potencia de dos. Con N=256 y Fs=16000, la separacion entre bins es <b>62.5 Hz</b>; el bin 32 corresponde a 2000 Hz. Solo usamos frecuencias positivas por debajo de 8000 Hz, limite de Nyquist.')
 p('La ventana Hann reduce fugas al cortar una señal continua en bloques: multiplica cada muestra por 0.5-0.5 cos(2πi/(N-1)). Se ponen a cero las partes imaginarias, se reordenan indices y se combinan pares en etapas. La energia relativa de un bin es re²+im². Se suman bins 2-127 y se divide la energia desde 2 kHz entre ese total: <b>agudos</b> va de 0 a 1. No se interpreta como porcentaje de “miedo”.')
 h('Cómo incorporarlo de forma guiada')
 p('1. Compilar P3 completo y confirmar que RMS y pico reaccionan. 2. Localizar espectro(): se llama despues de guardar RMS y ataque porque modifica re[]. 3. Observar ag en Serial con voz grave y un sonido agudo suave. 4. Para aislar una falla, comentar solo espectro(); RMS e impulsos deben seguir funcionando y ag queda en cero. Restaurar la llamada antes de pasar a P4.')
 p('La FFT describe solo una ventana de 16 ms y no el evento completo. Un sonido grave puede tener ataque con energia alta; el montaje y la distancia cambian la señal. El detector conserva el movimiento y permite comparar coincidencias temporales, pero no reconoce petardos de manera validada.')

 page('P3 · Ensayo acustico y lectura del codigo')
 table([['Funcion','Que hace / comprobar'],['iniciarAudio()','Crea canal RX, configura reloj y GPIO 6/7/1 y activa DMA. audioOK confirma inicializacion, no sonido correcto.'],['escuchar()','Recibe pares, descarta ranura derecha, normaliza y llena re[].'],['analizarAudio()','Quita media, calcula RMS/pico/ataque/decaimiento y compara con umbral.'],['espectro()','Hann + FFT in situ + proporcion de energia &gt;=2kHz.'],['impulso / ultimoAudio','Pulso de una vuelta de loop y marca temporal de ultima ventana procesada.']],[132,380])
 p('Tras subir, esperar 3 s en silencio relativo. Hablar suave y comprobar que rms y pico varian sin saturar. Reproducir una palmada grabada a volumen moderado, esperar 3 s y repetir. Comparar con un portazo, pirotecnia y trueno grabados, sin producir los sonidos originales. Registrar distancia y volumen para repetir condiciones. Mover luego el objeto suavemente y observar act en el mismo registro.')
 table([['Muestra','RMS / pico','ag / dur','¿Impulso? / movimiento'],['Voz / ambiente','________','________','________'],['Aplauso grabado','________','________','________'],['Portazo grabado','________','________','________'],['Pirotecnia / trueno grabados','________','________','________']],[150,100,100,162])
 p('Si rms=0 siempre: revisar L/R a GND, SD en GPIO1, 3.3 V y relojes. Si pico ~ 1 sostenido: revisar formato, interferencia y volumen. Si responde solo al mover cables, corregir contactos. No tratar valores de inicializacion como mediciones validas.')
 h('Actividad y verificacion')
 p('Comparar una palmada breve con una vocal sostenida de intensidad moderada: ¿cual tiene mayor pico/RMS?, ¿el umbral fijo genera falsas detecciones? Cambiar una sola constante a la vez y registrar el efecto.')
 checklist(['RMS dinamico','No saturacion permanente','MPU sigue midiendo','FFT restaurada','Modos y LED conservados'])
 code(3)

 practice_start(4,'Bateria y Bluetooth','Publicar estado en un telefono y ensayar la medida de entrada protegida.','ADC calibrado, histeresis, servicios GATT, lectura y notificaciones BLE.','H3; Android con BLE y nRF Connect. Para medir: H4, multimetro y fuente limitada. PILAS=false al comenzar.')
 page('P4 · BLE y sus limites')
 p('Instalar desde Gestor de bibliotecas <b>NimBLE-Arduino 2.5.2</b> de h2zero. Se usa porque ofrece BLE con menor carga de recursos que alternativas basadas en el stack clasico. No instalar otra NimBLE ni reemplazarla con BLESerial. Las firmas de callbacks varian entre versiones: el codigo está fijado a 2.5.2. Abrir P4, compilar y subir conservando bibliotecas de P2.')
 p('BLE transmite pequeños datos con bajo consumo relativo. El ESP32 anuncia su nombre; Android actua como central. Un <b>servicio</b> agrupa datos y una <b>caracteristica</b> contiene un valor y permisos. Una UUID identifica cada uno. “Leer” solicita el valor actual; “notificar” permite recibir cambios despues de suscribirse. Una notificacion GATT no crea por si misma una alerta del sistema operativo ni un sonido con la pantalla bloqueada.')
 table([['UUID (mismo sufijo)','Contenido / permiso'],['8d6c0001-3d68-4b85-9b71-4d3943414c4d','Servicio K9 CALM'],['8d6c0002-3d68-4b85-9b71-4d3943414c4d','Estado ASCII: READ y NOTIFY, cada 500 ms'],['8d6c0003-3d68-4b85-9b71-4d3943414c4d','Voltaje ASCII: READ; “USB; NA” si PILAS=false']],[285,227])
 p('Ejemplo <b>A E2 B0 Q80</b>: A automatico (M manual); E0 normal, E1 sospechoso, E2 posible reaccion, E3 insuficiente; B0 normal/USB, B1 baja, B2 critica, B3 ADC invalido; Q puntuacion experimental 0-100. El estado ocupa menos de 20 bytes y funciona con MTU ATT minimo de 23. La caracteristica de voltaje distingue USB de bateria real.')
 p('No se publica Battery Service 0x180F/2A19 porque exige un porcentaje que no hemos validado para estas AAA. Se comunica voltaje y estado mediante servicio propio. No se transmite audio ni se guarda informacion de mascotas. El ejemplo no exige autenticacion: usarlo en laboratorio, sin datos personales.')

 page('P4 · Conectarse desde Android')
 p('1. Instalar <b>nRF Connect for Mobile</b> de Nordic Semiconductor desde la tienda oficial; verificar el editor. Activar Bluetooth y conceder “dispositivos cercanos”; Android antiguo puede pedir ubicacion para escanear. No es necesario emparejar desde Ajustes para este ejemplo.')
 p('2. Subir P4 y abrir nRF Connect > Scanner > Scan. Buscar K9-CALM; acercar el telefono a un metro. Si el nombre no aparece, buscar la UUID de servicio; revisar que el escaneo activo permita respuesta de scan. Solo un telefono debe conectarse para simplificar el ensayo.')
 p('3. Pulsar Connect y expandir el servicio personalizado. En la caracteristica terminada en 0002, pulsar lectura y elegir visualizacion UTF-8/Text. Activar notificaciones con el control de suscripcion; su icono puede variar. Debe recibirse un valor aproximadamente cada 500 ms.')
 p('4. Pulsar el boton fisico: A cambia a M. En la caracteristica 0003 leer “USB; NA”. Reproducir el sonido de P3: P4 comunica E1, aun sin comparar movimiento posterior. Desconectar desde la app y volver a buscar: el callback reinicia la publicidad.')
 h('Lo que se incorpora al codigo')
 p('<b>iniciarBLE()</b> configura servidor, servicio, caracteristicas y anuncio. <b>publicar()</b> actualiza las dos caracteristicas sin imprimir muestras individuales; notify() solicita una entrega, no garantiza que la app este suscrita. <b>Conexion::onDisconnect()</b> usa la firma de NimBLE 2.5.2 y vuelve a anunciar.')
 p('<b>medirPilas()</b> corre cada segundo solo si PILAS=true. Promedia 16 valores en mV, reconstruye voltaje y clasifica con histeresis. B3 indica lectura fuera del rango didactico 100-2400 mV, no cualquier falla electrica. Un divisor mal montado puede aparentar voltaje valido: el multimetro sigue siendo necesario.')
 note('En P4, E1 queda como memoria del ultimo impulso hasta reiniciar; el pulso del LED dura 1 s. En P5 el estado vuelve a normal tras la espera. Esta diferencia prepara la maquina de estados.','Informacion')

 page('P4 · Ensayar ADC y alarmas')
 p('Primero mantener USB y pack desconectado. Para probar el divisor sin energizar dos veces la placa: separar fisicamente el cable Ventrada -> pin 5V. Conectar la fuente limitada solo a R1 y GND comun, medir el nodo y confirmar &lt;=2.4 V. No usar pilas durante este ensayo. Con la placa ya alimentada, variar la fuente de prueba entre 3.6 y 4.8 V, sin superar el rango permitido del nodo.')
 p('Cambiar PILAS=true temporalmente para ensayar ADC; compilar y subir. Esperar un segundo por punto y comparar lectura con multimetro en el punto superior R1-GND. Calcular CAL y repetir. Probar entrada de 4.2 V, 3.95 V, 4.05 V y 4.2 V: entra en baja en 3.95 y solo sale por arriba de 4.15. Probar 3.75 V para critica; el LED parpadea rapido. Estos valores ensayan logica, no aprueban la alimentacion real.')
 table([['V fuente / multimetro','V ADC esperada','V programa','B / LED'],['4.20 V','1.680 V','________','0'],['3.95 V','1.580 V','________','1 / lento'],['4.05 V','1.620 V','________','1 / permanece'],['4.20 V','1.680 V','________','0 / sale'],['3.75 V','1.500 V','________','2 / rapido']],[160,122,110,120])
 p('Al terminar, restaurar PILAS=false para USB normal. Para pasar a AAA, ejecutar toda la validacion H4, fijar umbrales reales, conectar el cable de Ventrada a 5V solo sin USB y cargar firmware PILAS=true previamente. Si no hay regulador identificado o estabilidad demostrada, permanecer en modalidad USB.')
 h('Analisis y criterios de avance')
 p('¿Por que un voltaje bajo no equivale a un porcentaje exacto? ¿Por que la alarma no evita un reinicio por una caida rapida? Registrar el error maximo en tres puntos y distinguir caida de D1 de error ADC. Si BLE no cambia, releer valor y verificar suscripcion antes de modificar el codigo.')
 checklist(['BLE lee A/M','Suscripcion recibe datos','ADC comparado con multimetro','Histeresis comprobada','PILAS=false restaurado en USB'])
 code(4)

 practice_start(5,'Integrar el detector','Relacionar un impulso con cambios de actividad y emitir una categoria experimental.','Ventanas previas/posteriores, calidad de datos, estados, puntuacion y enfriamiento.','Todo H5 en USB, Android, multimetro y objeto/peluche; sin motor y sin animales.')
 page('P5 · Decidir con memoria')
 p('No se añade una biblioteca. Abrir P5 completo: conserva controles, escaner I2C, lecturas, FFT, ADC condicional y BLE. En automatico añade OBSERVAR, POSTERIOR y REPOSO. En manual mide y publica, pero desarma la clasificacion; la letra l controla el LED, salvo que una alarma de alimentacion tenga prioridad.')
 fig('08_estados','Figura 15. Transicion por impulso, evaluacion tras 1.5 s y espera de 2 s antes de volver a observar.')
 p('<b>OBSERVAR:</b> historial circular de 100 valores de actividad, unos 2 s. Al detectar impulso se congela media previa y desviacion estandar. <b>POSTERIOR:</b> acumula 1.5 s de actividad nueva. <b>REPOSO:</b> muestra la decision y espera 2 s para evitar contar repetidamente el mismo episodio. La alerta visual dura 1.5 s, y BLE publica el estado durante el reposo.')
 p('La media previa resume el nivel habitual; sigma mide su variacion. El cambio significativo exige <b>media posterior > media previa + max(0.7,3×sigma)</b>. Las unidades siguen siendo m/s². Si la actividad previa ya era alta o variable, sube el umbral. Este criterio puede perder una reaccion breve; no es una regla universal de comportamiento.')
 p('Calidad suficiente requiere 100 lecturas previas, IMU reciente (<80 ms), audio reciente (<100 ms), pico inicial <0.98 y al menos 60 muestras posteriores. Un hueco durante la observacion posterior invalida la decision. La comprobacion temporal no detecta todos los errores de DMA ni verifica calibracion fisica: inspeccionar tambien trazas y cables.')

 page('P5 · Tabla de decision y puntuacion')
 table([['Impulso','Datos suficientes','Cambio posterior','Categoria'],['No','Cualquiera','Cualquiera','E0 Actividad normal*'],['Si','No','Cualquiera','E3 Informacion insuficiente'],['Si','Si','No','E1 Evento acustico sospechoso'],['Si','Si','Si','E2 Posible reaccion de sobresalto']],[60,105,110,237])
 p('*“Normal” significa sin evento pendiente segun este detector; no certifica ausencia de miedo. Sin impulso, aun con movimiento, no se crea una reaccion. E3 solo se produce despues de un impulso recibido: un microfono completamente desconectado puede impedirlo. Revisar sensores al inicio, no confiar solo en la categoria.')
 p('<b>Puntuacion:</b> +60 por cambio de movimiento; +20 si ataque>0.01, de lo contrario +10; +20 si fraccion agudos>0.25. Si faltan datos, Q=0. Por ejemplo: cambio si, ataque 0.02 y agudos 0.30 produce Q=100. Sin cambio y con el mismo sonido, Q=40 pero sigue E1. La categoria depende de la tabla, no de un umbral secreto de Q.')
 p('La puntuacion es una heuristica para comparar ensayos, no probabilidad. Un sonido grave podria generar E2 y Q80, mientras uno agudo genera E1 y Q40. FFT y ataque describen el sonido; no prueban miedo ni identifican su fuente. Mantener distancia, volumen y fijacion constantes para comparar resultados.')
 fig('08_flujo','Figura 16. Orden cooperativo de tareas. No hay delay(); las operaciones I2C/FFT/ADC aun requieren tiempo finito.',width=420)
 h('Lectura por modulos')
 p('<b>integrar()</b> copia estadisticas previas al disparo, cuenta lecturas nuevas con ultimoIMU, valida calidad y decide una sola vez. <b>inicioEvento</b> fija la ventana posterior; <b>descanso</b> limita repeticiones. <b>alertaHasta</b> controla el LED. El aviso de bateria tiene prioridad: lento para baja, rapido para critica o ADC invalido. El programa no corta potencia.')

 page('P5 · Protocolo guiado de integracion')
 p('Encender y esperar 5 s con objeto quieto. Verificar 0x68, audio variable y BLE conectado. Trabajar con PILAS=false. Registrar fecha, firmware, distancia al altavoz, volumen, montaje y resultado; dejar al menos 5 s entre ensayos. Repetir cada condicion cinco veces.')
 table([['Caso','Accion controlada','Esperado'],['1','Sin audio impulsivo, objeto quieto','E0; actividad baja'],['2','Mover objeto sin sonido','E0; actividad puede subir'],['3','Grabacion impulsiva moderada, sin mover','E1 si supera detector'],['4','Mismo sonido y mover suavemente el objeto durante 1.5 s','E2 si se supera cambio'],['5','Sonido antes de completar historia tras reinicio','E3 si hay impulso despues del segundo inicial y antes de 2 s de historia'],['6','Modo manual; sonido y movimiento','M y E0; no clasifica'],['7','Dos impulsos separados menos de 2 s','Sin decisiones repetidas por el mismo episodio'],['8','Desconectar y reconectar BLE desde app','Vuelve a anunciar y permite consultar']],[40,290,182])
 p('Para probar E3 sin tocar cables energizados, reiniciar y emitir grabacion entre 1.2 y 1.8 s; si no dispara, repetir con calma. No retirar sensores con energia. Para simular falla del IMU, desconectar su alimentacion sin USB y volver a encender; revisar mensaje de ausencia y una clasificacion insuficiente si se detecta impulso.')
 h('Si no se obtiene el resultado previsto')
 p('Primero confirmar si hubo impulso: si rms no supera el umbral, no se abre ventana. Si E1 persiste al mover, revisar act y el tiempo del movimiento, sin aumentar volumen. Si E3, comprobar historia y nPost; no reducir controles de calidad para “forzar” E2. Si hay reinicios, detener ensayos y revisar alimentacion antes de ajustar clasificadores.')
 h('Actividad de analisis y avance')
 p('Crear matriz de resultados de cinco repeticiones por caso. Calcular falsos positivos (E2 sin movimiento previsto) y falsos negativos (sin E2 cuando el ensayo lo esperaba). Son medidas del protocolo simulado, no precision sobre perros. Proponer una mejora y justificarla con registros.')
 checklist(['Se conservan P1-P4','E0/E1/E2/E3 explicados','Modo manual desarma','BLE informa','Sin repeticion inmediata','Sin uso animal'])
 code(5)

 page('Pruebas finales y limites','CIERRE / VERIFICACION Y CONSULTA')
 table([['Comprobacion','Criterio / evidencia a registrar'],['Inspeccion sin energia','Continuidad de cada red; sin corto 3V3-GND; serigrafia coincide.'],['USB solamente','Cinco practicas arrancan sin pack; monitor no es necesario para operar.'],['Sensores','0x68 estable; a cercana a gravedad en reposo; rms dinamico sin saturacion.'],['Carga de trabajo','Con BLE suscrito, lecturas recientes y nPost &gt;=60. Sin reinicios 10 minutos de banco.'],['Pilas (condicional)','Ficha LDO, barrido bajo carga, umbrales ajustados y temperaturas registradas.'],['Mecanica','Caja aislada, conector desmontable, sensor firme, mic y antena libres.'],['Documentacion','Registro distingue ensayo sintetico, compilacion y medida fisica.']],[120,392])
 h('Registro breve por equipo')
 p('Placa/marcaje LDO: ____________________  Firmware: _________<br/>3V3 con USB: ______ V  Entrada minima estable: ______ V<br/>Corriente promedio/pico observada: __________ Instrumento: __________<br/>CAL: ______  Baja/critica validadas: ______ / ______ V<br/>Resultados casos P5: __________________________________________<br/>Responsable y fecha: __________________________________________')
 note('No hay hardware fisico conectado en esta elaboracion. Las conexiones se revisan teoricamente; los ensayos reales de alimentacion, radio, sonido y bienestar quedan pendientes. La compilacion registrada no certifica un montaje.','Alcance')
 p('Para usar una pechera fuera del banco se requieren evaluaciones de seguridad electrica, termica y mecanica, y validacion profesional de bienestar. El motor sigue siendo una extension de laboratorio. Clasificar eventos no constituye tratamiento del miedo.')

 page('Diagnosticar por sintomas · 1')
 table([['Sintoma','Posible causa','Como comprobar','Solucion'],
 ['PC no detecta placa','Cable solo carga o USB sin datos','Cambiar cable/puerto; comparar listado antes/despues','Cable de datos; identificar USB nativo o puente'],
 ['Error de compilacion','Placa/version equivocada o sintaxis','Leer primer error y core seleccionado','ESP32C3 Dev Module; core 3.3.4; codigo completo'],
 ['No encuentra .h','Biblioteca faltante','Gestor de bibliotecas y ruta del error','Instalar versiones fijadas y dependencias'],
 ['Falla al subir','Puerto ocupado o arranque','Cerrar monitor/otras apps; revisar nuevo puerto','BOOT+RESET; elegir puerto de arranque; 115200'],
 ['Serial ilegible/vacio','Baudrate o CDC','Monitor a 115200; CDC Enabled','Corregir opciones, subir, RESET'],
 ['Error en callback NimBLE','Otra version de biblioteca','Leer version y firma onDisconnect','NimBLE-Arduino 2.5.2; quitar duplicados'],
 ['MPU no detectado','SDA/SCL, AD0 o alimentacion','Escaner; medir reposo lineas y VCC','4 SDA, 5 SCL, AD0 GND; pull-ups 3V3'],
 ['Movimiento absurdo','Modulo suelto o rango saturado','Fijar en mesa; revisar norma y orientacion','Sujetar, comprobar VCC/rango, repetir'],
 ['Sin audio','L/R equivocado o SD incorrecto','Ver H3 y RMS, inspeccionar reloj si posible','L/R GND; SD 1; SCK6; WS7'],
 ['Muestras I2S incorrectas','Ranuras/formato inadecuados','Revisar 32 bits estereo y desplazamiento','Usar P3 fijado; no mezclar API legacy'],
 ['Pico saturado','Audio muy fuerte o formato erroneo','Pico ~ 1 aun en silencio; bajar volumen','Corregir formato, desacoplo y distancia'],
 ['GPIO no responde','Se confundio posicion con numero','Continuidad sin energia y serigrafia','Seguir mapa; GPIO10 no es pin fisico 10']],[91,112,152,157])

 page('Diagnosticar por sintomas · 2')
 table([['Sintoma','Posible causa','Como comprobar','Solucion'],
 ['Reinicios','Caida en LDO, cable o sobrecorriente','Leer brownout; medir entrada/3V3 bajo BLE','Volver USB, validar H4; no desactivar brownout'],
 ['Voltaje incorrecto','R1/R2 invertidas o CAL mal','Medir resistencias sin energia y nodo con CC','150k arriba/100k abajo; recalibrar'],
 ['ADC inestable','Nodo alto en impedancia o GND flojo','Comparar multimetro en tres voltajes','100nF cerca GPIO0; promedio; soldar GND'],
 ['B3 permanente','Entrada ADC fuera de 100-2400mV','Medir nodo, revisar PILAS y fuente','Reparar divisor; en USB dejar PILAS=false'],
 ['Critica muy temprano','Dropout o umbral sin validar','Barrido H4 y tension despues D1','Fijar umbrales con margen; rechazar AAA si no estable'],
 ['BLE no aparece','Firmware no P4/P5 o permisos','Serial; Scanner; nombre y UUID','Conceder permisos; reiniciar; desconectar otro cliente'],
 ['No hay notificaciones','No suscrito o app desconectada','Leer caracteristica y activar suscripcion','Suscribirse a 0002; no esperar aviso del SO'],
 ['LED no enciende','Polaridad, resistencia, modo o B','Modo manual + l; medir GPIO10','Corregir H1; revisar alarma con prioridad'],
 ['Falsos positivos','Ruido, cables sueltos o actividad previa','Repetir control sin sonido y sin mover','Fijar montaje; calibrar umbral con registros'],
 ['P5 siempre E1','No cambia media posterior','Leer pre/post y sincronizar movimiento','Mover despues del impulso; revisar metrica'],
 ['P5 siempre E3','Historia corta o huecos de lectura','Esperar 5s; revisar nPost y mensajes','Corregir IMU/audio; quitar tareas largas'],
 ['P5 deja de actualizar','Bloqueos añadidos o biblioteca diferente','Probar P3/P4; comparar fuentes','Restaurar versiones y loop sin delay'],
 ['No se recupera tras reparar','Inicializacion solo ocurre en setup','Comprobar mensaje MPU AUSENTE','Apagar, corregir cableado y reiniciar']],[91,112,152,157])

 page('Glosario de bolsillo')
 table([['Termino','Significado en este proyecto'],
 ['ADC','Convertidor de voltaje a un valor digital. No se usa para el microfono I2S.'],
 ['Amplitud / pico','Valor de una muestra / mayor valor absoluto en una ventana.'],
 ['Antirrebote','Acepta el boton solo tras 30 ms de estabilidad.'],
 ['BLE / GATT','Enlace de bajo consumo / organizacion en servicios y caracteristicas.'],
 ['Brownout / dropout','Reinicio por alimentacion baja / margen minimo que necesita el regulador.'],
 ['Calibracion','Comparacion con una referencia para reducir error; no crea exactitud ilimitada.'],
 ['DMA','Hardware que transfiere muestras a memoria mientras CPU hace otras tareas.'],
 ['FFT / bin','Transformada rapida de Fourier / intervalo de frecuencia del espectro.'],
 ['GPIO / GND','Pin de entrada/salida / referencia comun de potencial.'],
 ['Gravedad / g','Aceleracion de referencia; g ~ 9.80665 m/s². No confundir con gramos.'],
 ['Histeresis','Umbrales distintos para entrar y salir de una alarma.'],
 ['I2C / SDA / SCL','Bus de registros / datos / reloj. Direccion MPU: 0x68.'],
 ['I2S / BCLK / WS / SD','Bus de audio / reloj de bits / ranura / datos digitales.'],
 ['LDO','Regulador lineal de baja caida; en la placa produce 3.3 V.'],
 ['Muestreo / Hz','Tomar valores periodicamente / ciclos o muestras por segundo segun contexto.'],
 ['Pull-up / pull-down','Resistencia que define alto / bajo cuando nadie conduce la linea.'],
 ['RMS / Hann','Medida cuadratica de amplitud / ventana para reducir fuga espectral.'],
 ['Sigma / norma','Desviacion estandar / longitud del vector de tres ejes.'],
 ['UUID / MTU','Identificador de servicio o dato / tamaño maximo de paquete negociado.'],
 ['Velocidad angular','Rapidez de giro; rad/s en las lecturas usadas aqui.']],[125,387])

 page('Fuentes tecnicas y licencias')
 p('Consulta documental: 27 de octubre de 2026. Se revisaron README, licencias y actividad de los seis repositorios solicitados, mas Adafruit Unified Sensor. Las fuentes se aplicaron al formato I2S, API del sensor, callbacks BLE y seleccion del dibujo por terminales. Versiones fijadas, no equivalentes a “ultima version”.')
 refs=[
 ('R1 · ESP32-C3, Espressif','https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf','Datos electricos, GPIO, strapping y radio. Complementar con guia de hardware.'),
 ('R2 · Arduino-ESP32','https://github.com/espressif/arduino-esp32','Core 3.3.4; LGPL-2.1. Se usan API GPIO/ADC y driver estandar incluido.'),
 ('R3 · Instalacion oficial','https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html','Gestor de placas y URL oficial.'),
 ('R4 · ADC oficial','https://docs.espressif.com/projects/arduino-esp32/en/latest/api/adc.html','analogReadMilliVolts, resolucion y rangos por chip.'),
 ('R5 · I2S ESP-IDF','https://docs.espressif.com/projects/esp-idf/en/v5.5/esp32c3/api-reference/peripherals/i2s.html','Controlador std, ranuras Philips, DMA y lectura con timeout.'),
 ('R6 · INMP441, InvenSense','https://www.invensense.com/wp-content/uploads/2015/02/INMP441.pdf','Formato de 24 bits, 64 relojes, L/R y pulldown SD 100k.'),
 ('R7 · Adafruit MPU6050','https://github.com/adafruit/Adafruit_MPU6050','2.2.9; BSD-3-Clause (license.txt). API getEvent, rangos y unidades.'),
 ('R8 · Adafruit BusIO','https://github.com/adafruit/Adafruit_BusIO','1.17.4; MIT. Dependencia de comunicacion.'),
 ('R9 · Unified Sensor','https://github.com/adafruit/Adafruit_Sensor','1.1.15; Apache-2.0. Estructuras de lecturas.'),
 ('R10 · NimBLE-Arduino','https://github.com/h2zero/NimBLE-Arduino','2.5.2; Apache-2.0 y avisos de terceros. Servidor/advertising/callbacks.'),
 ]
 for title,url,desc in refs:
  if title.startswith('R7'): page('Bibliotecas y versiones fijadas')
  h(title);story.append(Paragraph(f'<link href="{url}" color="{CYAN}">{url}</link>',styles['small']));p(desc)

 page('Recursos visuales y reproducibilidad')
 more=[
 ('R11 · Fritzing','https://github.com/fritzing/fritzing-app','Aplicacion revisada; codigo GPLv3 y otras licencias por componente. No instalada; no se ejecutaron scripts ni se distribuye la aplicacion.'),
 ('R12 · Adafruit Fritzing Library','https://github.com/adafruit/Fritzing-Library','CC BY-SA 3.0 segun LICENSE. Revisada como referencia de representacion; no se copiaron piezas graficas ni imagenes.'),
 ('R13 · SuperMini, esquema de distribuidor','https://dl.artronshop.co.th/ESP32-C3%20SuperMini%20datasheet.pdf','Referencia secundaria para columnas de 16 pines. No identifica de forma universal el regulador ni reemplaza el esquema de la unidad real.'),
 ('R14 · MPU6050, guia Adafruit','https://learn.adafruit.com/mpu6050-6-dof-accelerometer-and-gyro','Explicacion de aceleracion/giro y uso de biblioteca; no asumir que breakout Adafruit y GY-521 sean electricamente identicos.'),
 ('R15 · Nordic nRF Connect','https://www.nordicsemi.com/Products/Development-tools/nRF-Connect-for-mobile','App BLE Android; controles pueden cambiar entre versiones.'),
 ('R16 · Arduino IDE','https://www.arduino.cc/en/software','Descarga del entorno; usar distribucion oficial.'),
 ('R17 · Guia hardware C3','https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/schematic-checklist.html','Recomendacion de fuente y desacoplo del chip.'),
 ]
 for title,url,desc in more:
  if title.startswith('R16'): page('Herramientas de esta edición')
  h(title);story.append(Paragraph(f'<link href="{url}" color="{CYAN}">{url}</link>',styles['small']));p(desc)
 p('Los esquemas electricos se dibujan en SVG y conservan terminales verificables. La portada utiliza una ilustracion conceptual generada con IA, identificada como tal. Las vistas de placa y sensores son esquematizaciones identificadas; el orden fisico de sensores varia por proveedor. Las graficas son sinteticas. Se distribuyen SVG editables y PNG de alta resolucion.')
 p('Herramientas usadas: skill pdf, Python/ReportLab, PyMuPDF, Pillow y Poppler. Fritzing y KiCad CLI no estaban disponibles; los diagramas SVG por terminal ofrecen una alternativa auditable. No se encontro una skill especializada en Arduino entre las disponibles; no se invento una. La generacion de imagen se uso para la portada conceptual; no para inventar pines o cableado.')
 # validation record dynamically populated from real log summaries
 page('Registro de verificacion de esta entrega')
 result_path=P/'Fuentes_PDF'/'compilacion.json'
 results=json.loads(result_path.read_text()) if result_path.exists() else []
 table([['Practica','Verificacion de compilacion'],*[[str(i),next((r['resultado'] for r in results if r['practica']==i),'Pendiente; consultar README antes de usar')] for i in range(1,6)]],[70,442])
 p('Configuracion de referencia: Arduino-ESP32 3.3.4, ESP32C3 Dev Module (esp32:esp32:esp32c3), USB CDC habilitado; Adafruit MPU6050 2.2.9, BusIO 1.17.4, Unified Sensor 1.1.15 y NimBLE-Arduino 2.5.2. Las cinco fuentes completas se imprimen en el manual y se entregan como proyectos separados.')
 table([['Nivel','Resultado / limite'],['Revision electrica teorica','Sin conflicto entre GPIO asignados; USB18/19 y strapping2/8/9 reservados. Sensores a 3.3 V; divisor 150k/100k y fuente unica.'],['Calculos','R LED ~ 4mA; divisor×2.50; I2S16k×64=1.024MHz; FFT62.5Hz/bin; historial2s.'],['Pruebas numericas','FFT con tonos 500/4000 Hz y silencio; E1/E2/E3, reposo, modo manual e histeresis: verificadas con funciones extraidas del firmware. No emulan perifericos.'],['Ejecucion fisica','No realizada: faltan placa real, instrumentos, carga, sensores y ensayo de AAA.'],['Clasificador','Heuristica experimental; faltan datos etiquetados y validacion sobre condiciones reales.'],['Portatil','No aprobada por este documento: depende de LDO identificado y mediciones H4.']],[125,387])
 p('La carpeta de fuentes incluye los registros de compilacion, bibliotecas/versiones, diagramas originales y generador. El README explica como regenerar sin editar directamente el PDF. El paquete ZIP conserva la estructura K9_Calm solicitada; en el repositorio el PDF final reside exclusivamente en output/pdf/K9_Calm/.')

 # Build PDF with visible consistent furniture. Flowable overflow is caught later.
 out=root/'output'/'pdf'/'K9_Calm';out.mkdir(parents=True,exist_ok=True)
 pdf=out/'Manual_K9_Calm.pdf'
 def footer(c,d):
  furniture(c,d,'MANUAL COMPLETO / CONSULTA')
 class ManualDoc(SimpleDocTemplate):
  def afterFlowable(self,flow):
   if isinstance(flow,Paragraph) and flow.style.name=='title':
    key=flow.getPlainText();self.record[key]=self.page
    if key=='K9 CALM' or key=='Comprar con criterio' or key.startswith(('01 /','02 /','03 /','04 /','05 /')) or key=='Pruebas finales y límites':
     mark='p'+str(self.page);self.canv.bookmarkPage(mark);self.canv.addOutlineEntry(key,mark,level=0)
 doc=ManualDoc(str(pdf),pagesize=(612,792),rightMargin=50,leftMargin=50,topMargin=54,bottomMargin=48,title='K9 CALM - Manual de laboratorio',author='Profesor Francisco López Velázquez | zolvek.com.mx',pageCompression=1)
 doc.record={}
 doc.build(story,onFirstPage=footer,onLaterPages=footer)
 pagination_file.write_text(json.dumps(doc.record,ensure_ascii=False,indent=2))
 # Source archive and documentation are populated separately, never a second loose PDF.
 print('PDF:',pdf)
 # Save extracted content for searchable edit/review; main source remains this module.
 (S/'Requisitos_de_entorno.txt').write_text('Python 3.11+\nreportlab\nPyMuPDF\nPillow\nFuentes Noto Sans y DejaVu Sans Mono (copias incluidas).\n')
