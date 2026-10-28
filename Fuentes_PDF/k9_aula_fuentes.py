"""Cinco programas breves y biblioteca de aula basada en el motor del manual completo."""
from pathlib import Path
import sys,re,json,zipfile,shutil,hashlib
AUTHOR='Francisco López Velázquez'
REPO='https://github.com/f-lopez-velazquez/K9-CALM'
NAMES=['01_Luz_y_boton','02_Movimiento','03_Sonido','04_Bluetooth','05_Detector_completo']
COMMON='''// Hecho por el profesor Francisco López Velázquez.
// zolvek.com.mx | K9 CALM - guia facil
#include <K9CalmAula.h>  // Biblioteca incluida en el curso.
K9CalmAula aula;         // Nuestro dispositivo.
'''
SKETCHES=[COMMON+'''
const int PARPADEO_MS = 500; // Cambia SOLO este numero.

void setup() {               // Se ejecuta una vez.
  aula.iniciar(1);            // Prepara LED, boton y Serial.
}

void loop() {                // Se repite continuamente.
  aula.actualizar();          // Lee el boton sin detener el programa.
  aula.parpadear(PARPADEO_MS); // AUTO: enciende y apaga el LED.
  aula.mostrar();             // Muestra el modo cada 250 ms.
}
''',COMMON+'''
const float UMBRAL_MOV = 0.70; // Menor = mas sensible.

void setup() {
  aula.iniciar(2);             // Conserva P1 y agrega MPU6050.
}

void loop() {
  aula.actualizar();           // Lee boton y movimiento.
  bool seMueve = aula.actividad() > UMBRAL_MOV;
  aula.encender(seMueve);      // AUTO: LED si supera el umbral.
  aula.mostrar();              // a, giro y act en el monitor.
}
''',COMMON+'''
const float UMBRAL_MOV = 0.70;
const float UMBRAL_SONIDO = 0.004; // Menor = detecta sonidos mas suaves.
const int ALERTA_MS = 1000;        // Duracion de la luz.

void setup() {
  aula.ajustarSonido(UMBRAL_SONIDO);
  aula.iniciar(3);                  // Conserva P2 y agrega microfono.
}

void loop() {
  aula.actualizar();                // Lee ambos sensores y boton.
  if (aula.impulso()) {             // Detecto un sonido brusco.
    aula.alertar(ALERTA_MS);        // Guarda la alerta sin usar delay.
  }
  aula.encender(aula.actividad() > UMBRAL_MOV);
  aula.mostrar();                   // Observa act, rms y pico.
}
''',COMMON+'''
const float UMBRAL_MOV = 0.70;
const float UMBRAL_SONIDO = 0.004;
const int ALERTA_MS = 1000;
const bool MEDIR_DIVISOR = false; // Dejar false en USB normal.
const float CALIBRACION = 1.000;  // Cambiar solo al medir con multimetro.

void setup() {
  aula.ajustarSonido(UMBRAL_SONIDO);
  aula.prepararMedicion(MEDIR_DIVISOR, CALIBRACION);
  aula.iniciar(4);                // Conserva P3 y agrega BLE.
}

void loop() {
  aula.actualizar();              // Tambien mide ADC si fue habilitado.
  if (aula.impulso()) aula.alertar(ALERTA_MS);
  aula.encender(aula.actividad() > UMBRAL_MOV);
  aula.enviar();                  // Estado y voltaje para nRF Connect.
  aula.mostrar();                 // Comprueba tambien en la PC.
}
''',COMMON+'''
const float UMBRAL_SONIDO = 0.004;
const float CAMBIO_MOV = 0.70;     // Diferencia minima despues del sonido.
const bool MEDIR_DIVISOR = false; // USB: false. Medicion guiada: true.
const float CALIBRACION = 1.000;

void setup() {
  aula.ajustarSonido(UMBRAL_SONIDO);
  aula.ajustarCambio(CAMBIO_MOV);
  aula.prepararMedicion(MEDIR_DIVISOR, CALIBRACION);
  aula.iniciar(5);                // Conserva todo lo anterior.
}

void loop() {
  aula.actualizar();              // Sigue leyendo aunque haya alerta.
  aula.compararEvento();          // Compara 2 s antes y 1.5 s despues.
  aula.encender(aula.evento() == 2); // LED: posible reaccion.
  aula.enviar();                  // Envia E0, E1, E2 o E3 por BLE.
  aula.mostrar();                 // Muestra categoria y puntuacion.
}
''']
HEADER='''// Hecho por el profesor Francisco López Velázquez. zolvek.com.mx
#pragma once
#include <Arduino.h>
// Ayuda de aula: la configuracion del hardware vive en el .cpp.
class K9CalmAula {
 public:
  void iniciar(uint8_t etapa);
  void actualizar();
  void ajustarSonido(float minimo);
  void ajustarCambio(float minimo);
  void prepararMedicion(bool activa, float calibracion=1.0f);
  void parpadear(uint32_t intervaloMs);
  void encender(bool estado);
  void alertar(uint32_t tiempoMs=1000);
  void mostrar();
  void enviar();
  void compararEvento();
  float actividad() const;
  float rms() const;
  float voltaje() const;
  bool impulso() const;
  bool movimientoOK() const;
  bool sonidoOK() const;
  bool automatico() const;
  int evento() const;
  int puntos() const;
 private:
  uint8_t etapa_=1;
};
'''
WRAPPER=r'''
} // namespace motor: detalles de los sensores y comunicaciones

void K9CalmAula::ajustarSonido(float v){ motor::minSonido=fmaxf(v,0.00001f); }
void K9CalmAula::ajustarCambio(float v){ motor::minCambio=fmaxf(v,0.01f); }
void K9CalmAula::prepararMedicion(bool activa,float c){
  motor::PILAS=activa; motor::CAL=c;
}
void K9CalmAula::iniciar(uint8_t etapa){
  etapa_=constrain(etapa,1,5);
  Serial.begin(115200);
  pinMode(motor::LED,OUTPUT); pinMode(motor::BTN,INPUT_PULLUP);
  if(etapa_>=2) motor::iniciarIMU();
  if(etapa_>=3) motor::iniciarAudio();
  if(etapa_>=4) motor::iniciarBLE();
  Serial.println("K9 CALM | Zolvek | listo");
  Serial.println("Boton: AUTO/MANUAL. En MANUAL, envia l para cambiar LED.");
}
void K9CalmAula::actualizar(){
  motor::ahora=millis(); motor::controles();
  if(etapa_>=2) motor::movimiento();
  if(etapa_>=3) motor::escuchar();
  if(etapa_>=4) motor::medirPilas();
  yield();
}
void K9CalmAula::encender(bool estado){
  bool luz=motor::automatico?estado:motor::manualLed;
  if(motor::automatico && motor::alertaActiva){
    if(uint32_t(millis()-motor::inicioAlerta)<motor::duracionAlerta) luz=true;
    else motor::alertaActiva=false;
  }
  // Los avisos de alimentacion tienen prioridad sobre la luz del ejercicio.
  if(motor::bateria) luz=(millis()/(motor::bateria==1?500:125))%2;
  digitalWrite(motor::LED,luz);
}
void K9CalmAula::parpadear(uint32_t t){
  t=t?t:1; encender((millis()/t)%2);
}
void K9CalmAula::alertar(uint32_t t){
  motor::inicioAlerta=millis();motor::duracionAlerta=t;motor::alertaActiva=true;
  motor::evento=1;
}
void K9CalmAula::compararEvento(){
  if(etapa_>=5){
    motor::integrar();
    if(motor::evento!=2) motor::alertaActiva=false;
  }
}
void K9CalmAula::enviar(){ if(etapa_>=4) motor::publicar(); }
void K9CalmAula::mostrar(){
  if(millis()-motor::informe<250) return;
  motor::informe=millis();
  Serial.printf("modo:%d",motor::automatico);
  if(etapa_>=2) Serial.printf(" a:%.2f giro:%.2f act:%.3f IMU:%d",
      motor::magnitud,motor::giro,motor::actividad,movimientoOK());
  if(etapa_>=3) Serial.printf(" rms:%.5f pico:%.5f MIC:%d",
      motor::rms,motor::pico,sonidoOK());
  if(etapa_>=4) Serial.printf(" V:%.3f B:%d E:%d Q:%d",
      motor::voltaje,motor::bateria,motor::evento,motor::puntos);
  Serial.println();
}
float K9CalmAula::actividad() const {return motor::actividad;}
float K9CalmAula::rms() const {return motor::rms;}
float K9CalmAula::voltaje() const {return motor::voltaje;}
bool K9CalmAula::impulso() const {return motor::impulso;}
bool K9CalmAula::movimientoOK() const {
  return motor::imuOK && motor::ultimoIMU && millis()-motor::ultimoIMU<80;
}
bool K9CalmAula::sonidoOK() const {
  // Confirma recepcion reciente, no demuestra que SD tenga audio correcto.
  return motor::audioOK && motor::ultimoAudio && millis()-motor::ultimoAudio<100;
}
bool K9CalmAula::automatico() const {return motor::automatico;}
int K9CalmAula::evento() const {return motor::evento;}
int K9CalmAula::puntos() const {return motor::puntos;}
'''

def generate(root,public):
 sys.path.insert(0,str(root/'scripts/generators'))
 import generar_k9_calm as full
 lib=public/'Biblioteca/K9CalmAula';(lib/'src').mkdir(parents=True,exist_ok=True)
 (lib/'src/K9CalmAula.h').write_text(HEADER)
 combined=full.BASE.replace('@STAGE@','aula')+full.MOTION+full.AUDIO+full.BATTERY+full.INTEGRATION
 combined=re.sub(r'^#include.*\n','',combined,flags=re.M)
 combined=combined.replace('constexpr bool PILAS=false;','bool PILAS=false;')
 combined=combined.replace('constexpr float CAL=1.000f, FACTOR=2.50f;','float CAL=1.000f; constexpr float FACTOR=2.50f;')
 combined=combined.replace('fmaxf(0.004f,ruido*6)','fmaxf(minSonido,ruido*6)')
 combined=combined.replace('fmaxf(0.7f,3*sigma)','fmaxf(minCambio,3*sigma)')
 combined=combined.replace('alertaHasta=ahora+1500;', 'alertaHasta=ahora+1500; inicioAlerta=ahora; duracionAlerta=1500; alertaActiva=true;')
 prefix='''// Hecho por el profesor Francisco López Velázquez. zolvek.com.mx
// Motor de aula: completo y editable. Las bibliotecas externas conservan sus licencias.
#include "K9CalmAula.h"
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <driver/i2s_std.h>
#include <NimBLEDevice.h>
#include <math.h>
namespace motor {
float minSonido=0.004f, minCambio=0.7f;
bool alertaActiva=false;
uint32_t inicioAlerta=0,duracionAlerta=1000;
'''
 (lib/'src/K9CalmAula.cpp').write_text(prefix+combined+WRAPPER)
 (lib/'LICENSE').write_text('Copyright (c) 2026 Francisco López Velázquez.\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies, subject to retaining this copyright and permission notice.\n\nTHE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM OR DAMAGES ARISING FROM USE OF THE SOFTWARE.\n\nExternal libraries are separately licensed by their authors.\n')
 (lib/'library.properties').write_text('''name=K9CalmAula
version=1.0.0
author=Francisco Lopez Velazquez
maintainer=Francisco Lopez Velazquez
sentence=Ayuda de laboratorio K9 CALM para preparatoria.
paragraph=Sensores, LED, boton, BLE y ADC; cinco practicas acumulativas.
category=Other
url=https://github.com/f-lopez-velazquez/K9-CALM
architectures=esp32
includes=K9CalmAula.h
depends=Adafruit MPU6050 (=2.2.9), Adafruit BusIO (=1.17.4), Adafruit Unified Sensor (=1.1.15), NimBLE-Arduino (=2.5.2)
''')
 for i,(name,code) in enumerate(zip(NAMES,SKETCHES),1):
  p=public/'Codigo'/name;p.mkdir(parents=True,exist_ok=True);(p/(name+'.ino')).write_text(code)
 # Fuentes de terceros en archivos ZIP oficiales; sin entornos/caches/instalaciones.
 downloads=root/'tmp/pdfs/k9_tools/downloads/libraries'
 dest=public/'Librerias/ZIP';dest.mkdir(parents=True,exist_ok=True)
 ordered=['Adafruit_BusIO-1.17.4.zip','Adafruit_Unified_Sensor-1.1.15.zip','Adafruit_GFX_Library-1.13.0.zip','Adafruit_SSD1306-2.5.17.zip','Adafruit_MPU6050-2.2.9.zip','NimBLE_Arduino-2.5.2.zip']
 for n in ordered:shutil.copyfile(downloads/n,dest/n)
 with zipfile.ZipFile(dest/'K9CalmAula-1.0.0.zip','w',zipfile.ZIP_DEFLATED) as z:
  for f in lib.rglob('*'):
   if f.is_file():z.write(f,'K9CalmAula/'+str(f.relative_to(lib)))
 with zipfile.ZipFile(public/'Librerias/Instalar_todas.zip','w',zipfile.ZIP_DEFLATED) as z:
  for archive in sorted(dest.glob('*.zip')):
   with zipfile.ZipFile(archive) as src:
    roots={n.split('/')[0] for n in src.namelist() if n}
    assert len(roots)==1,(archive,roots)
    for n in src.namelist():
     if not n.endswith('/'):z.writestr('libraries/'+n,src.read(n))
 hashes={str(f.relative_to(public)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted((public/'Librerias').rglob('*.zip'))}
 (public/'Librerias/SHA256.json').write_text(json.dumps(hashes,indent=2)+'\n')
 (public/'Librerias/LEEME.md').write_text('''# Bibliotecas incluidas

Ruta más sencilla: extrae `Instalar_todas.zip` **dentro de la carpeta del sketchbook** que aparece en Archivo > Preferencias de Arduino IDE. Quedará `Arduino/libraries/K9CalmAula/`, junto con las seis bibliotecas de terceros. Reinicia el IDE. No lo extraigas dentro de otra carpeta `libraries` porque se duplicaría ese nivel.

Alternativa: Programa/Sketch > Incluir biblioteca > Añadir biblioteca .ZIP; instala **cada uno de los siete ZIP** de `ZIP/`, primero las dependencias y K9CalmAula al final. Si el IDE ofrece descargar dependencias, las copias de esta carpeta ya fijan las versiones.

Incluidas: K9CalmAula 1.0.0; MPU6050 2.2.9; BusIO 1.17.4; Unified Sensor 1.1.15; GFX 1.13.0; SSD1306 2.5.17; NimBLE-Arduino 2.5.2. GFX/SSD1306 son dependencias declaradas de esta versión de MPU6050; **no se necesita una pantalla**.

ZIP de terceros: copias de los archivos originales descargados por Arduino CLI desde el índice oficial; se conservan código, avisos y licencias. `SHA256.json` permite verificar las copias. No se incluyen ejecutables ni entornos instalados. Arduino IDE y el core ESP32 (con herramientas por sistema operativo) requieren instalación oficial; consulta `Guia/00_Empezar.md`.
''')
 print('Cinco sketches breves y siete bibliotecas empaquetados')
