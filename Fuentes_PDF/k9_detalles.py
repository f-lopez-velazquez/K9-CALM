"""Laminas originales por terminal: componentes y circuito integrado."""
def details(SVG,board):
 s=SVG(1000,370);s.text(25,33,'H1 | Componentes reales, conexiones identificadas',24)
 # Axial resistor and explicit two-terminal LED (symbol plus illustrated lens)
 s.text(35,82,'GPIO10',19);s.line(35,110,150,110,'#d17b20');s.rect(150,90,165,40,'#e3c78f');
 for x,c in [(180,'#d57c28'),(210,'#d57c28'),(240,'#854b1e'),(283,'#c2a245')]:s.rect(x,90,8,40,c,c,r=0)
 s.text(232,162,'330 ohm',18,anchor='middle');s.line(315,110,420,110,'#d17b20')
 s.s.append('<path d="M 420 90 Q 450 45 480 90 L 480 125 L 420 125 Z" fill="#dc5a51" stroke="#8e3c37" stroke-width="3"/>')
 s.line(420,110,420,220,'#956f4b');s.line(480,125,480,220,'#956f4b');s.line(480,220,550,220);s.text(558,226,'GND',18)
 s.text(345,249,'Anodo (+)',18);s.text(478,249,'Catodo (-)',18);s.text(345,278,'La pata larga suele ser +; confirmar.',16)
 s.text(635,82,'GPIO3',19);s.line(635,110,700,110,'#9163b0');s.circle(700,110,5);s.line(700,110,758,76,'#9163b0');s.circle(775,110,5);s.line(775,110,930,110);s.text(880,143,'GND',18)
 s.rect(715,177,90,60,'#353b44');s.circle(760,207,17,'#b1bac4');s.text(638,273,'Pulsador: abierto sin presionar.',17);s.text(638,300,'La entrada usa pull-up interno.',17)
 s.text(25,346,'Circuito equivalente: GPIO10 -> 330 ohm -> LED -> GND. GPIO3 -> pulsador -> GND.',18);s.save('13_led_boton')
 s=SVG(1200,710);s.text(25,35,'H5 | Circuito completo de laboratorio por redes etiquetadas',25)
 s.text(25,66,'USB como unica fuente. Etiquetas iguales = unidos; no representan una protoboard.',18)
 pins=board(s,290,170)
 roles={'5V':('LIBRE: sin pack','#da5757'),'GND':('GND','#344b59'),'3V3':('3V3','#da5757'),'4':('SDA4','#168fa6'),'3':('BOT3','#9368a3'),'2':('LIBRE','#89969c'),'1':('SD1','#258ec2'),'0':('ADC0 (opcional)','#d15d77'),'5':('SCL5','#21936d'),'6':('BCLK6','#cf9224'),'7':('WS7','#9961b7'),'8':('LIBRE','#89969c'),'9':('LIBRE','#89969c'),'10':('LED10','#da8026'),'20':('LIBRE','#89969c'),'21':('LIBRE','#89969c')}
 for pin,(x,y) in pins.items():
  a,c=roles[pin];left=x<400;end=x-75 if left else x+75
  s.line(x,y,end,y,c);s.circle(end,y,4,c);s.text(end-8 if left else end+8,y+5,a,17,c,'end' if left else 'start')
 # Endpoint blocks with pin labels on left and same net on the right. No fake module pin footprint.
 def module(x,y,title,rows):
  s.rect(x,y,470,50+len(rows)*35,'#edf4f7');s.text(x+235,y+30,title,20,anchor='middle')
  for i,(pin,net,col) in enumerate(rows):
   yy=y+60+i*35;s.text(x+20,yy+5,pin,18);s.line(x+105,yy,x+280,yy,col,3);s.circle(x+105,yy,4,col);s.text(x+295,yy+5,net,18,col)
 module(690,105,'GY-521 / MPU6050',[('VCC','3V3','#da5757'),('GND','GND','#344b59'),('SDA','SDA4','#168fa6'),('SCL','SCL5','#21936d'),('AD0','GND','#344b59')])
 module(690,365,'INMP441',[('VDD','3V3','#da5757'),('GND','GND','#344b59'),('SCK','BCLK6','#cf9224'),('WS','WS7','#9961b7'),('SD','SD1 + 100k a GND','#258ec2'),('L/R','GND','#344b59')])
 s.text(25,555,'LED10 -> 330 ohm -> anodo LED; catodo -> GND',18)
 s.text(25,590,'BOT3 -> pulsador normalmente abierto -> GND',18)
 s.text(25,625,'100nF entre 3V3 y GND cerca de cada sensor.',18)
 s.text(25,660,'ADC0: divisor H4; desconectado en USB normal.',18)
 s.text(25,697,'GY-521 XDA, XCL e INT libres. Pull-ups I2C solo a 3V3. Revisar continuidad sin energia.',18);s.save('14_laboratorio')
 s=SVG(1000,420);s.text(25,35,'Portapilas 3 AAA + interruptor: identificar polaridad',24)
 s.rect(70,75,430,245,'#343d48')
 for i in range(3):
  y=100+i*65;s.rect(100,y,330,45,'#d3d9dd');s.rect(430,y+12,12,20,'#c8b060');s.text(115,y+30,'-',23);s.text(400,y+30,'+',23);s.text(250,y+30,'AAA 1.5 V',19,anchor='middle')
 s.text(90,350,'En serie: las tensiones se suman.',18);s.text(90,380,'Medir polaridad real; no confiar solo en colores.',17)
 s.line(500,130,580,130,'#d45454');s.rect(580,95,150,70,'#eef4f6');s.text(655,125,'F1 + D1',20,anchor='middle');s.text(655,150,'Proteccion',15,anchor='middle');s.line(730,130,800,130,'#d45454')
 s.circle(800,130);s.line(800,130,855,95,'#d45454');s.circle(870,130);s.line(870,130,955,130,'#d45454');s.text(810,190,'S1 / SPST',20);s.text(785,230,'Al nodo Ventrada',18)
 s.line(500,280,955,280,'#344b59');s.text(795,308,'GND comun',19)
 s.text(545,365,'No es cargador. No recargar alcalinas.',18);s.text(545,395,'USB retirado al conectar el portapilas.',18);s.save('15_portapilas')

 s=SVG(1000,480);s.text(25,35,'K9 CALM | Concepto de pechera sobre un peluche',24)
 s.s.append('<defs><linearGradient id="tela" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2d6c5"/><stop offset="1" stop-color="#b9a48a"/></linearGradient><linearGradient id="caja" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#28627d"/><stop offset="1" stop-color="#15354c"/></linearGradient></defs>')
 # Silueta de peluche; costura intencional, no fotografia ni ensayo fisico.
 s.s.append('<path d="M 232 220 Q 145 195 124 135 Q 97 142 105 176 Q 133 236 210 268" fill="#d2bfa6" stroke="#a38b72" stroke-width="3"/>')
 s.s.append('<ellipse cx="420" cy="254" rx="212" ry="105" fill="#d2bfa6" stroke="#a38b72" stroke-width="3"/>')
 for x,y in [(290,285),(355,300),(510,292),(570,278)]:
  s.s.append(f'<path d="M {x} {y} Q {x-14} {y+51} {x-9} 382 Q {x+20} 405 {x+48} 382 L {x+35} {y}" fill="#d2bfa6" stroke="#a38b72" stroke-width="3"/>')
 s.s.append('<path d="M 567 220 Q 578 140 645 112 Q 707 80 752 128 L 763 170 L 819 187 Q 839 209 816 229 L 744 242 Q 704 292 626 267 Z" fill="#d2bfa6" stroke="#a38b72" stroke-width="3"/>')
 s.s.append('<path d="M 655 115 Q 608 140 616 221 Q 650 246 683 185 L 701 123" fill="#856c54" stroke="#705a45" stroke-width="3"/>')
 s.circle(739,159,8,'#29343c');s.circle(742,156,2,'white');s.rect(814,188,23,21,'#29343c',r=8)
 s.s.append('<path d="M 732 222 Q 777 238 806 220" fill="none" stroke="#7d6751" stroke-width="3"/>')
 s.s.append('<path d="M 235 245 Q 420 320 605 231" fill="none" stroke="#9c8d7c" stroke-width="2" stroke-dasharray="5,7"/>')
 # Bandas y caja colocadas sobre el peluche.
 s.s.append('<path d="M 347 160 Q 334 245 360 348" fill="none" stroke="#28566f" stroke-width="28"/>')
 s.s.append('<path d="M 581 177 Q 550 255 589 316" fill="none" stroke="#28566f" stroke-width="28"/>')
 s.s.append('<path d="M 354 205 L 566 213" fill="none" stroke="#28566f" stroke-width="24"/>')
 s.rect(380,128,150,100,'#234e68');s.text(455,167,'K9 CALM',20,'white','middle');s.circle(498,200,5,'#6cce96');s.circle(411,200,8,'#9bb4c4')
 for x,y in [(390,138),(519,138),(390,217),(519,217)]:s.circle(x,y,3,'#a5c0ce')
 s.line(410,133,305,85,'#1598b1',2);s.text(50,80,'Caja aislante y sensor firme',18)
 s.line(499,146,570,82,'#1598b1',2);s.text(575,87,'Antena y microfono libres',18)
 s.line(385,219,175,335,'#1598b1',2);s.text(25,358,'Pack desmontable',18);s.text(25,383,'en compartimento aislado',17)
 s.text(500,446,'Ilustracion de diseño. Solo maqueta: sin validacion de uso animal.',18,anchor='middle');s.save('16_concepto_pechera')
 s=SVG(1000,330);s.text(25,35,'Prueba ADC por USB | sin pilas ni otra fuente',24)
 s.text(45,130,'3V3',23);s.line(120,124,200,124,'#087f99');s.rect(200,95,160,55);s.text(280,129,'R1 150k',21,anchor='middle');s.line(360,124,470,124,'#087f99');s.circle(470,124,6,'#087f99')
 s.line(470,124,600,124,'#087f99');s.text(470,87,'Nodo: ~1.32 V',20,anchor='middle');s.text(615,131,'GPIO0',22)
 s.line(470,124,470,180);s.rect(390,180,160,50);s.text(470,212,'R2 100k',21,anchor='middle');s.line(470,230,470,270);s.line(470,270,800,270);s.text(815,276,'GND',21)
 s.line(750,124,750,185);s.line(470,124,750,124,'#087f99');s.line(730,185,770,185);s.line(730,199,770,199);s.line(750,199,750,270);s.text(790,198,'100nF',18)
 s.text(30,309,'150k arriba, 100k abajo. Ventrada = Vnodo x 2.5. Placa alimentada solo por USB.',19);s.save('17_divisor_usb')
