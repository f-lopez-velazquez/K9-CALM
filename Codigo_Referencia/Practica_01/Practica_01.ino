// K9 CALM | Practica 1 | Arduino-ESP32 3.3.4
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

void setup(){
  Serial.begin(115200); // sin esperar al monitor: funciona con pilas
  pinMode(LED,OUTPUT); pinMode(BTN,INPUT_PULLUP);
  Serial.println("K9 CALM listo; boton cambia modo; l conmuta LED manual");
}
void loop(){
  ahora=millis(); controles();
  bool luz=automatico?((ahora/500)%2):manualLed;
  digitalWrite(LED,luz);
  if(ahora-informe>=250){
    informe=ahora;
    Serial.printf("modo:%d",automatico);
    Serial.println();
  }
  yield(); // cede CPU; no espera milisegundos fijos
}
