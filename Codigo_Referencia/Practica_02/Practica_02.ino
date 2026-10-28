// K9 CALM | Practica 2 | Arduino-ESP32 3.3.4
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

void setup(){
  Serial.begin(115200); // sin esperar al monitor: funciona con pilas
  pinMode(LED,OUTPUT); pinMode(BTN,INPUT_PULLUP);
  iniciarIMU();
  Serial.println("K9 CALM listo; boton cambia modo; l conmuta LED manual");
}
void loop(){
  ahora=millis(); controles();
  movimiento();
  bool luz=automatico?((ahora/500)%2):manualLed;
  if(automatico) luz=(actividad>0.7f);
  digitalWrite(LED,luz);
  if(ahora-informe>=250){
    informe=ahora;
    Serial.printf("modo:%d",automatico);
    Serial.printf(" a:%.3f giro:%.3f act:%.3f",magnitud,giro,actividad);
    Serial.println();
  }
  yield(); // cede CPU; no espera milisegundos fijos
}
