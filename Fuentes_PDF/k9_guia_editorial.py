"""Edición didáctica 3: páginas de taller, vector y ejemplos desarrollados."""
from pathlib import Path
import html,json,re
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor,Color
from reportlab.graphics import renderPDF
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from k9_identidad import furniture,REPO_URL,AUTHOR,WEBSITE
from k9_laminas import REGISTRY,generate,NAVY,TEAL,GRAY,LIGHT,PALE
from k9_aula_fuentes import NAMES
W=512
class Book:
 def __init__(self,path,public):
  self.public=public;self.c=canvas.Canvas(str(path),pagesize=(612,792));self.n=0;self.records={}
  self.c.setTitle('K9 CALM - Guía fácil de taller / edición 3');self.c.setAuthor('Profesor Francisco López Velázquez | zolvek.com.mx')
 def page(self,title,kicker='GUÍA FÁCIL / EDICIÓN DE TALLER',sub=None):
  if self.n:self.c.showPage()
  self.n+=1;self.records[title]=self.n
  class D:pass
  d=D();d.page=self.n;furniture(self.c,d,'GUÍA FÁCIL / EDICIÓN 3')
  self.c.bookmarkPage('p'+str(self.n));self.c.addOutlineEntry(title,'p'+str(self.n),level=0)
  self.text(50,66,kicker,8.2,TEAL,True)
  y=self.para(50,81,title,512,23,27,bold=True)
  if sub:y=self.para(50,y+8,sub,512,10.3,14.6)
  return y+14
 def text(self,x,y,t,size=9,c=NAVY,bold=False):
  self.c.setFillColor(HexColor(c));self.c.setFont('Bold' if bold else 'Body',size);self.c.drawString(x,792-y-size*.8,str(t))
 def para(self,x,y,t,w=512,size=10.3,lead=14.6,c=NAVY,bold=False):
  style=ParagraphStyle('p',fontName='Bold' if bold else 'Body',fontSize=size,leading=lead,textColor=HexColor(c))
  p=Paragraph(t,style);_,h=p.wrap(w,1000)
  if y+h>731:raise ValueError(('Desborde de texto',self.n,y,h,t[:80]))
  p.drawOn(self.c,x,792-y-h);return y+h
 def rule(self,y):
  self.c.setStrokeColor(HexColor(LIGHT));self.c.setLineWidth(.6);self.c.line(50,792-y,562,792-y)
 def head(self,y,n,t):
  self.c.setFillColor(HexColor(TEAL));self.c.roundRect(50,792-y-17,21,17,3,fill=1,stroke=0)
  self.c.setFillColor(HexColor('#ffffff'));self.c.setFont('Bold',8);self.c.drawCentredString(60.5,792-y-11,str(n))
  self.text(80,y+2,t,11.3,bold=True);return y+28
 def step(self,y,n,title,body):
  self.c.setStrokeColor(HexColor(LIGHT));self.c.setLineWidth(.8);self.c.circle(61,792-y-10,10,fill=0,stroke=1)
  self.c.setFillColor(HexColor(TEAL));self.c.setFont('Bold',9);self.c.drawCentredString(61,792-y-13,str(n))
  self.text(82,y,title,10.4,bold=True)
  end=self.para(82,y+18,body,480,size=10,lead=14)
  return end+15
 def callout(self,y,title,t):
  # Medir antes de dibujar para que fondo y contenido compartan altura.
  p=Paragraph(t,ParagraphStyle('box',fontName='Body',fontSize=9.7,leading=13.5,textColor=HexColor(NAVY)));_,h=p.wrap(481,500)
  height=h+36
  if y+height>731:raise ValueError(('Desborde aviso',self.n,y,height,title))
  self.c.setFillColor(HexColor(PALE));self.c.rect(50,792-y-height,512,height,fill=1,stroke=0)
  self.c.setFillColor(HexColor(TEAL));self.c.rect(50,792-y-height,2,height,fill=1,stroke=0)
  self.text(63,y+10,title,9.5,bold=True);p.drawOn(self.c,63,792-y-27-h)
  return y+height+12
 def table(self,y,heads,rows,widths):
  x=50;headerh=24
  self.c.setFillColor(HexColor(NAVY));self.c.rect(50,792-y-headerh,512,headerh,fill=1,stroke=0)
  for h,w in zip(heads,widths):self.text(x+9,y+8,h,8.5,'#ffffff',True);x+=w
  y+=headerh
  for ri,row in enumerate(rows):
   plist=[];maxh=0
   for val,w in zip(row,widths):
    p=Paragraph(html.escape(str(val)),ParagraphStyle('cell',fontName='Body',fontSize=9.2,leading=12.5,textColor=HexColor(NAVY)));_,hh=p.wrap(w-18,1000);maxh=max(maxh,hh);plist.append((p,w,hh))
   height=maxh+15
   if y+height>731:raise ValueError(('Desborde tabla',self.n,y,row))
   if ri%2==0:self.c.setFillColor(HexColor(PALE));self.c.rect(50,792-y-height,512,height,fill=1,stroke=0)
   x=50
   for p,w,hh in plist:p.drawOn(self.c,x+9,792-y-7-hh);x+=w
   y+=height
  return y+12
 def figure(self,y,key,width=512):
  d=REGISTRY[key];scale=width/d.width;height=d.height*scale
  if y+height>731:raise ValueError(('Desborde figura',self.n,key,y,height))
  self.c.saveState();self.c.translate(50,792-y-height);self.c.scale(scale,scale);renderPDF.draw(d,self.c,0,0);self.c.restoreState()
  return y+height+8
 def terminal(self,y,label,lines):
  h=40+len(lines)*17
  self.c.setFillColor(HexColor(NAVY));self.c.roundRect(50,792-y-h,512,h,4,fill=1,stroke=0)
  self.text(64,y+11,label,8.2,'#a7d6dc',True)
  for i,line in enumerate(lines):
   self.c.setFillColor(HexColor('#ffffff'));self.c.setFont('Mono',9.5);self.c.drawString(64,792-y-42-i*17,line)
  return y+h+14
 def code(self,y,name,highlight):
  source=(self.public/'Codigo'/name/(name+'.ino')).read_text().splitlines();h=36+len(source)*12.2
  if y+h>731:raise ValueError(('Desborde código',self.n,y,h))
  self.c.setFillColor(HexColor(PALE));self.c.roundRect(50,792-y-h,512,h,4,fill=1,stroke=0)
  self.text(64,y+10,name+'.ino',8.5,TEAL,True);self.rule(y+28)
  for i,line in enumerate(source):
   yy=792-y-43-i*12.2
   if any(term in line for term in highlight):
    self.c.setFillColor(HexColor('#e0edf0'));self.c.rect(57,yy-3,498,12.2,fill=1,stroke=0)
   # Dibujo de una línea íntegra; sin números ni tokens insertados.
   self.c.setFont('Mono',8.8);self.c.setFillColor(HexColor(GRAY if line.lstrip().startswith('//') else NAVY));self.c.drawString(64,yy,line)
  return y+h+13
 def finish(self):self.c.save()

TOPICS=[
 {
 'title':'Luz y botón','new':'LED, resistencia de 330 ohm y pulsador.',
 'action':'El ESP32 controla una luz. El botón cambia cómo la usamos.',
 'why':'El LED necesita una resistencia para limitar corriente. El botón conecta GPIO3 a GND al pulsarlo; la placa detecta ese cambio.',
 'diagram':'H1_conexiones',
 'wires':[['GPIO10','330 ohm -> ánodo del LED'],['Cátodo del LED','GND'],['GPIO3','Un lado del pulsador'],['Otro lado del pulsador','GND']],
 'check':'Revisa el LED: el cátodo suele ser la pata corta y el lado plano. Comprueba los pares del botón con continuidad, sin USB. Rint del plano ya está dentro del ESP32: no la compres.',
 'before':'Conecta USB y mide entre 3V3 y GND: cerca de 3.3 V. No unas 3V3 con GND. Si hay calor o reinicios, retira USB y revisa.',
 'explain':[['const int PARPADEO_MS = 500;','Un número entero: fija 500 ms entre cambios de luz.'],['setup() / iniciar(1)','Prepara el equipo una vez, al encender.'],['loop() / actualizar()','Repite el trabajo y atiende el botón.'],['parpadear() / mostrar()','Controla la luz y escribe el modo.']],
 'high':['const int PARPADEO_MS'],
 'trace':[('El tiempo del programa','0 ms -> 500 ms -> 1000 ms'),('El LED en AUTO','apagado -> encendido -> apagado')],
 'test':[('Carga y mira','Verificar > Subir. Abre Monitor serie a 115200. El LED cambia cada medio segundo.'),('Pulsa una vez','Debe aparecer MANUAL y modo:0. Mantener pulsado no debe alternar continuamente.'),('Manda una orden','En MANUAL, escribe l (ele minúscula) y envía. La luz cambia. Vuelve a pulsar: AUTO.')],
 'output':['modo:1','MANUAL','modo:0'],
 'numbers':[['500','1.0 s por ciclo completo'],['250','0.5 s por ciclo completo'],['1000','2.0 s por ciclo completo']],
 'change':'PARPADEO_MS','reason':'Un ciclo incluye encender y apagar. Por eso 500 ms entre cambios producen un ciclo de 1000 ms.',
 'failure':'Si no prende, prueba MANUAL + l. Revisa LED al revés, resistencia y GPIO10. Si el botón nunca cambia, revisa sus pares de patas.',
 },
 {
 'title':'Medir movimiento','new':'Módulo GY-521 / MPU6050. Conserva LED y botón.',
 'action':'Primero observa un número; después úsalo para decidir si prende el LED.',
 'why':'El acelerómetro mide en tres ejes. La biblioteca resume el cambio en act. Una act pequeña indica poca variación; un umbral decide cuándo avisar. No mide miedo.',
 'diagram':'H2_conexiones',
 'wires':[['VCC / GND del GY-521','3V3 / GND del ESP32'],['SDA / SCL del GY-521','GPIO4 / GPIO5'],['AD0','GND: dirección 0x68'],['XDA, XCL e INT','Dejar sin conectar']],
 'check':'SDA lleva datos y SCL sincroniza la conversación. Ambos necesitan pull-ups a 3V3; muchos módulos ya los traen. Alimenta el módulo con 3V3 y comprueba que sea compatible.',
 'before':'Con USB, mide VCC-GND en el sensor. SDA y SCL en reposo deben estar cerca de 3.3 V, nunca 5 V. Después, el programa debe encontrar 0x68.',
 'explain':[['const float UMBRAL_MOV = 0.70;','float guarda decimales. 0.70 es el umbral en m/s².'],['aula.actividad()','Obtiene la última actividad calculada.'],['actividad() > UMBRAL_MOV','Pregunta: ¿el número es mayor que 0.70?'],['bool seMueve / encender(seMueve)','bool guarda sí/no. En AUTO, ese resultado controla la luz.']],
 'high':['const float UMBRAL_MOV'],
 'trace':[('Ejemplo quieto','act = 0.12; 0.12 > 0.70 es NO -> LED apagado'),('Ejemplo en movimiento','act = 1.10; 1.10 > 0.70 es SÍ -> LED encendido')],
 'test':[('Espera en la mesa','Sube P2 y espera 5 s sin tocarlo. Busca I2C 0x68 e IMU:1. La magnitud a debe aproximarse a 9.81.'),('Mueve el objeto','Fija el sensor a un objeto o peluche. Muévelo suave, sin golpear: act aumenta. El LED avisa si supera el umbral.'),('Déjalo quieto otra vez','act debe disminuir. Prueba también el botón: MANUAL sigue disponible.')],
 'output':['I2C 0x68','modo:1 a:9.81 giro:0.02 act:0.12 IMU:1'],
 'numbers':[['0.30','Más sensible a pequeños cambios'],['0.70','Valor de partida'],['1.20','Exige mayor actividad']],
 'change':'UMBRAL_MOV','reason':'La lectura act no cambia porque cambies el umbral; cambia la decisión. La misma act=0.50 prende con 0.30 y no prende con 0.70.',
 'failure':'Sin 0x68 o con IMU:0, revisa 4/SDA, 5/SCL, AD0 y GND. No interpretes act=0 como reposo si no hay datos recientes.',
 },
 {
 'title':'Detectar un sonido','new':'INMP441, 100 kohm de SD a GND y desacoplo si falta. Conserva P2.',
 'action':'Escucha un sonido moderado y compara su lectura con el ambiente.',
 'why':'El micrófono ya entrega números digitales. SCK y WS son relojes; SD lleva los datos al C3. rms resume la amplitud en una ventana: no es una medida de dB.',
 'diagram':'H3_conexiones',
 'wires':[['VDD / GND / L/R','3V3 / GND / GND'],['SCK / WS','GPIO6 / GPIO7'],['SD','GPIO1 y resistencia 100 kohm a GND'],['100 nF, si falta en módulo','Entre VDD y GND, cerca del micrófono']],
 'check':'L/R a GND elige el canal izquierdo, que es el que lee el código. No confundas SD del audio con SDA del acelerómetro. No tapes el orificio del micrófono.',
 'before':'Mide VDD-GND: cerca de 3.3 V. Después del arranque, habla suave y verifica que rms y pico cambien. Un reloj I2S no se comprueba con una lectura fija del multímetro.',
 'explain':[['ajustarSonido(UMBRAL_SONIDO)','Configura el mínimo de amplitud antes de iniciar.'],['aula.impulso()','Pregunta si se detectó un sonido brusco en esta vuelta.'],['if (...) { alertar(...); }','Si hubo impulso, guarda una alerta de duración definida.'],['actualizar() / encender()','Sigue leyendo ambos sensores; no usa delay para sostener la luz.']],
 'high':['const float UMBRAL_SONIDO','const int ALERTA_MS'],
 'trace':[('Ejemplo de ambiente','rms = 0.001; pequeño frente al mínimo 0.004'),('Ejemplo de sonido brusco','rms = 0.012; puede activar si cumple las otras condiciones')],
 'test':[('Aprende el ambiente','Sube P3 y espera 3 s. Habla suave: rms y pico deben variar. MIC:1 solo confirma datos recientes, no audio correcto.'),('Reproduce el sonido','Usa una palmada grabada a volumen moderado. Espera 3 s entre intentos. La alerta dura 1 s si detecta un impulso.'),('Conserva lo anterior','Mueve el objeto y observa act. El LED también puede encender por movimiento; deja el objeto quieto para probar solo sonido.')],
 'output':['modo:1 a:9.81 giro:0.02 act:0.10 IMU:1', 'rms:0.00100 pico:0.00300 MIC:1'],
 'numbers':[['0.008','Sube el mínimo: puede detectar menos'],['0.004','Valor de partida'],['0.002','Baja el mínimo: comprueba falsas alertas']],
 'change':'UMBRAL_SONIDO','reason':'El detector también considera ruido de fondo, ataque y pico/RMS. Superar 0.004 no garantiza una alerta. Después cambia ALERTA_MS=1500: solo debe durar más la luz.',
 'failure':'Audio siempre cero: revisa L/R a GND y SD=1. Pico cerca de 1 permanentemente: baja volumen y revisa formato/cables. Evita sonidos fuertes.',
 },
 {
 'title':'Ver datos en el teléfono','new':'No agregues cables. El C3 ya tiene Bluetooth Low Energy.',
 'action':'Lleva el mismo estado del monitor serie al teléfono.',
 'why':'BLE publica un servicio y dos características: un dato de estado y otro de voltaje. La app consulta o se suscribe. No necesita internet para ese enlace.',
 'diagram':'07_sistema',
 'wires':[['Sensores, LED y botón','Exactamente como en P3'],['Alimentación','USB como única fuente'],['GPIO0','Libre; MEDIR_DIVISOR=false'],['Portapilas y motor','No se conectan en esta guía']],
 'check':'No añadas una tarjeta Bluetooth: ya está integrada. Usa nRF Connect for Mobile de Nordic Semiconductor. La cuenta o la nube no forman parte de la práctica.',
 'before':'Primero comprueba que P3 funciona. Si cambiaste valores, anótalos. Para empezar P4 usa los valores que aparecen en el archivo entregado.',
 'explain':[['prepararMedicion(false,...)','Deja el ADC opcional apagado durante USB normal.'],['iniciar(4)','Conserva P3 y agrega el servicio BLE.'],['aula.enviar()','Actualiza estado cada 500 ms cuando corresponde.'],['aula.mostrar()','Mantiene el monitor serie para comparar con el teléfono.']],
 'high':['const bool MEDIR_DIVISOR','const float CALIBRACION'],
 'trace':[('A E1 B0 Q0','Automático / último impulso / USB o normal / puntuación 0'),('M E1 B0 Q0','El botón cambia A a M; en P4 E1 queda hasta reiniciar')],
 'test':[('Escanea y conecta','Abre nRF Connect: Scanner > Scan > K9-CALM > Connect. Concede permisos de dispositivos cercanos si Android los pide.'),('Lee una característica','Expande el servicio 8d6c0001. En 0002 pulsa Read y elige texto UTF-8. Activa su suscripción para recibir cambios.'),('Compara dos pantallas','Pulsa el botón: A cambia a M. Lee 0003: USB; NA. En la computadora, modo también cambia.')],
 'output':['A E1 B0 Q0','M E1 B0 Q0','USB; NA'],
 'numbers':[['1000 -> 500','ALERTA_MS: la luz dura menos'],['0.004 -> 0.008','UMBRAL_SONIDO: cambia la detección'],['false','MEDIR_DIVISOR: mantener así en USB normal']],
 'change':'Un valor por vez','reason':'La transmisión BLE no enciende por sí sola una notificación del sistema operativo. Debes permanecer conectado y suscrito dentro de la app.',
 'failure':'Si no aparece, revisa permisos y desconecta otros teléfonos. Si puedes leer pero no llegan cambios, activa la suscripción de 0002.',
 },
 {
 'title':'Relacionar sonido y movimiento','new':'No agregues componentes. Ahora cambia la forma de decidir.',
 'action':'Un ruido no basta: observa qué pasó antes y después.',
 'why':'El programa conserva 2 s de actividad previa. Si detecta un impulso, observa 1.5 s posteriores. Compara las medias (promedios de las lecturas) y comprueba que haya suficientes datos.',
 'diagram':'08_estados',
 'wires':[['Montaje','Conserva P4 y USB'],['Objeto','Sensor sujeto: no debe quedar colgando'],['Sonido','Grabación moderada, misma distancia'],['Personas y animales','Pruebas en mesa o peluche; sin perros']],
 'check':'Las categorías describen ensayos: E0 sin evento pendiente, E1 sonido, E2 posible cambio posterior, E3 datos insuficientes. Ninguna mide miedo con certeza.',
 'before':'Al iniciar, deja el objeto quieto 5 s. Revisa IMU:1, MIC:1 y que rms cambie con sonido. E0 por sí solo no demuestra que los sensores estén bien.',
 'explain':[['ajustarCambio(CAMBIO_MOV)','Fija la diferencia mínima de actividad que compararás.'],['compararEvento()','Gestiona historia previa, ventana posterior y espera.'],['aula.evento() == 2','Comprueba si la categoría actual es E2.'],['encender(...) / enviar()','Muestra la decisión mediante LED y BLE.']],
 'high':['const float CAMBIO_MOV'],
 'trace':[('Antes: 0.10 / después: 0.20','E1 si hubo impulso y datos válidos.'),('Antes: 0.10 / después: 1.20','Puede producir E2; requiere datos válidos y cambio suficiente.')],
 'test':[('Control: solo sonido','Tras 5 s quieto, reproduce el sonido sin mover nada. Debe producir E1 si detecta un impulso.'),('Añade movimiento posterior','Repite el mismo sonido y mueve el objeto durante el siguiente segundo y medio. Puede producir E2 si cambia suficiente.'),('Prueba MANUAL','Pulsa el botón: sigue midiendo y transmitiendo, pero P5 muestra M y E0; desarma la comparación automática.')],
 'output':['A E1 B0 Q20','A E2 B0 Q80','M E0 B0 Q0'],
 'numbers':[['0.30','Reduce el mínimo; observa falsas alertas'],['0.70','Valor de partida'],['1.20','Aumenta el mínimo de cambio']],
 'change':'CAMBIO_MOV','reason':'También cuenta la variación previa: se usa el mayor entre CAMBIO_MOV y tres veces esa variación. Q es una puntuación experimental, no un porcentaje de miedo.',
 'failure':'Siempre E1: revisa cuándo mueves el objeto y observa act. E3: espera 5 s y revisa lecturas recientes. No quites las condiciones de calidad para forzar E2.',
 },
]

def build(root,public):
 root=Path(root);public=Path(public)
 for name in ['Body','Bold','Mono']:pdfmetrics.registerFont(TTFont(name,str(public/'Fuentes_PDF/fonts'/(name+'.ttf'))))
 pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
 generate(public/'Diagramas',root/'tmp/pdfs/k9_laminas')
 out=root/'output/pdf/K9_Calm';out.mkdir(parents=True,exist_ok=True);book=Book(out/'Manual_K9_Calm_Guia_Facil.pdf',public)
 b=book
 y=b.page('K9 CALM','ZOLVEK / ELECTRÓNICA PARA PREPARATORIA','Guía fácil de taller. Cinco prácticas para construir y comprender el mismo prototipo.')
 cover=public/'Ilustraciones/K9_Calm_concepto.png';b.c.drawImage(str(cover),50,792-y-287,width=512,height=287,mask='auto',preserveAspectRatio=True,anchor='c');y+=298
 y=b.para(50,y,'Ilustración conceptual sobre maniquí; no muestra un montaje probado ni una intervención veterinaria.',512,8.5,12,c=GRAY)
 y=b.head(y+20,'01','Descarga el material del curso')
 y=b.para(50,y,f'<link href="{REPO_URL}" color="{TEAL}">{REPO_URL}</link>',512,11,16,bold=True)
 y=b.para(50,y+8,'En GitHub pulsa <b>Code > Download ZIP</b> y extrae la carpeta. El paquete incluye programas, biblioteca de aula y dependencias.')
 y=b.callout(y+10,'Tu objetivo','Hacer que una luz responda a pruebas de sonido y movimiento, y consultar el resultado en Android. Trabaja por USB, en mesa o peluche.')
 b.para(50,y,'<b>'+AUTHOR+'</b><br/>zolvek.com.mx',512,10,14)

 y=b.page('Primero entiende el recorrido','ANTES DE CONSTRUIR / QUÉ HACE EL EQUIPO')
 y=b.figure(y,'07_sistema')
 y=b.table(y+12,['Práctica','Lo que añades','Lo que debes lograr'],[
  ['1','LED y botón','Controlar luz y modo.'],['2','Sensor de movimiento','Leer act y elegir un umbral.'],['3','Micrófono digital','Detectar un impulso moderado.'],['4','Comunicación BLE','Leer el estado en el teléfono.'],['5','Comparación temporal','Relacionar antes y después.']],[55,160,297])
 y=b.head(y+3,'A','La rutina de todas las prácticas')
 y=b.para(50,y,'<b>Conecta sin USB -> comprueba -> copia el código -> sube -> observa -> cambia un valor.</b> Guarda el resultado antes de avanzar. El montaje anterior permanece.')
 b.callout(y+15,'Qué significa “posible reacción”','Solo significa que coincidieron un evento acústico y un cambio de actividad según una regla de ensayo. El prototipo no identifica ni trata miedo.')

 y=b.page('Materiales que sí vas a usar','ANTES DE CONSTRUIR / UNA LISTA PARA TODO EL CURSO')
 y=b.table(y,['Cant.','Material','Especificación'],[
  ['1','ESP32-C3 SuperMini','USB-C; 16 terminales; flash 4 MB.'],['1','Cable USB-C','De datos y alimentación.'],['1 + juego','Protoboard y cables','400/830 puntos; Dupont M-M y M-H.'],['1 + 1','LED rojo y resistencia','LED 3 mm + resistencia 330 ohm / 1/4 W.'],['1','Pulsador','Normalmente abierto.'],['1','GY-521 / MPU6050','Compatible con 3.3 V y pull-ups a 3.3 V.'],['1','INMP441','Micrófono digital I2S.'],['1','Resistencia 100 kohm','Para SD del micrófono a GND.'],['2','Capacitores 100 nF','Si los sensores no traen desacoplo.'],['1 juego','Cabeceras 2.54 mm','Soldadas, sin USB conectado.'],['Compartir','Multímetro y herramientas','Voltaje CC; soldadura con supervisión.'],['Disponibles','PC y Android BLE','Arduino IDE y nRF Connect.']],[46,160,306])
 b.callout(y+5,'Compra opcional para medir voltaje','Otra resistencia de 100 kohm, una de 150 kohm (ambas 1%) y otro capacitor de 100 nF. No necesitas pantalla, motor ni pilas para terminar.')

 y=b.page('Prepara Arduino una sola vez','CONFIGURACIÓN / PLACA Y PUERTO')
 y=b.step(y,1,'Instala Arduino IDE 2.x','Descárgalo de arduino.cc/en/software. Abre Archivo > Preferencias.')
 y=b.step(y,2,'Agrega el soporte de Espressif','En URLs adicionales del Gestor de tarjetas pega esta dirección:')
 y=b.callout(y,'URL oficial','<font size="8.5">https://espressif.github.io/arduino-esp32/package_esp32_index.json</font>')
 y=b.step(y,3,'Instala la versión del curso','Gestor de placas > esp32 by Espressif Systems > 3.3.4 > Instalar. Se necesita internet para descargar las herramientas de tu sistema.')
 y=b.table(y,['Ajuste','Usa este valor'],[['Placa','ESP32C3 Dev Module'],['USB CDC On Boot','Enabled'],['Flash','4 MB'],['Puerto','El que aparece al conectar tu USB de datos'],['Monitor serie','115200 baudios']],[170,342])
 y=b.figure(y+3,'11_ide')

 y=b.page('Instala la biblioteca del curso','CONFIGURACIÓN / SIN BUSCAR ARCHIVOS SUELTOS')
 y=b.step(y,1,'Encuentra tu sketchbook','En Archivo > Preferencias copia la Ubicación del sketchbook. Puede estar en Documentos o OneDrive: usa la ruta que indique tu IDE.')
 y=b.step(y,2,'Extrae el paquete en esa carpeta','Extrae Librerias/Instalar_todas.zip dentro del sketchbook. No lo metas dentro de otra carpeta libraries.')
 y=b.terminal(y,'COMPRUEBA ESTA RUTA',['Arduino/libraries/K9CalmAula/src/K9CalmAula.h'])
 y=b.step(y,3,'Reinicia Arduino IDE','En Programa/Sketch > Incluir biblioteca debe aparecer K9CalmAula. Las otras seis dependencias vienen en el mismo paquete.')
 y=b.table(y,['Biblioteca','Versión incluida'],[['K9CalmAula','1.0.0'],['MPU6050 / BusIO / Unified Sensor','2.2.9 / 1.17.4 / 1.1.15'],['GFX / SSD1306','1.13.0 / 2.5.17; no se necesita pantalla'],['NimBLE-Arduino','2.5.2']],[280,232])
 b.callout(y+5,'Qué hace la biblioteca de aula','Prepara los sensores y las comunicaciones. Tú escribirás las decisiones y cambiarás sus valores. Su código completo está en Biblioteca/K9CalmAula/src/.')

 y=b.page('Aprende a leer las conexiones','ANTES DE CONSTRUIR / UN PIN NO ES SU POSICIÓN')
 y=b.figure(y,'01_pinout')
 y=b.figure(y+10,'18_lectura_plano')
 b.callout(y+6,'Comprueba antes de conectar','Lee los números impresos de tu placa. GPIO10 significa el terminal marcado 10, no la décima pata. Los diagramas muestran circuitos equivalentes: no son fotografías ni la distribución de una protoboard.')

 y=b.page('El plano completo del montaje','ANTES DE CONSTRUIR / CONSULTA PARA LAS CINCO PRÁCTICAS')
 y=b.figure(y,'14_laboratorio')
 y=b.para(50,y+8,'<b>Lee las etiquetas:</b> SDA4 une GPIO4 con SDA del MPU6050; SD1 une GPIO1 con SD del micrófono y la resistencia R4. Dos nombres iguales representan la misma red, aunque no haya una línea larga entre ellos.',512,10,14)
 y=b.callout(y+14,'Monta una etapa por vez','Este plano reúne el circuito terminado. Empieza solo con LED y botón; añade sensores en las prácticas 2 y 3. No necesitas montarlo todo para comenzar.')
 b.para(50,y,'Los módulos pueden cambiar el orden físico de sus terminales. Sigue sus etiquetas impresas y las tablas de cada práctica; el símbolo no es una huella de montaje.',512,9.3,13,c=GRAY)

 for i,(name,t) in enumerate(zip(NAMES,TOPICS),1):
  y=b.page(f'{i:02d} / {t["title"]}',f'PRÁCTICA {i} / A · CONECTAR',t['action'])
  y=b.para(50,y,'<b>Con USB retirado:</b> '+t['new'])
  y=b.figure(y+8,t['diagram'])
  y=b.table(y+4,['Desde','Conecta hasta'],t['wires'],[175,337])
  y=b.para(50,y,t['why'],512,10,14)
  y=b.para(50,y+8,t['check'],512,9.3,13,c=GRAY)
  b.callout(y+10,'Comprueba esta etapa',t['before'])

  y=b.page(f'{i:02d} / Programa y entiende',f'PRÁCTICA {i} / B · UN ARCHIVO COMPLETO')
  y=b.para(50,y,'Abre el archivo de esta práctica o borra el editor y pega <b>todo</b> este bloque. No lo agregues debajo del programa anterior. El sombreado señala qué puedes cambiar.',512,10,14)
  y=b.code(y+10,name,t['high'])
  y=b.table(y,['Línea o función','Qué hace'],t['explain'],[210,302])
  if i in [1,2]:
   b.figure(y+2,'19_tiempo' if i==1 else '20_umbral')
  elif i==5:
   b.callout(y+2,'Ejemplos de medias: antes y después','<b>'+t['trace'][0][0]+':</b> '+t['trace'][0][1]+'<br/><b>'+t['trace'][1][0]+':</b> '+t['trace'][1][1])
  else:b.para(50,y,'<b>Después de copiar:</b> Verificar > Subir > Monitor serie a 115200. Si falla, revisa el primer error; no borres líneas para ocultarlo.',512,9.5,13.5,c=GRAY)

  y=b.page(f'{i:02d} / Observa, predice y cambia',f'PRÁCTICA {i} / C · UNA VARIABLE POR ENSAYO')
  for j,(title,body) in enumerate(t['test'],1):y=b.step(y,j,title,body)
  y=b.terminal(y,'FRAGMENTOS DE SALIDA / valores ilustrativos',t['output'])
  y=b.head(y,'4','Cambia '+t['change'])
  y=b.table(y,['Prueba','Qué debes comparar'],t['numbers'],[125,387])
  y=b.para(50,y,t['reason'],512,9.8,13.7)
  y=b.callout(y+10,'Si no obtienes el resultado',t['failure'])
  b.para(50,y,'<b>Registra:</b> cambié __________; predije __________; observé __________.<br/><b>Avanza cuando:</b> puedas repetir la prueba y explicar por qué cambió la salida.',512,9.5,14)

  if i==4:
   y=b.page('04 / Opcional: comprobar el ADC','PRÁCTICA 4 / EXTENSIÓN POR USB', 'Una medición conocida es la mejor forma de comprobar un voltímetro.')
   y=b.figure(y,'17_divisor_usb')
   y=b.step(y,1,'Conecta con USB retirado','3V3 -> 150k -> nodo GPIO0 -> 100k -> GND. Añade 100 nF entre el nodo y GND. No conectes pilas ni otra fuente.')
   y=b.step(y,2,'Mide antes de usar el número','Con USB conectado, mide 3V3 y el nodo. Si la entrada es 3.30 V, el nodo debe ser aproximadamente 1.32 V: el divisor deja pasar 0.4 veces el voltaje.')
   y=b.step(y,3,'Habilita la medición en P4','Cambia MEDIR_DIVISOR=true y sube. La biblioteca multiplica por 2.5 para reconstruir la entrada: debe mostrar cerca de 3.30 V.')
   y=b.callout(y,'Ejemplo de calibración','Si el multímetro marca 3.30 V y el programa 3.20 V, usa CALIBRACION=1.03125 (3.30 / 3.20). Repite la medición.')
   b.para(50,y,'Esta prueba no mide una batería. El aviso crítico es esperado porque 3.3 V está por debajo de los umbrales didácticos de pilas. Al terminar, vuelve a MEDIR_DIVISOR=false. AAA: solo después de validar el regulador según el manual completo.',512,9.5,13.5,c=GRAY)

 y=b.page('Comprueba el sistema completo','CIERRE / TU REGISTRO DE LABORATORIO')
 y=b.para(50,y,'Usa P5. Deja el objeto quieto 5 s al arrancar y entre ensayos. Mantén la misma grabación, volumen moderado y distancia. Repite cada caso tres veces.')
 y=b.table(y+10,['Ensayo','Resultado que comparas','Tus tres resultados'],[['Sin sonido ni movimiento','E0: sin evento pendiente','____ / ____ / ____'],['Sonido sin mover el objeto','E1 si se detecta un impulso','____ / ____ / ____'],['Mismo sonido + movimiento posterior','E2 si el cambio es suficiente','____ / ____ / ____'],['Modo MANUAL','M y E0; no clasifica','____ / ____ / ____']],[190,190,132])
 y=b.head(y+5,'?','Si aparece E3')
 y=b.para(50,y,'El detector recibió un impulso, pero no reunió suficientes datos para comparar. Espera 5 s y revisa IMU/MIC. Un micrófono sin audio puede no producir ningún impulso: E0 no sustituye comprobar sensores.')
 y=b.figure(y+12,'08_estados')
 b.callout(y+6,'Explica tu resultado','¿Qué pasó al cambiar el umbral sin cambiar el movimiento? ¿Qué diferencia hay entre detectar un ruido y comprobar un cambio posterior? La puntuación Q no es una probabilidad de miedo.')

 y=b.page('Si algo falla, vuelve a una prueba pequeña','CIERRE / DIAGNÓSTICO POR SÍNTOMAS')
 y=b.table(y,['Síntoma','Comprueba y corrige'],[['No aparece el puerto','Cable de datos; otro USB; observa qué puerto aparece al conectar.'],['No sube el programa','C3 Dev Module; CDC Enabled. BOOT + RESET y selecciona el puerto de arranque.'],['Falta K9CalmAula.h','Comprueba sketchbook/libraries/K9CalmAula/src; reinicia el IDE.'],['Falta otra biblioteca','Extrae las siete bibliotecas del paquete en el sketchbook.'],['Monitor vacío','115200 baudios; USB CDC Enabled; sube otra vez y pulsa RESET.'],['LED no responde','Prueba P1 en MANUAL + l; revisa polaridad, 330 ohm y GPIO10.'],['MPU ausente / IMU:0','Sin USB, revisa SDA4, SCL5, AD0 y tierra común. Reinicia.'],['Audio siempre cero','Sin USB, revisa SD1, SCK6, WS7 y L/R a GND.'],['BLE lee, pero no actualiza','Suscríbete a 0002 dentro de nRF Connect; no basta conectarse.'],['Reinicios o calor','Retira USB; busca cortos. No uses pilas en estas prácticas.'],['Alertas inesperadas','Fija sensores y prueba sonido sin movimiento. Cambia un valor por vez.']],[155,357])
 b.callout(y+5,'Necesitas ayuda útil','Anota la práctica, copia el primer error o la última salida y toma una fotografía clara del montaje sin energía. Cambiar varios cables y valores a la vez borra la pista del problema.')

 y=b.page('La vibración sigue siendo una pregunta','CIERRE / EVIDENCIA Y LÍMITES')
 y=b.callout(y,'No hay una ubicación calmante validada','La búsqueda no encontró evidencia clínica suficiente para indicar pecho, espalda o ambos ni una dosis por raza, kg, frecuencia o duración para calmar perros.')
 y=b.table(y,['Qué se investigó','Qué se puede concluir'],[['Vibración háptica','Algunos perros aprenden órdenes táctiles. Aprendizaje no equivale a reducir miedo.'],['Chalecos de presión','Son otra intervención; la evidencia sobre ansiedad es limitada e inconsistente.'],['K9 CALM','Conserva detección, LED y BLE. Motor opcional solo en banco o peluche.']],[170,342])
 for title,url in [('Chaleco háptico / estudio de caso, 2019','https://doi.org/10.1109/WHC.2019.8816079'),('Comunicación háptica / revisión, 2026','https://doi.org/10.3390/ani16020323'),('Presión / revisión sistemática, 2024','https://doi.org/10.3390/ani14233445')]:
  y=b.para(50,y+9,'<b>'+title+'</b><br/><link href="'+url+'" color="'+TEAL+'">'+url+'</link>',512,9.5,14)
 y=b.para(50,y+15,'Informe con límites y referencias: <link href="'+REPO_URL+'/blob/main/Guia/Evidencia_vibracion_y_bienestar.md" color="'+TEAL+'">Guia/Evidencia_vibracion_y_bienestar.md</link>. Búsqueda dirigida del 27 de octubre de 2026; no es una nueva revisión sistemática.',512,9.3,13)
 b.callout(y+15,'Qué está verificado','Los cinco programas compilaron con las bibliotecas del paquete. Esta edición cambia la enseñanza y los dibujos; no afirma pruebas físicas de hardware ni de bienestar animal.')
 b.finish()
 (public/'Fuentes_PDF/paginacion_guia.json').write_text(json.dumps(b.records,ensure_ascii=False,indent=2))
 print('Guía de taller:',b.n,'páginas')
