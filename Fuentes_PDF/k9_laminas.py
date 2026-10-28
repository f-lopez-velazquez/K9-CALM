"""Láminas vectoriales de electrónica K9 CALM: geometría, símbolos y redes.

Una misma geometría produce SVG editable, PNG de revisión y figuras vectoriales
para ReportLab. Coordenadas en puntos al tamaño de impresión de 512 pt.
"""
from pathlib import Path
import math,json
from reportlab.graphics.shapes import Drawing,Line,Rect,Circle,Polygon,PolyLine,String
from reportlab.graphics import renderSVG,renderPDF
from reportlab.lib.colors import HexColor,Color
from reportlab.pdfbase.pdfmetrics import stringWidth
NAVY='#12334d';TEAL='#087f99';WIRE='#087f99';GRAY='#607784';LIGHT='#d9e4e9';PALE='#f2f6f8';POWER='#a65327'
REGISTRY={}
class Plate:
 def __init__(self,w=512,h=220):
  self.w=w;self.h=h;self.d=Drawing(w,h);self.text_boxes=[]
 def line(self,x,y,x2,y2,c=NAVY,width=1,dash=None):
  self.d.add(Line(x,self.h-y,x2,self.h-y2,strokeColor=HexColor(c),strokeWidth=width,strokeDashArray=dash))
 def path(self,pts,c=WIRE,width=1.2,dash=None):
  self.d.add(PolyLine([v for x,y in pts for v in (x,self.h-y)],strokeColor=HexColor(c),strokeWidth=width,fillColor=None,strokeDashArray=dash))
 def rect(self,x,y,w,h,fill=None,stroke=LIGHT,r=0,width=.8):
  self.d.add(Rect(x,self.h-y-h,w,h,rx=r,ry=r,fillColor=HexColor(fill) if fill else None,strokeColor=HexColor(stroke) if stroke else None,strokeWidth=width))
 def circle(self,x,y,r=2,fill=WIRE,stroke=None,width=.8):
  self.d.add(Circle(x,self.h-y,r,fillColor=HexColor(fill) if fill else None,strokeColor=HexColor(stroke) if stroke else None,strokeWidth=width))
 def poly(self,pts,fill=None,stroke=NAVY,width=1):
  self.d.add(Polygon([v for x,y in pts for v in (x,self.h-y)],fillColor=HexColor(fill) if fill else None,strokeColor=HexColor(stroke) if stroke else None,strokeWidth=width))
 def text(self,x,y,t,size=9,c=NAVY,bold=False,anchor='start'):
  t=str(t);font='Helvetica-Bold' if bold else 'Helvetica'
  self.d.add(String(x,self.h-y,t,fontName=font,fontSize=size,fillColor=HexColor(c),textAnchor=anchor))
  wid=stringWidth(t,font,size);left=x-(wid if anchor=='end' else wid/2 if anchor=='middle' else 0)
  self.text_boxes.append([round(left,2),round(y-size,2),round(left+wid,2),round(y+2,2),t])
 def arrow(self,x,y,x2,y2,c=TEAL,width=1.1,head=5):
  self.line(x,y,x2,y2,c,width);a=math.atan2(y2-y,x2-x)
  self.poly([(x2,y2),(x2-head*math.cos(a-.5),y2-head*math.sin(a-.5)),(x2-head*math.cos(a+.5),y2-head*math.sin(a+.5))],c,c,width=.3)
 def ground(self,x,y,label=True):
  self.line(x,y,x,y+6);self.line(x-8,y+6,x+8,y+6);self.line(x-5,y+9,x+5,y+9);self.line(x-2,y+12,x+2,y+12)
  if label:self.text(x,y+25,'GND',8,c=GRAY,anchor='middle')
 def supply(self,x,y,label='3V3'):
  self.line(x,y,x,y-10,POWER);self.poly([(x-4,y-10),(x,y-16),(x+4,y-10)],None,POWER)
  self.text(x,y-21,label,9,POWER,True,anchor='middle')
 def resistor(self,x,y,length=50,vertical=False,ref='R1',value='330 ohm',label_side=1):
  if vertical:
   self.line(x,y,x,y+12);self.rect(x-5,y+12,10,length-24,stroke=NAVY,width=1);self.line(x,y+length-12,x,y+length)
   self.text(x+12*label_side,y+length/2-3,ref,8,bold=True,anchor='start' if label_side>0 else 'end');self.text(x+12*label_side,y+length/2+10,value,8,anchor='start' if label_side>0 else 'end')
  else:
   self.line(x,y,x+12,y);self.rect(x+12,y-5,length-24,10,stroke=NAVY,width=1);self.line(x+length-12,y,x+length,y)
   self.text(x+length/2,y-20,ref,8,bold=True,anchor='middle');self.text(x+length/2,y-9,value,8,anchor='middle')
 def capacitor(self,x,y,ref='C1',value='100 nF',length=44,side=1):
  a=y+length/2-3;b=y+length/2+3
  self.line(x,y,x,a);self.line(x-9,a,x+9,a);self.line(x-9,b,x+9,b);self.line(x,b,x,y+length)
  self.text(x+14*side,a-2,ref,8,bold=True,anchor='start' if side>0 else 'end');self.text(x+14*side,b+10,value,8,anchor='start' if side>0 else 'end')
 def diode(self,x,y,vertical=True,ref='D1',led=False,up=False):
  # The triangle points toward the cathode bar. Conventional LED/diodo symbol.
  if vertical:
   self.line(x,y,x,y+14);self.poly([(x-8,y+14),(x+8,y+14),(x,y+29)],None,NAVY);self.line(x-9,y+30,x+9,y+30);self.line(x,y+30,x,y+45)
   if led:
    self.arrow(x+11,y+16,x+22,y+5,head=3);self.arrow(x+16,y+23,x+27,y+12,head=3)
   self.text(x+34,y+18,ref,8,bold=True);self.text(x+34,y+31,'LED rojo' if led else 'Diodo',8)
  else:
   self.line(x,y,x+13,y);self.poly([(x+13,y-8),(x+13,y+8),(x+29,y)],None,NAVY);self.line(x+30,y-9,x+30,y+9);self.line(x+30,y,x+44,y)
   self.text(x+22,y-24,ref,8,bold=True,anchor='middle');self.text(x+22,y-13,'LED rojo' if led else 'Schottky',8,anchor='middle')
 def module(self,x,y,w,h,title,sub=None):
  self.rect(x,y,w,h,fill='#ffffff',stroke=NAVY,width=1.2)
  self.rect(x,y,w,30,fill=PALE,stroke=None);self.line(x,y+30,x+w,y+30,LIGHT,.7)
  self.text(x+10,y+19,title,10,bold=True)
  if sub:self.text(x+10,y+h-10,sub,8,GRAY)
 def pin(self,x,y,label,side='left',color=WIRE,length=22):
  if side=='left':self.line(x-length,y,x,y,color,1.2);self.text(x+7,y+3,label,9)
  else:self.line(x,y,x+length,y,color,1.2);self.text(x-7,y+3,label,9,anchor='end')
 def note(self,x,y,num,title,body):
  self.circle(x+9,y+8,9,fill=PALE);self.text(x+9,y+11,num,8,bold=True,anchor='middle')
  self.text(x+27,y+5,title,9,bold=True)
  for i,t in enumerate(body):self.text(x+27,y+18+i*12,t,8.3,GRAY)
 def save(self,name,folder,temp):
  REGISTRY[name]=self.d;folder.mkdir(parents=True,exist_ok=True);temp.mkdir(parents=True,exist_ok=True)
  renderSVG.drawToFile(self.d,str(folder/(name+'.svg')))
  intermediate=temp/(name+'.pdf');renderPDF.drawToFile(self.d,str(intermediate))
  import pymupdf as fitz
  doc=fitz.open(intermediate);doc[0].get_pixmap(matrix=fitz.Matrix(3,3)).save(folder/(name+'.png'))
  errors=[b for b in self.text_boxes if b[0]<-1 or b[1]<-1 or b[2]>self.w+1 or b[3]>self.h+1]
  if errors:raise ValueError((name,errors))
  return {'nombre':name,'ancho_pt':self.w,'alto_pt':self.h,'textos':self.text_boxes}

def h1():
 p=Plate(h=212)
 p.module(12,40,112,138,'U1 / ESP32-C3','USB · 3.3 V lógicos')
 p.pin(124,88,'GPIO10','right');p.pin(124,145,'GPIO3','right')
 p.path([(146,88),(175,88)]);p.resistor(175,88,60,ref='R3',value='330 ohm');p.path([(235,88),(283,88)])
 p.diode(283,88,ref='D2',led=True);p.ground(283,133)
 p.text(282,72,'A',8,GRAY);p.text(272,126,'K',8,GRAY)
 p.path([(146,145),(185,145),(185,179),(400,179),(400,129)])
 # Internal resistor and input node, open switch to ground.
 p.circle(400,129,2.3);p.resistor(400,75,54,True,'Rint','pull-up');p.supply(400,75,'3V3 interna')
 p.path([(400,129),(454,129),(454,141)])
 p.circle(454,143,2,fill='#ffffff',stroke=NAVY);p.circle(454,161,2,fill='#ffffff',stroke=NAVY)
 p.line(454,143,466,157);p.line(454,163,454,174);p.ground(454,174,False)
 p.text(477,174,'S2',8,bold=True)
 p.text(397,196,'S2 abierto: HIGH / cerrado: LOW',8,anchor='middle')
 p.text(12,203,'La resistencia interna se activa con INPUT_PULLUP; no se compra ni se cablea.',8.5,GRAY)
 return p

def imu():
 p=Plate(h=206)
 p.module(12,45,126,136,'U1 / ESP32-C3')
 p.module(328,45,168,136,'U2 / GY-521')
 for y,a,b,c in [(90,'3V3','VCC',POWER),(116,'GPIO4','SDA',WIRE),(142,'GPIO5','SCL',WIRE)]:
  p.pin(138,y,a,'right',c);p.path([(160,y),(306,y)],c);p.pin(328,y,b,'left',c)
 p.text(228,78,'Alimentación',8,POWER,anchor='middle')
 p.text(228,108,'DATOS',8,GRAY,anchor='middle');p.text(228,134,'RELOJ',8,GRAY,anchor='middle')
 # Common ground and fixed address via explicit named net terminals.
 p.text(28,172,'GND',8,GRAY);p.path([(53,181),(53,185)]);p.ground(53,185,False)
 p.text(366,170,'GND',8,GRAY,anchor='middle');p.text(454,170,'AD0',8,GRAY,anchor='middle')
 p.path([(366,181),(366,191),(454,191),(454,181)],GRAY,.8);p.circle(410,191,2,GRAY);p.ground(410,191,False)
 p.text(12,28,'SDA y SCL necesitan pull-ups a 3V3; comprueba los del módulo.',9,bold=True)
 return p

def microphone():
 p=Plate(h=230)
 p.module(12,43,132,158,'U1 / ESP32-C3')
 p.module(330,43,166,158,'U3 / INMP441')
 for y,a,b,c in [(86,'3V3','VDD',POWER),(111,'GPIO6','SCK',WIRE),(136,'GPIO7','WS',WIRE),(161,'GPIO1','SD',WIRE)]:
  p.pin(144,y,a,'right',c);p.path([(166,y),(308,y)],c);p.pin(330,y,b,'left',c)
 p.text(230,104,'BCLK',8,GRAY,anchor='middle');p.text(230,129,'WS',8,GRAY,anchor='middle');p.arrow(254,155,218,155,head=4)
 p.circle(270,161,2);p.resistor(270,161,44,True,'R4','100 kohm');p.ground(270,205,False)
 p.text(28,190,'GND',8,GRAY);p.line(53,201,53,205);p.ground(53,205,False)
 p.text(372,190,'GND',8,GRAY,anchor='middle');p.text(456,190,'L/R',8,GRAY,anchor='middle')
 p.path([(372,201),(372,211),(456,211),(456,201)],GRAY,.8);p.circle(414,211,2,GRAY);p.ground(414,211,False)
 p.text(12,25,'Todos comparten GND. L/R a GND selecciona el canal izquierdo.',9,bold=True)
 return p

def divider(usb=True):
 p=Plate(h=204)
 p.text(20,23,'MEDIR VOLTAJE / ' + ('prueba por USB' if usb else 'entrada portátil validada'),10,bold=True)
 p.text(20,45,'R1 arriba · R2 abajo · el ADC mide el punto entre ambas.',9,GRAY)
 p.supply(108,92,'3V3' if usb else 'VENTRADA')
 p.resistor(108,92,48,True,'R1','150 kohm');p.circle(108,140,2.3)
 p.resistor(108,140,42,True,'R2','100 kohm');p.ground(108,182,False)
 p.path([(108,140),(232,140)]);p.circle(232,140,2.3)
 p.capacitor(232,140,'C2','100 nF',42);p.ground(232,182,False)
 p.path([(232,140),(352,140)])
 p.module(352,105,144,62,'U1 / ESP32-C3');p.pin(352,140,'GPIO0','left')
 p.text(348,79,'Vnodo = ' + ('1.32 V si 3V3 = 3.30 V' if usb else 'Ventrada x 0.4'),9,bold=True,anchor='middle')
 p.text(20,201,'La tensión reconstruida es Vnodo x 2.50. No confundirla con un porcentaje de carga.',8.3,GRAY)
 return p

def integrated():
 p=Plate(h=390)
 p.text(12,15,'ESQUEMA POR REDES / etiquetas iguales significan una misma conexión',9,bold=True)
 p.module(15,29,145,255,'U1 / ESP32-C3')
 rows=[(75,'3V3','3V3',POWER),(95,'GND','GND',GRAY),(123,'GPIO4','SDA4',WIRE),(143,'GPIO5','SCL5',WIRE),(171,'GPIO6','BCLK6',WIRE),(191,'GPIO7','WS7',WIRE),(211,'GPIO1','SD1',WIRE),(239,'GPIO10','LED10',WIRE),(264,'GPIO3','BOT3',WIRE)]
 for y,pin,net,col in rows:
  p.pin(160,y,pin,'right',col,length=12);p.line(172,y,190,y,col);p.text(194,y+3,net,8.5,col)
 p.module(281,29,213,112,'U2 / GY-521')
 for i,(a,b,c) in enumerate([('VCC','3V3',POWER),('SDA','SDA4',WIRE),('SCL','SCL5',WIRE),('GND','GND',GRAY),('AD0','GND',GRAY)]):
  y=72+i*14;p.text(294,y,a,8.5);p.line(353,y-3,397,y-3,c);p.text(407,y,b,8.5,c)
 p.module(281,158,213,126,'U3 / INMP441')
 for i,(a,b,c) in enumerate([('VDD','3V3',POWER),('SCK','BCLK6',WIRE),('WS','WS7',WIRE),('SD','SD1',WIRE),('GND','GND',GRAY),('L/R','GND',GRAY)]):
  y=200+i*14;p.text(294,y,a,8.5);p.line(353,y-3,397,y-3,c);p.text(407,y,b,8.5,c)
 p.line(12,295,500,295,LIGHT,.7)
 p.text(12,330,'LED10',8.5,WIRE,bold=True);p.path([(53,327),(70,327)])
 p.resistor(70,327,55,ref='R3',value='330 ohm');p.line(125,327,151,327)
 p.diode(151,327,vertical=False,ref='D2',led=True);p.arrow(196,316,205,307,head=3);p.arrow(203,319,212,310,head=3)
 p.line(195,327,231,327);p.ground(231,327,False)
 p.text(12,362,'BOT3',8.5,WIRE,bold=True);p.line(47,359,70,359);p.circle(70,359,2,fill='#ffffff',stroke=NAVY);p.circle(95,359,2,fill='#ffffff',stroke=NAVY);p.line(72,357,92,349);p.line(97,359,118,359);p.ground(118,359,False);p.text(148,366,'S2 / pull-up interna en GPIO3',8,GRAY)
 p.text(333,330,'SD1',8.5,WIRE,bold=True);p.line(357,327,379,327);p.resistor(379,327,53,ref='R4',value='100 kohm');p.line(432,327,456,327);p.ground(456,327,False)
 p.text(12,387,'VCC/VDD a 3V3. Desacoplo de 100 nF junto a cada sensor si el módulo no lo incluye.',8,GRAY)
 return p

def pinout(back=False):
 p=Plate(h=258)
 p.text(12,18,'MAPA DE TERMINALES / USB arriba · vista de componentes',10,bold=True)
 p.rect(198,46,116,190,fill=PALE,stroke=NAVY,width=1.1,r=5)
 p.rect(236,35,40,25,fill='#e0e6ea',stroke=GRAY,r=4);p.rect(242,36,28,8,fill='#ffffff',stroke=GRAY,r=2)
 p.text(256,79,'USB-C',9,bold=True,anchor='middle');p.text(256,114,'ESP32-C3',10,bold=True,anchor='middle');p.text(256,131,'SuperMini',9,anchor='middle')
 p.text(256,180,'16 terminales',8,GRAY,anchor='middle');p.text(256,197,'vista de referencia',8,GRAY,anchor='middle')
 left=[('5V','No conectar en USB'),('GND','Tierra común'),('3V3','Alimentar sensores'),('4','SDA / MPU6050'),('3','Botón a GND'),('2','Libre / arranque'),('1','SD / INMP441'),('0','ADC / divisor')]
 right=[('5','SCL / MPU6050'),('6','BCLK / INMP441'),('7','WS / INMP441'),('8','Libre / arranque'),('9','Libre / BOOT'),('10','LED con 330 ohm'),('20','Libre'),('21','Libre')]
 for i,((a,b),(c,d)) in enumerate(zip(left,right)):
  yy=89+i*19
  p.circle(202,yy,3,fill='#ffffff',stroke=GRAY);p.circle(310,yy,3,fill='#ffffff',stroke=GRAY)
  p.text(212,yy+3,a,8);p.text(300,yy+3,c,8,anchor='end')
  p.path([(199,yy),(181,yy)],GRAY,.7);p.text(173,yy+3,b,8.5,anchor='end')
  p.path([(313,yy),(331,yy)],GRAY,.7);p.text(339,yy+3,d,8.5)
 p.text(12,255,'Verifica la serigrafía de tu placa. Es un mapa de pines, no una reproducción del PCB.',8.4,GRAY)
 return p

def faces():
 p=Plate(h=225)
 for k,back in enumerate([False,True]):
  x=83+k*270;p.rect(x,33,76,164,fill=PALE,stroke=NAVY,width=1.2,r=4);p.rect(x+21,22,34,23,fill='#e0e6ea',stroke=GRAY,r=3)
  l=['5V','G','3V3','4','3','2','1','0'];r=['5','6','7','8','9','10','20','21']
  if back:l,r=r,l
  for i,(a,b) in enumerate(zip(l,r)):
   y=61+i*17;p.circle(x+7,y,2.5,fill='#ffffff',stroke=GRAY);p.circle(x+69,y,2.5,fill='#ffffff',stroke=GRAY);p.text(x-7,y+3,a,8.5,anchor='end');p.text(x+83,y+3,b,8.5)
  p.text(x+38,124,'ATRÁS' if back else 'FRENTE',9,bold=True,anchor='middle');p.text(x+38,218,'Las columnas se reflejan' if back else 'USB arriba',9,anchor='middle')
 p.text(256,14,'Orientación de lectura de los conectores',10,bold=True,anchor='middle')
 return p

def signals(kind):
 p=Plate(h=207)
 p.text(12,18,'DATOS DE EJEMPLO / simulados, no mediciones de un animal',9,bold=True)
 left,right,top,bottom=47,492,44,158
 for k in range(5):
  y=top+k*(bottom-top)/4;p.line(left,y,right,y,LIGHT,.5)
 p.line(left,top,left,bottom,GRAY,.8);p.line(left,bottom,right,bottom,GRAY,.8)
 if kind=='motion':
  ymax=2.4
  pts=[]
  for i in range(220):
   t=6*i/219;v=.13+.045*math.sin(t*13)+(1.55*(.5+.5*math.sin(t*18)) if 2.7<t<4.1 else 0)
   pts.append((left+(right-left)*t/6,bottom-(bottom-top)*v/ymax))
  p.path(pts,width=1.4);p.text(15,34,'m/s²',8)
  for k in range(5):p.text(39,top+4+k*(bottom-top)/4,f'{ymax*(4-k)/4:.1f}',8,anchor='end')
  for v in [0,2,4,6]:p.text(left+(right-left)*v/6,bottom+15,v,8,anchor='middle')
  xx=left+(right-left)*2.4/6;p.line(xx,top,xx,bottom,POWER,.9,[3,2]);p.text(xx+5,top+10,'sonido',8,POWER)
  p.text(258,196,'Tiempo (s) · antes del sonido / observación posterior',8.5,GRAY,anchor='middle')
 elif kind=='fft':
  energies=[math.exp(-((k-8)/3)**2)+.53*math.exp(-((k-40)/10)**2) for k in range(1,65)]
  for k in range(1,65):
   h=(bottom-top)*energies[k-1]/max(energies)
   x=left+k*(right-left)/65;p.rect(x,bottom-h,3,h,fill=TEAL,stroke=None)
  for value in [0,.5,1]:p.text(39,bottom-(bottom-top)*value+3,f'{value:.1f}',8,anchor='end')
  for v in [0,2000,4000,6000,8000]:p.text(left+(right-left)*v/8000,bottom+15,v,8,anchor='middle')
  p.text(260,196,'Frecuencia (Hz) · barras = energía relativa',8.5,GRAY,anchor='middle')
 else:
  # All examples share labelled amplitude and time axes; no fabricated signatures.
  pts=[]
  for i in range(450):
   t=i/449;x=left+(right-left)*t;v=.04*math.sin(160*t)+(math.sin(t*240)*math.exp(-(t-.23)*12)*.85 if t>.23 else 0);y=(top+bottom)/2-(bottom-top)*v/2;pts.append((x,y))
  p.path(pts,width=1.1);p.text(39,top+3,'+1',8,anchor='end');p.text(39,(top+bottom)/2+3,'0',8,anchor='end');p.text(39,bottom+3,'-1',8,anchor='end')
  for v in [0,.25,.5,.75,1]:p.text(left+(right-left)*v,bottom+15,f'{v:.2f}',8,anchor='middle')
  p.text(256,196,'Tiempo (s) · amplitud digital normalizada, no dB',8.5,GRAY,anchor='middle')
 return p

def states(loop=False):
 p=Plate(h=145)
 labels=[('OBSERVAR','2 s de historia'),('POSTERIOR','1.5 s de actividad'),('REPOSO','2 s sin repetir')] if not loop else [('LEER','Botón y sensores'),('COMPARAR','Evento y alimentación'),('INFORMAR','LED + BLE + Serial')]
 for i,(a,b) in enumerate(labels):
  x=12+i*174;p.rect(x,35,140,55,fill=PALE,stroke=NAVY,width=.9,r=3);p.text(x+70,56,a,9,bold=True,anchor='middle');p.text(x+70,73,b,8.3,GRAY,anchor='middle')
  if i<2:
   p.arrow(x+140,62,x+174,62)
   if not loop:p.text(x+157,48,'impulso' if i==0 else 'evaluar',7.5,TEAL,anchor='middle')
 p.path([(430,90),(430,111),(82,111),(82,90)],GRAY,.8);p.arrow(82,107,82,90,GRAY,head=4)
 p.text(256,135,'Cada vuelta atiende el trabajo pendiente sin usar delay().' if loop else 'Sin impulso, sigue observando. El modo manual cancela la comparación.',8.5,GRAY,anchor='middle')
 return p

def system():
 p=Plate(h=145)
 for y,title,sub in [(35,'SONIDO','INMP441 / I2S'),(100,'MOVIMIENTO','MPU6050 / I2C')]:
  p.rect(12,y-18,142,42,fill=PALE,stroke=LIGHT);p.text(24,y-2,title,9,bold=True);p.text(24,y+13,sub,8,GRAY)
 p.path([(154,39),(185,39),(185,73),(218,73)]);p.path([(154,104),(185,104),(185,73)]);p.circle(185,73,2)
 p.rect(218,49,132,49,fill=PALE,stroke=NAVY);p.text(284,68,'ESP32-C3',10,bold=True,anchor='middle');p.text(284,83,'Compara los datos',8,anchor='middle');p.arrow(350,73,381,73)
 p.rect(381,49,119,49,fill=PALE,stroke=NAVY);p.text(440,68,'LED + BLE',10,bold=True,anchor='middle');p.text(440,83,'Muestra un evento',8,anchor='middle')
 p.text(12,140,'Un evento acústico y un cambio de actividad no equivalen a un diagnóstico de miedo.',8.5,GRAY)
 return p

def power():
 p=Plate(h=250)
 p.text(12,18,'ALIMENTACIÓN PORTÁTIL / validar el LDO de la placa antes de conectar pilas',9,bold=True)
 p.rect(12,49,70,78,stroke=NAVY);p.text(47,71,'B1',9,bold=True,anchor='middle');p.text(47,87,'3 x AAA',9,anchor='middle');p.text(47,104,'alcalinas',8,anchor='middle')
 p.path([(82,69),(104,69)],POWER);p.resistor(104,69,50,ref='F1',value='PTC 0.5 A');p.line(154,69,178,69,POWER);p.diode(178,69,vertical=False,ref='D1');p.line(222,69,250,69,POWER)
 p.circle(250,69,2,fill='#ffffff',stroke=NAVY);p.circle(274,69,2,fill='#ffffff',stroke=NAVY);p.line(252,67,270,58);p.text(262,45,'S1',8,bold=True)
 p.path([(276,69),(346,69),(346,128)],POWER);p.module(368,89,132,79,'U1 / SuperMini');p.pin(368,128,'5V / entrada','left',POWER);p.text(380,151,'LDO -> 3V3',8,GRAY)
 p.circle(304,69,2,POWER);p.path([(304,69),(304,97),(196,97),(196,112)],POWER)
 p.resistor(196,112,43,True,'R1','150 kohm',label_side=-1);p.circle(196,155,2)
 p.resistor(196,155,43,True,'R2','100 kohm',label_side=-1)
 p.path([(196,155),(246,155)]);p.circle(246,155,2);p.capacitor(246,155,'C2','100 nF',43)
 p.path([(246,155),(282,155)]);p.text(249,144,'GPIO0',8.5)
 p.line(304,97,304,119);p.capacitor(304,119,'C1','100 uF',79);p.text(289,149,'+',10,POWER)
 p.path([(82,110),(100,110),(100,214),(434,214),(434,168)],GRAY)
 for x in [196,246,304]:p.line(x,198,x,214,GRAY);p.circle(x,214,2,GRAY)
 p.ground(100,214,False);p.text(399,185,'GND',8,GRAY);p.text(366,61,'Ventrada',8,POWER)
 p.text(12,247,'Sin USB. El divisor toma Ventrada después de F1, D1 y S1; C1 lleva + hacia Ventrada.',8.3,GRAY)
 return p

def motor():
 p=Plate(h=239)
 p.text(12,18,'MOTOR OPCIONAL / únicamente banco o peluche',9,bold=True)
 p.supply(342,70,'+3 V regulados externos');p.circle(342,90,16,fill='#ffffff',stroke=NAVY);p.text(342,94,'M',12,bold=True,anchor='middle');p.line(342,70,342,74);p.line(342,106,342,130);p.circle(342,130,2)
 # NMOS low-side with insulated gate, D/S labels, pulldown and flyback diode.
 p.line(342,130,342,146);p.line(342,146,326,146);p.line(326,146,326,163);p.line(326,177,326,194);p.line(326,194,342,194);p.line(342,194,342,211)
 p.line(317,146,317,194);p.line(309,151,309,189);p.line(277,170,309,170)
 p.line(326,170,342,170);p.line(342,170,342,194);p.arrow(339,183,328,183,NAVY,head=3)
 p.text(357,159,'Q1 / NMOS',8.5,bold=True);p.text(357,172,'Logic-level 3.3 V',8.5)
 p.text(338,141,'D',8);p.text(339,206,'S',8);p.text(294,161,'G',8)
 p.text(12,174,'GPIO20',9,bold=True);p.line(65,170,100,170);p.resistor(100,170,60,ref='R5',value='100 ohm');p.line(160,170,277,170);p.circle(226,170,2)
 p.resistor(226,170,42,True,'R6','100 kohm');p.line(226,212,226,218);p.line(226,218,342,218);p.line(342,211,342,218);p.ground(342,218,False)
 # Flyback: cathode at upper rail, anode at drain (triangle points up).
 p.path([(342,60),(454,60),(454,80)]);p.circle(342,60,2);p.line(454,80,454,92);p.line(446,92,462,92);p.poly([(454,94),(446,108),(462,108)],None,NAVY);p.line(454,108,454,130);p.line(454,130,342,130)
 p.text(470,99,'D3',8,bold=True);p.text(470,112,'banda +',7.5)
 p.text(12,233,'Fuente separada de 3 V y GND común. No conectar el motor al GPIO ni al pin 3V3.',8,GRAY)
 return p

def battery():
 p=Plate(h=180)
 p.rect(18,38,178,102,fill=PALE,stroke=NAVY,r=3)
 for i in range(3):
  y=53+i*26;p.rect(31,y,149,18,fill='#ffffff',stroke=GRAY,r=3);p.text(44,y+12,'AAA',8,bold=True);p.text(170,y+12,'+' if i%2==0 else '-',10,anchor='middle')
 p.text(107,157,'B1 / 3 celdas en serie',9,bold=True,anchor='middle')
 p.path([(196,61),(237,61)],POWER);p.text(216,48,'+',9,POWER);p.resistor(237,61,52,ref='F1',value='PTC');p.line(289,61,315,61);p.diode(315,61,vertical=False,ref='D2');p.line(359,61,395,61);p.circle(395,61,2,fill='#ffffff',stroke=NAVY);p.circle(420,61,2,fill='#ffffff',stroke=NAVY);p.line(397,59,416,49);p.line(422,61,492,61);p.text(406,35,'S2',8,bold=True);p.text(492,46,'Ventrada',8,anchor='end')
 p.path([(196,119),(492,119)],GRAY);p.text(492,110,'GND',8,anchor='end');p.text(229,151,'Conector polarizado + tapa + aislamiento',8.5)
 p.text(12,177,'Representación de conexiones. No recargar pilas alcalinas ni conectar USB y pack a la vez.',8.5,GRAY)
 return p

def sensors():
 p=Plate(h=210)
 p.module(12,32,230,149,'U2 / MPU6050','Aceleración y velocidad de giro')
 p.module(270,32,230,149,'U3 / INMP441','Audio digital mediante I2S')
 p.rect(35,83,55,55,fill=PALE,stroke=GRAY);p.circle(62,110,3,fill=TEAL);p.arrow(62,110,113,110);p.arrow(62,110,62,64);p.text(116,114,'X',9,bold=True);p.text(69,72,'Y',9,bold=True);p.text(98,147,'Z sale del plano',8,GRAY)
 p.circle(319,109,20,fill=PALE,stroke=GRAY);p.circle(319,109,4,fill=NAVY);p.text(354,96,'SCK / reloj de bits',8.5);p.text(354,114,'WS / canal',8.5);p.text(354,132,'SD / datos',8.5)
 p.text(256,204,'Ejes y orden físico: coteja la serigrafía del módulo comprado.',8.5,GRAY,anchor='middle')
 return p

def ide():
 p=Plate(h=174)
 p.text(12,18,'ARDUINO IDE / recorrido de trabajo',10,bold=True)
 for i,(a,b,c) in enumerate([('1 / VERIFICAR','Compila el programa','Revisa errores'),('2 / SUBIR','Lo guarda en el C3','Placa + puerto correctos'),('3 / MONITOR','Lee la salida del programa','Selecciona 115200')]):
  x=12+174*i;p.rect(x,43,140,88,fill=PALE,stroke=LIGHT,r=3);p.text(x+11,63,a,9,bold=True);p.text(x+11,86,b,8.3);p.text(x+11,106,c,8.3,GRAY)
  if i<2:p.arrow(x+140,86,x+174,86)
 p.text(12,162,'Es un mapa de acciones; los iconos y menús pueden variar con idioma y versión.',8.5,GRAY)
 return p

def mount():
 p=Plate(h=195)
 p.rect(20,35,472,128,fill=PALE,stroke=NAVY,r=5)
 for x,y,w,h,ref,sub in [(36,53,100,90,'B1','Pack separado'),(166,53,130,90,'U1','ESP32-C3'),(326,53,150,40,'U2 / GY-521','Fijación rígida'),(326,106,150,40,'U3 / INMP441','Puerto libre')]:
  p.rect(x,y,w,h,fill='#ffffff',stroke=GRAY,r=2);p.text(x+w/2,y+17,ref,9,bold=True,anchor='middle');p.text(x+w/2,y+31,sub,8,anchor='middle')
 p.text(256,18,'DISTRIBUCIÓN MECÁNICA / propuesta sobre una maqueta',9,bold=True,anchor='middle');p.text(256,186,'Caja aislante, alivio de tensión y antena libre. No es una colocación terapéutica.',8.5,GRAY,anchor='middle')
 return p

def generate(folder,temp):
 assets={
 '01_pinout':pinout,'02_caras':faces,'03_sensores':sensors,'04_alimentacion':power,
 '05_motor':motor,'06_montaje':mount,'07_sistema':system,'08_estados':states,
 '08_flujo':lambda:states(True),'09_sonidos':lambda:signals('audio'),
 '10_movimiento':lambda:signals('motion'),'11_ide':ide,'12_fft':lambda:signals('fft'),
 '13_led_boton':h1,'14_laboratorio':integrated,'15_portapilas':battery,
 '17_divisor_usb':divider,'H1_conexiones':h1,'H2_conexiones':imu,'H3_conexiones':microphone,
 'H4_conexiones':lambda:divider(False),'H5_conexiones':integrated,
 '18_lectura_plano':legend,'19_tiempo':timing,'20_umbral':threshold,
 }
 report=[]
 for name,f in assets.items():report.append(f().save(name,Path(folder),Path(temp)))
 (Path(folder)/'geometria_y_textos.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 return REGISTRY

def legend():
 p=Plate(h=148)
 p.text(12,17,'CÓMO LEER EL PLANO / símbolos que usarás en las prácticas',10,bold=True)
 p.line(20,58,70,58,WIRE);p.text(85,57,'Cable',9,bold=True);p.text(85,70,'Une dos terminales.',8.5,GRAY)
 p.path([(220,58),(266,58)]);p.path([(243,44),(243,75)]);p.circle(243,58,2.5);p.text(282,57,'Punto',9,bold=True);p.text(282,70,'Aquí sí hay unión.',8.5,GRAY)
 p.ground(435,48,False);p.text(457,57,'GND',9,bold=True);p.text(405,85,'Todos los GND se unen.',8.3,GRAY)
 p.resistor(20,116,50,ref='',value='');p.text(85,112,'Resistencia',9,bold=True);p.text(85,125,'Su valor se indica al lado.',8.5,GRAY)
 p.circle(221,116,2,fill='#ffffff',stroke=NAVY);p.circle(244,116,2,fill='#ffffff',stroke=NAVY);p.line(223,114,242,103);p.text(260,112,'Botón abierto',9,bold=True);p.text(260,125,'Al pulsarlo, une ambos lados.',8.5,GRAY)
 return p

def threshold():
 p=Plate(h=109)
 p.text(12,14,'MISMA LECTURA / cambia el umbral, no el movimiento',9,bold=True)
 for i,(threshold,answer,on) in enumerate([('0.70','NO',False),('0.30','SÍ',True)]):
  y=42+47*i
  p.text(13,y+4,'act = 0.50',9,bold=True);p.arrow(81,y,121,y)
  p.rect(121,y-13,168,26,fill=PALE,stroke=LIGHT,r=3);p.text(205,y+4,'¿0.50 > '+threshold+'?',9,anchor='middle')
  p.arrow(289,y,338,y);p.text(312,y-8,answer,8,bold=True,anchor='middle')
  p.circle(357,y,7,fill=TEAL if on else '#ffffff',stroke=TEAL,width=1.2)
  p.text(375,y+4,'LED encendido' if on else 'LED apagado',9)
 return p

def timing():
 p=Plate(h=115)
 p.text(12,14,'500 ms ENTRE CAMBIOS / un ciclo completo dura 1000 ms',9,bold=True)
 x0,x1=80,490;yhigh,ylow=48,77
 for k in range(5):
  x=x0+(x1-x0)*k/4;p.line(x,34,x,84,LIGHT,.6);p.text(x,103,str(k*500),8,anchor='middle')
 p.text(12,51,'Encendido',8);p.text(12,80,'Apagado',8)
 pts=[(x0,ylow)]
 for k in range(4):
  end=x0+(x1-x0)*(k+1)/4;y=ylow if k%2==0 else yhigh
  pts.extend([(end,y),(end,yhigh if k%2==0 else ylow)])
 p.path(pts,width=1.6)
 return p
