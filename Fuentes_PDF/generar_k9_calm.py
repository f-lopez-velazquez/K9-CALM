#!/usr/bin/env python3
"""Construye fuentes Arduino, diagramas y manual K9 CALM. Ver README."""
from pathlib import Path
import sys, json, csv, math, html, shutil, zipfile
from k9_texto import accent
HERE=Path(__file__).resolve()
REPO=next((p for p in HERE.parents if (p/'scripts'/'project_cli.py').is_file()),None)
ROOT=REPO if REPO else HERE.parents[1]
PROJECT=ROOT/'projects'/'K9_Calm' if REPO else HERE.parents[1]
for sub in ['Codigo','Diagramas','Fuentes_PDF']:(PROJECT/sub).mkdir(parents=True,exist_ok=True)

BASE=r'''// K9 CALM | Practica @STAGE@ | Arduino-ESP32 3.3.4
// LED externo activo en HIGH. No se usa LED integrado.
#include <Arduino.h>
#include <math.h>
constexpr int LED=10, BTN=3;
bool automatico=true, manualLed=false;
uint32_t ahora=0, cambio=0, informe=0;
bool crudo=HIGH, estable=HIGH;
int evento=0, puntos=0; // 0 normal, 1 sonido, 2 posible reaccion, 3 insuficiente
uint32_t alertaHasta=0;
void controles() {
  bool b=digitalRead(BTN);
  if(b!=crudo){ crudo=b; cambio=ahora; }
  if(ahora-cambio>=30 && b!=estable){
    estable=b;
    if(b==LOW){ automatico=!automatico; Serial.println(automatico?"AUTO":"MANUAL"); }
  }
  // En modo manual, enviar l (ele minuscula) conmuta el LED.
  if(Serial.available() && Serial.read()=='l') manualLed=!manualLed;
}
'''
MOTION=r'''
#include <Wire.h>
#include <Adafruit_MPU6050.h>
Adafruit_MPU6050 mpu;
bool imuOK=false;
float actividad=0, giro=0, magnitud=0;
float historial[100]={0}; // 2 s a 50 Hz; contiene actividad filtrada
int cabeza=0, cuantos=0;
uint32_t ultimoIMU=0, pasoIMU=0;
void iniciarIMU(){
  Wire.begin(4,5); Wire.setTimeOut(10); // SDA, SCL, limite de espera I2C
  Serial.println("Escaner I2C: se espera 0x68");
  for(int d=1;d<127;d++){
    Wire.beginTransmission(d);
    if(Wire.endTransmission()==0) Serial.printf("I2C 0x%02X\n",d);
  }
  imuOK=mpu.begin(0x68,&Wire); // AD0 a GND. Si falla, revisar y reiniciar.
  if(!imuOK){ Serial.println("MPU AUSENTE: revisar H2"); return; }
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
}
void movimiento(){
  if(!imuOK || ahora-pasoIMU<20) return;
  pasoIMU=ahora;
  sensors_event_t a,g,t;
  if(!mpu.getEvent(&a,&g,&t)) return;
  // Unidades de Adafruit: m/s2 y rad/s (no grados/s).
  magnitud=sqrtf(a.acceleration.x*a.acceleration.x+
      a.acceleration.y*a.acceleration.y+a.acceleration.z*a.acceleration.z);
  giro=sqrtf(g.gyro.x*g.gyro.x+g.gyro.y*g.gyro.y+g.gyro.z*g.gyro.z);
  float dinamica=fabsf(magnitud-9.80665f);
  actividad+=0.15f*(dinamica-actividad); // filtro exponencial
  historial[cabeza]=actividad; cabeza=(cabeza+1)%100;
  if(cuantos<100) cuantos++;
  ultimoIMU=ahora;
}
'''
AUDIO=r'''
#include <driver/i2s_std.h>
i2s_chan_handle_t rx=nullptr;
bool audioOK=false, impulso=false;
constexpr int N=256, FS=16000;
float re[N], im[N], rms=0, pico=0, ruido=0.001f, agudos=0;
float ataque=0, decaimiento=0, rmsAnterior=0;
uint32_t ultimoAudio=0, inicioSonido=0, duracion=0, ultimoPulso=0;
bool sonando=false;
int llenos=0;
void iniciarAudio(){
  i2s_chan_config_t c=I2S_CHANNEL_DEFAULT_CONFIG(I2S_NUM_0,I2S_ROLE_MASTER);
  c.dma_desc_num=8; c.dma_frame_num=128;
  if(i2s_new_channel(&c,nullptr,&rx)!=ESP_OK) return;
  i2s_std_config_t s={};
  s.clk_cfg=I2S_STD_CLK_DEFAULT_CONFIG(FS);
  // Dos ranuras de 32 bits = 64 BCLK por trama. Solo usamos izquierda.
  s.slot_cfg=I2S_STD_PHILIPS_SLOT_DEFAULT_CONFIG(
      I2S_DATA_BIT_WIDTH_32BIT,I2S_SLOT_MODE_STEREO);
  s.gpio_cfg.mclk=I2S_GPIO_UNUSED; s.gpio_cfg.bclk=GPIO_NUM_6;
  s.gpio_cfg.ws=GPIO_NUM_7; s.gpio_cfg.dout=I2S_GPIO_UNUSED;
  s.gpio_cfg.din=GPIO_NUM_1;
  audioOK=(i2s_channel_init_std_mode(rx,&s)==ESP_OK &&
           i2s_channel_enable(rx)==ESP_OK);
  if(!audioOK) Serial.println("ERROR I2S: revisar version y pines");
}
// FFT radix-2 in situ. N debe ser potencia de 2.
void espectro(){
  for(int i=0;i<N;i++){
    re[i]*=0.5f-0.5f*cosf(2*PI*i/(N-1)); im[i]=0; // ventana Hann
  }
  for(int i=1,j=0;i<N;i++){
    int b=N>>1; for(;j&b;b>>=1) j^=b; j^=b;
    if(i<j){ float v=re[i]; re[i]=re[j]; re[j]=v; }
  }
  for(int len=2;len<=N;len<<=1){
    float ang=-2*PI/len;
    for(int i=0;i<N;i+=len){
      for(int j=0;j<len/2;j++){
        int u=i+j,v=u+len/2;
        float c=cosf(ang*j),s=sinf(ang*j);
        float tr=c*re[v]-s*im[v],ti=s*re[v]+c*im[v];
        re[v]=re[u]-tr; im[v]=im[u]-ti; re[u]+=tr; im[u]+=ti;
      }
    }
  }
  float total=0,alta=0;
  for(int k=2;k<N/2;k++){
    float e=re[k]*re[k]+im[k]*im[k]; total+=e;
    if(k*FS/N>=2000) alta+=e;
  }
  agudos=total>1e-12f?alta/total:0; // proporcion, no identificador del sonido
}
void analizarAudio(){
  float media=0, suma=0; pico=0;
  for(int i=0;i<N;i++) media+=re[i]/N;
  for(int i=0;i<N;i++){
    re[i]-=media; suma+=re[i]*re[i]; pico=fmaxf(pico,fabsf(re[i]));
  }
  rms=sqrtf(suma/N);
  ataque=fmaxf(0,rms-rmsAnterior); decaimiento=fmaxf(0,rmsAnterior-rms);
  float umbral=fmaxf(0.004f,ruido*6);
  bool fuerte=(rms>umbral);
  // Calentamiento 1 s; no se aprende el ruido durante sonidos fuertes.
  if(ahora<1000 || !fuerte) ruido+=0.01f*(rms-ruido);
  impulso=(ahora>=1000 && fuerte && !sonando &&
      pico/fmaxf(rms,1e-6f)>2.0f && ataque>ruido*2 &&
      ahora-ultimoPulso>2000);
  if(impulso) ultimoPulso=ahora;
  if(fuerte && !sonando){ inicioSonido=ahora; sonando=true; }
  if(sonando) duracion=ahora-inicioSonido;
  if(!fuerte) sonando=false;
  rmsAnterior=rms;
  espectro(); // destruye re[]; se vuelve a llenar en la siguiente ventana
  ultimoAudio=ahora;
}
void escuchar(){
  impulso=false;
  if(!audioOK) return;
  int32_t par[64*2]; size_t leidos=0;
  // Timeout 0: si DMA no tiene datos, volvemos sin esperar.
  i2s_channel_read(rx,par,sizeof(par),&leidos,0);
  for(size_t j=0;j+1<leidos/4;j+=2){
    // 24 bits validos alineados a la izquierda; canal L/R conectado a GND.
    re[llenos++]=(par[j]>>8)/8388608.0f;
    if(llenos==N){ llenos=0; analizarAudio(); }
  }
}
'''
BATTERY=r'''
#include <NimBLEDevice.h>
// Cambiar a true SOLO tras validar H4. En USB, desconectar el portapilas.
constexpr bool PILAS=false;
constexpr float CAL=1.000f, FACTOR=2.50f; // 150k arriba + 100k abajo
// Umbrales didacticos: sustituir por los determinados con carga y regulador real.
constexpr float V_BAJA=4.00f, V_CRITICA=3.80f, HISTERESIS=0.15f;
float voltaje=0; int bateria=0; // 0 USB/normal, 1 baja, 2 critica, 3 ADC invalido
uint32_t pasoADC=0, pasoBLE=0;
NimBLECharacteristic *estadoBLE=nullptr, *voltajeBLE=nullptr;
const char* SERVICIO="8d6c0001-3d68-4b85-9b71-4d3943414c4d";
class Conexion:public NimBLEServerCallbacks{
  void onDisconnect(NimBLEServer*,NimBLEConnInfo&,int) override{
    NimBLEDevice::startAdvertising();
  }
} conexion;
void iniciarBLE(){
  NimBLEDevice::init("K9-CALM");
  auto s=NimBLEDevice::createServer(); s->setCallbacks(&conexion,false);
  auto servicio=s->createService(SERVICIO);
  estadoBLE=servicio->createCharacteristic(
      "8d6c0002-3d68-4b85-9b71-4d3943414c4d",
      NIMBLE_PROPERTY::READ|NIMBLE_PROPERTY::NOTIFY);
  voltajeBLE=servicio->createCharacteristic(
      "8d6c0003-3d68-4b85-9b71-4d3943414c4d",NIMBLE_PROPERTY::READ);
  servicio->start();
  auto a=NimBLEDevice::getAdvertising();
  a->setName("K9-CALM"); a->addServiceUUID(SERVICIO);
  a->enableScanResponse(true); a->start();
  analogReadResolution(12); analogSetPinAttenuation(0,ADC_11db);
}
void medirPilas(){
  if(!PILAS || ahora-pasoADC<1000) return;
  pasoADC=ahora;
  uint32_t suma=0;
  for(int j=0;j<16;j++) suma+=analogReadMilliVolts(0);
  float mv=suma/16.0f; voltaje=mv*FACTOR*CAL/1000;
  if(mv<100 || mv>2400){ bateria=3; return; }
  if(bateria==3) bateria=0;
  if(voltaje<V_CRITICA) bateria=2;
  else if(bateria==2 && voltaje<V_CRITICA+HISTERESIS) return;
  else if(voltaje<V_BAJA) bateria=1;
  else if(voltaje>V_BAJA+HISTERESIS) bateria=0;
  else if(bateria==2) bateria=1;
}
void publicar(){
  if(ahora-pasoBLE<500) return;
  pasoBLE=ahora;
  // <=20 bytes: compatible con ATT MTU 23. Sin datos privados ni audio.
  char texto[21];
  snprintf(texto,sizeof(texto),"%c E%d B%d Q%d",automatico?'A':'M',
      evento,bateria,puntos);
  estadoBLE->setValue(texto); estadoBLE->notify();
  char v[12];
  if(PILAS) snprintf(v,sizeof(v),"%.3f V",voltaje);
  else snprintf(v,sizeof(v),"USB; NA");
  voltajeBLE->setValue(v);
}
'''
INTEGRATION=r'''
enum Fase{OBSERVAR,POSTERIOR,REPOSO};
Fase fase=OBSERVAR;
float previa=0, sigma=0, sumaPost=0, ataqueEvento=0, agudosEvento=0;
int nPost=0; bool suficiente=false;
uint32_t inicioEvento=0, descanso=0, contadoIMU=0;
void integrar(){
  // Modo manual conserva medidas y BLE; desarma la clasificacion automatica.
  if(!automatico){ fase=OBSERVAR; evento=0; puntos=0; return; }
  if(fase==REPOSO){
    if(ahora-descanso>=2000){fase=OBSERVAR; evento=0; puntos=0;}
    return;
  }
  if(fase==OBSERVAR && impulso){
    previa=0; sigma=0;
    for(int j=0;j<cuantos;j++) previa+=historial[j]/cuantos;
    for(int j=0;j<cuantos;j++) sigma+=sq(historial[j]-previa)/cuantos;
    sigma=sqrtf(sigma);
    suficiente=(cuantos==100 && ahora-ultimoIMU<80 &&
                ahora-ultimoAudio<100 && pico<0.98f);
    ataqueEvento=ataque; agudosEvento=agudos;
    sumaPost=0; nPost=0; inicioEvento=ahora; contadoIMU=ultimoIMU;
    evento=1; fase=POSTERIOR;
  }
  if(fase!=POSTERIOR) return;
  if(ahora-ultimoIMU>80 || ahora-ultimoAudio>100) suficiente=false;
  if(ultimoIMU!=contadoIMU){
    contadoIMU=ultimoIMU; sumaPost+=actividad; nPost++;
  }
  if(ahora-inicioEvento<1500) return;
  float posterior=nPost?sumaPost/nPost:0;
  bool cambioMov=(posterior>previa+fmaxf(0.7f,3*sigma));
  // Puntuacion exploratoria; no es probabilidad ni diagnostico.
  puntos=(cambioMov?60:0)+(ataqueEvento>0.01f?20:10)+
         (agudosEvento>0.25f?20:0);
  suficiente=suficiente && nPost>=60;
  evento=!suficiente?3:(cambioMov?2:1);
  if(!suficiente) puntos=0;
  alertaHasta=ahora+1500; descanso=ahora; fase=REPOSO;
  Serial.printf("Evento=%d Q=%d pre=%.2f post=%.2f n=%d\n",
      evento,puntos,previa,posterior,nPost);
}
'''
def firmware():
 for stage in range(1,6):
  code=BASE.replace('@STAGE@',str(stage))
  if stage>=2:code+=MOTION
  if stage>=3:code+=AUDIO
  if stage>=4:code+=BATTERY
  if stage>=5:code+=INTEGRATION
  code+='\nvoid setup(){\n  Serial.begin(115200); // sin esperar al monitor: funciona con pilas\n  pinMode(LED,OUTPUT); pinMode(BTN,INPUT_PULLUP);\n'
  if stage>=2:code+='  iniciarIMU();\n'
  if stage>=3:code+='  iniciarAudio();\n'
  if stage>=4:code+='  iniciarBLE();\n'
  code+='  Serial.println("K9 CALM listo; boton cambia modo; l conmuta LED manual");\n}\nvoid loop(){\n  ahora=millis(); controles();\n'
  if stage>=2:code+='  movimiento();\n'
  if stage>=3:code+='  escuchar();\n'
  if stage==3:code+='  if(impulso){ evento=1; alertaHasta=ahora+1000; }\n'
  if stage>=4:code+='  medirPilas();\n'
  if stage==4:code+='  if(impulso){ evento=1; alertaHasta=ahora+1000; }\n'
  if stage>=5:code+='  integrar();\n'
  if stage>=4:code+='  publicar();\n'
  code+='  bool luz=automatico?((ahora/500)%2):manualLed;\n'
  if stage>=2:code+='  if(automatico) luz=(actividad>0.7f);\n'
  if stage>=3:code+='  if(automatico && int32_t(alertaHasta-ahora)>0) luz=true;\n'
  if stage>=4:code+='  if(bateria) luz=((ahora/(bateria==1?500:125))%2);\n'
  code+='  digitalWrite(LED,luz);\n  if(ahora-informe>=250){\n    informe=ahora;\n'
  code+='    Serial.printf("modo:%d",automatico);\n'
  if stage>=2:code+='    Serial.printf(" a:%.3f giro:%.3f act:%.3f",magnitud,giro,actividad);\n'
  if stage>=3:code+='    Serial.printf(" rms:%.5f pico:%.5f ag:%.2f dur:%lu",rms,pico,agudos,\n        (unsigned long)duracion);\n'
  if stage>=4:code+='    Serial.printf(" V:%.3f B:%d E:%d Q:%d",voltaje,bateria,evento,puntos);\n'
  code+='    Serial.println();\n  }\n  yield(); // cede CPU; no espera milisegundos fijos\n}\n'
  p=PROJECT/('Codigo_Referencia' if (PROJECT/'Codigo_Referencia').exists() else 'Codigo')/f'Practica_{stage:02d}';p.mkdir(exist_ok=True)
  (p/f'Practica_{stage:02d}.ino').write_text(code)
  print('Firmware',stage,len(code.splitlines()),'lineas')

# SVG original: terminales explicitos, redes etiquetadas; no finge una fotografia.
class SVG:
 def __init__(self,w=1000,h=500):self.w=w;self.h=h;self.s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="100%" height="100%" fill="white"/>']
 def line(self,x,y,x2,y2,c='#15334c',sw=3):self.s.append(f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{sw}"/>')
 def rect(self,x,y,w,h,c='#edf6fa',stroke='#12334d',r=8):self.s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{c}" stroke="{stroke}" stroke-width="2"/>')
 def text(self,x,y,t,size=18,c='#12334d',anchor='start'):self.s.append(f'<text x="{x}" y="{y}" font-family="DejaVu Sans,sans-serif" font-size="{size}" fill="{c}" text-anchor="{anchor}">{html.escape(accent(t))}</text>')
 def circle(self,x,y,r=5,c='#cda552'):self.s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>')
 def save(self,name):
  p=PROJECT/'Diagramas'/f'{name}.svg'
  drawing=''.join(self.s)+'</svg>'
  for old in ['#9561a9','#279566','#d18d22','#925cc2','#288cc3','#d25d77','#21916e','#df7c2e','#d77a25','#925cc2','#925cc2']:
   drawing=drawing.replace(old,'#087f99')
  p.write_text(drawing)
  import fitz
  doc=fitz.open(str(p)); doc[0].get_pixmap(matrix=fitz.Matrix(2,2)).save(str(p.with_suffix('.png')))

def board(s,x,y,back=False):
 s.rect(x,y,210,330,'#1e4864');s.rect(x+70,y-8,70,55,'#c0cad1');s.text(x+105,y+25,'USB-C',14,anchor='middle')
 if not back:
  s.rect(x+60,y+100,90,95,'#252c33');s.text(x+105,y+140,'ESP32',14,'white','middle');s.text(x+105,y+162,'C3',14,'white','middle')
  s.rect(x+64,y+258,83,35,'#b34a32');s.text(x+105,y+281,'ANTENA',13,'white','middle')
  s.rect(x+50,y+58,35,20,'#d8dde1');s.rect(x+125,y+58,35,20,'#d8dde1');s.text(x+67,y+54,'RST',11,'white');s.text(x+128,y+54,'BOOT',11,'white')
 else:s.text(x+105,y+150,'REVERSO',17,'white','middle');s.text(x+105,y+177,'sin escala',14,'white','middle')
 left=['5V','GND','3V3','4','3','2','1','0'];right=['5','6','7','8','9','10','20','21']
 if back:left,right=right,left
 for i,(a,b) in enumerate(zip(left,right)):
  yy=y+70+i*33;s.circle(x+10,yy);s.circle(x+200,yy)
  s.text(x+23,yy+5,a,13,'white');s.text(x+187,yy+5,b,13,'white','end')
 return {str(n):(x+(10 if side==0 else 200),y+70+i*33) for side,arr in enumerate([left,right]) for i,n in enumerate(arr)}

def diagrams():
 s=SVG(1000,490);s.text(30,34,'ESP32-C3 SuperMini | USB arriba, componentes a la vista',22)
 p=board(s,330,90)
 funcs={'5V':'VBUS / entrada LDO validada','GND':'Referencia comun','3V3':'Salida regulada: sensores','4':'SDA / MPU6050','3':'Boton a GND','2':'Arranque: libre','1':'SD / microfono','0':'ADC1 / divisor','5':'SCL / MPU6050','6':'BCLK / microfono','7':'WS / microfono','8':'LED integrado / arranque: libre','9':'BOOT / arranque: libre','10':'LED externo con 330 ohm','20':'Libre / UART RX','21':'Libre / UART TX'}
 for n,(x,y) in p.items():
  if x<400:s.line(x,y,300,y,'#198ba3',2);s.text(285,y+5,f'{n}: {funcs[n]}',14,anchor='end')
  else:s.line(x,y,570,y,'#198ba3',2);s.text(585,y+5,f'{n}: {funcs[n]}',14)
 s.text(30,466,'Ilustracion tecnica original. Confirmar serigrafia y regulador de cada unidad.',16);s.save('01_pinout')
 s=SVG(1000,470);s.text(35,35,'Reconocer las dos caras antes de cablear',23);board(s,160,90);board(s,620,90,True)
 s.text(265,448,'Frente: componentes',18,anchor='middle');s.text(725,448,'Atras: columnas reflejadas',18,anchor='middle');s.save('02_caras')
 # Componentes con terminales y ejes; pin placement deliberately terminal block rather than unknown clone physical orientation.
 s=SVG(1000,440);s.text(30,35,'Sensores: leer las etiquetas del modulo comprado',24)
 for x,title,pins in [(50,'GY-521 / MPU6050',['VCC','GND','SCL','SDA','XDA','XCL','AD0','INT']),(550,'INMP441',['VDD','GND','SCK','WS','SD','L/R'])]:
  s.rect(x,85,390,230,'#204e76');s.text(x+195,120,title,22,'white','middle');s.rect(x+150,155,90,75,'#242b34')
  for i,p in enumerate(pins):s.circle(x+25+i*45,280,7);s.text(x+25+i*45,305,p,12,'white','middle')
 s.line(290,190,375,190,'#df7c2e');s.text(380,197,'X',20);s.line(290,190,290,135,'#21916e');s.text(296,149,'Y',20);s.circle(280,201,7,'#23a8bf');s.text(295,220,'Z sale de la placa',13,'white')
 s.text(65,357,'Ejes ilustrativos: cotejar flechas del PCB real.',16);s.text(550,357,'L/R a GND: canal izquierdo. Orificio libre.',16)
 s.text(30,400,'Vista esquematizada, no huella de montaje. Orden de terminales varia entre fabricantes.',17);s.save('03_sensores')
 # Wiring stages use per-net horizontal rows, exact endpoints no crossing ambiguity.
 net=[('10','330 ohm -> anodo LED; catodo a GND','#d77a25'),('3','Pulsador normalmente abierto -> GND','#9561a9'),('3V3','VCC GY-521 + VDD INMP441','#dc5353'),('GND','GND sensores, AD0 y L/R','#344b59'),('4','MPU6050 SDA','#168fa6'),('5','MPU6050 SCL','#279566'),('6','INMP441 SCK / BCLK','#d18d22'),('7','INMP441 WS','#925cc2'),('1','INMP441 SD; 100k a GND','#288cc3'),('0','Nodo divisor 150k / 100k + 100nF a GND','#d25d77')]
 for st in range(1,6):
  count={1:2,2:6,3:9,4:10,5:10}[st];s=SVG(1000,135+count*39)
  s.text(25,35,f'H{st} | '+['LED y boton','Anadir MPU6050','Anadir INMP441','Medir pilas','Montaje integrado'][st-1],25)
  s.rect(30,65,190,count*39+15,'#1e4864');s.text(125,90,'ESP32-C3',21,'white','middle')
  for i,(pin,dest,col) in enumerate(net[:count]):
   if st<3: dest=dest.replace(' + VDD INMP441','').replace(', AD0 y L/R',', AD0')
   y=115+i*39;s.circle(210,y,5);s.text(195,y+5,pin,18,'white','end');s.line(215,y,340,y,col,4);s.circle(340,y,5,col);s.text(355,y+5,dest,18)
  if st==2:s.text(355,115+2*39+23,'INMP441 todavia no se monta.',13)
  s.text(25,120+count*39,'USB en H1-H3. H4-H5: elegir USB o pilas; nunca ambos.',17);s.save(f'H{st}_conexiones')
 # Power topology with separable pack; branch node after switch ensures no ADC injection when off.
 s=SVG(1000,460);s.text(25,35,'H4 | Alimentacion portatil, habilitacion condicionada',24)
 items=[(20,'3 AAA','max. medido'),(230,'F1 + D1','PTC + Schottky'),(460,'S1','interruptor'),(690,'5V / VBUS','LDO -> 3V3')]
 for x,a,b in items:s.rect(x,90,190,75);s.text(x+95,120,a,18,anchor='middle');s.text(x+95,145,b,14,anchor='middle')
 for x in [210,440,670]:s.line(x,127,x+20,127,'#d75555',4)
 s.line(680,127,680,215,'#d75555');s.circle(680,127);s.rect(610,215,140,50);s.text(680,246,'R1 150k',19,anchor='middle')
 s.line(680,265,680,300);s.line(680,300,880,300,'#218ba7');s.text(885,306,'GPIO0',17)
 s.rect(610,320,140,50);s.text(680,351,'R2 100k',19,anchor='middle');s.line(680,300,680,320);s.line(680,370,680,400)
 s.line(680,400,900,400);s.text(905,406,'GND',17);s.line(830,300,830,335);s.line(810,335,850,335);s.line(810,347,850,347);s.line(830,347,830,400);s.text(852,350,'100nF',14)
 s.text(25,220,'D1: anodo hacia + pilas; banda/catodo hacia S1.',16);s.text(25,250,'F1: PTC 0.5 A nominal, validar curva y caida.',16)
 s.text(25,280,'C1: 100 uF / 10 V entre nodo S1 y GND.',16);s.text(25,310,'Todos los negativos a GND. USB desconectado.',16)
 s.text(25,340,'El divisor mide DESPUES de F1, D1 y S1.',16);s.text(25,370,'No detecta inversion, temperatura ni corta la energia.',16);s.save('04_alimentacion')
 s=SVG(1000,390);s.text(25,35,'Extension opcional | motor a 3 V regulados, solo en banco',24)
 s.rect(680,95,130,70);s.text(745,135,'MOTOR 3 V',18,anchor='middle');s.line(745,65,745,95);s.text(760,70,'+3 V regulados externos',16)
 s.line(745,165,745,240);s.rect(675,240,140,60);s.text(745,275,'NMOS',19,anchor='middle');s.line(745,300,745,350);s.text(762,352,'GND comun',17)
 s.line(75,265,250,265);s.text(75,246,'GPIO20 (reservado)',18);s.rect(250,242,100,45);s.text(300,270,'100 ohm',16,anchor='middle');s.line(350,265,675,265)
 s.line(480,265,480,300);s.rect(435,300,90,40);s.text(480,326,'100k',18,anchor='middle');s.line(480,340,480,350);s.line(480,350,745,350)
 s.line(745,65,900,65);s.line(900,65,900,95);s.rect(850,95,100,70);s.text(900,122,'Diodo',16,anchor='middle');s.text(900,148,'banda +',15,anchor='middle');s.line(900,165,900,200);s.line(745,200,900,200)
 s.text(25,380,'NMOS con RDS(on) especificada a 2.5/3.3 V; diodo en antiparalelo. No conectar motor al GPIO.',16);s.save('05_motor')
 # Compact harness concept
 s=SVG(1000,440);s.text(30,35,'Propuesta de montaje | maqueta sobre peluche, sin uso animal',23)
 s.rect(100,90,800,260,'#e5edf2');s.rect(130,195,740,55,'#b9cbd6')
 for x,y,w,h,a in [(155,120,180,150,'3 AAA en caja'),(400,125,180,140,'ESP32-C3'),(650,125,130,65,'GY-521'),(650,235,130,65,'INMP441')]:s.rect(x,y,w,h,'#174965');s.text(x+w/2,y+h/2,a,17,'white','middle')
 s.text(120,385,'Caja aislante + alivio de tension + fijacion del sensor. Antena y puerto acustico libres.',18)
 s.text(120,414,'Sin bordes, piezas sueltas ni conductores expuestos. Retirar para programar por USB.',17);s.save('06_montaje')
 s=SVG(1000,250);s.text(25,35,'De una senal fisica a un registro comprensible',24)
 for i,(a,b) in enumerate([('Sonido','INMP441 / I2S'),('Movimiento','MPU6050 / I2C'),('ESP32-C3','Analisis temporal'),('Resultado','LED + BLE')]):
  x=20+i*250;s.rect(x,90,210,90);s.text(x+105,123,a,21,anchor='middle');s.text(x+105,155,b,16,anchor='middle')
  if i<3:s.line(x+210,135,x+245,135,'#18a0b5');s.text(x+227,127,'>',20)
 s.text(25,224,'Sonido y movimiento se combinan en el ESP32-C3; no diagnostican miedo.',18);s.save('07_sistema')
 for flow in ['estados','flujo']:
  s=SVG(1000,360);s.text(25,35,'Maquina de estados' if flow=='estados' else 'Flujo de una vuelta de loop()',24)
  labels=['OBSERVAR: 2 s previos','POSTERIOR: 1.5 s','REPOSO: 2 s'] if flow=='estados' else ['Boton + MPU6050','DMA audio + FFT','ADC + estados + BLE']
  for i,t in enumerate(labels):
   x=25+i*330;s.rect(x,110,290,95);s.text(x+145,165,t,18,anchor='middle')
   if i<2:s.line(x+290,155,x+330,155,'#1b9db4');s.text(x+300,145,'>',20)
  s.line(830,205,830,280);s.line(830,280,170,280);s.line(170,280,170,205)
  s.text(500,315,'Sin impulso permanece observando; el modo manual desarma el evento.' if flow=='estados' else 'Cada modulo atiende su plazo; I2S devuelve de inmediato si no hay datos.',17,anchor='middle');s.save('08_'+flow)
 # Signals and physics plots, using svg exact original examples not measured.
 s=SVG(1000,590);s.text(25,35,'Sonidos ilustrativos | formas sinteticas, sin grabaciones reales',24)
 for row,(name,dec,freq) in enumerate([('Aplauso',35,40),('Portazo',13,13),('Pirotecnia',24,32),('Trueno',4,6)]):
  y=115+row*110;s.text(25,y,name,18);s.line(180,y,950,y,'#9baeb8',1)
  prev=None
  for k in range(390):
   t=k/390;v=(math.sin(freq*2*math.pi*t)+.35*math.sin(2*freq*2*math.pi*t))*math.exp(-dec*t);x=180+770*t;yy=y-v*32
   if prev:s.line(*prev,x,yy,'#188ca9',1.5)
   prev=(x,yy)
 s.text(180,560,'Tiempo ->    Altura = amplitud relativa; el origen no se deduce de la curva.',17);s.save('09_sonidos')
 s=SVG(1000,440);s.text(25,35,'Movimiento | ejemplo simulado, actividad en m/s2',24)
 s.line(90,340,950,340);s.line(90,340,90,80);s.text(65,90,'3',16);s.text(65,342,'0',16)
 prev=None
 for k in range(500):
  t=k/500*6;val=.1+.08*math.sin(t*10)+(1.5*(1+math.sin(t*18))*.5 if 2.5<t<4 else 0);x=90+860*t/6;y=340-val*77
  if prev:s.line(*prev,x,y,'#168da4',2)
  prev=(x,y)
 s.line(90+860*2/6,80,90+860*2/6,340,'#df7c2e');s.text(320,70,'Sonido',17);s.text(130,390,'Antes: linea base',18);s.text(440,390,'Despues: comparar',18);s.text(820,390,'6 s',17);s.save('10_movimiento')
 s=SVG(1000,400);s.text(25,35,'Interfaz Arduino IDE 2.x | representacion, no captura real',24)
 s.rect(35,65,930,300,'#f5f7f8');s.rect(35,65,930,55,'#d4e8e9');s.text(60,100,'Verificar [check]   Subir [->]    ESP32C3 Dev Module   | Puerto USB',20)
 s.rect(50,137,185,200,'white');s.text(65,170,'Gestor de placas',17);s.text(65,205,'Bibliotecas',17);s.text(65,240,'Herramientas',17)
 s.text(260,167,'Practica_01.ino',20);s.text(260,210,'void setup() { ... }',18);s.text(260,247,'void loop()  { ... }',18);s.rect(250,265,690,75,'#e4eef2');s.text(265,294,'Monitor serie / Serial Plotter: 115200 baudios',17);s.text(265,321,'modo:1 a:9.810 giro:0.020 act:0.030',17);s.save('11_ide')
 s=SVG(1000,390);s.text(25,35,'FFT | de la onda a la energia por banda',24)
 s.line(80,310,940,310);s.line(80,310,80,80)
 for k in range(1,31):
  x=100+k*25;h=150*math.exp(-((k-4)/2)**2)+65*math.exp(-((k-19)/5)**2)
  s.rect(x,310-h,12,h,'#1b96ad',r=0)
 s.text(100,350,'0 Hz',16);s.text(300,350,'2 kHz',16);s.text(830,350,'8 kHz',16);s.text(150,85,'Graves',18);s.text(570,170,'Agudos: fraccion sobre 2 kHz',18);s.save('12_fft')

if __name__=='__main__':
 firmware();diagrams()
 from k9_detalles import details
 details(SVG,board)
 # El modulo editorial vive junto al generador en el repositorio o el paquete.
 sys.path.insert(0,str(Path(__file__).resolve().parent))
 from k9_editorial import build
 build(ROOT,PROJECT)
