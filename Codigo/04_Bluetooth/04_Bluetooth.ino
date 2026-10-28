// Hecho por el profesor Francisco López Velázquez.
// zolvek.com.mx | K9 CALM - guia facil
#include <K9CalmAula.h>  // Biblioteca incluida en el curso.
K9CalmAula aula;         // Nuestro dispositivo.

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
