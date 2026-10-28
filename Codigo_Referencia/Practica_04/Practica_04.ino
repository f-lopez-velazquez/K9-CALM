// K9 CALM | Practica 4 | Arduino-ESP32 3.3.4
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

void setup(){
  Serial.begin(115200); // sin esperar al monitor: funciona con pilas
  pinMode(LED,OUTPUT); pinMode(BTN,INPUT_PULLUP);
  iniciarIMU();
  iniciarAudio();
  iniciarBLE();
  Serial.println("K9 CALM listo; boton cambia modo; l conmuta LED manual");
}
void loop(){
  ahora=millis(); controles();
  movimiento();
  escuchar();
  medirPilas();
  if(impulso){ evento=1; alertaHasta=ahora+1000; }
  publicar();
  bool luz=automatico?((ahora/500)%2):manualLed;
  if(automatico) luz=(actividad>0.7f);
  if(automatico && int32_t(alertaHasta-ahora)>0) luz=true;
  if(bateria) luz=((ahora/(bateria==1?500:125))%2);
  digitalWrite(LED,luz);
  if(ahora-informe>=250){
    informe=ahora;
    Serial.printf("modo:%d",automatico);
    Serial.printf(" a:%.3f giro:%.3f act:%.3f",magnitud,giro,actividad);
    Serial.printf(" rms:%.5f pico:%.5f ag:%.2f dur:%lu",rms,pico,agudos,
        (unsigned long)duracion);
    Serial.printf(" V:%.3f B:%d E:%d Q:%d",voltaje,bateria,evento,puntos);
    Serial.println();
  }
  yield(); // cede CPU; no espera milisegundos fijos
}
