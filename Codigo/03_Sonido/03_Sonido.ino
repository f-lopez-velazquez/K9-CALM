// Hecho por el profesor Francisco López Velázquez.
// zolvek.com.mx | K9 CALM - guia facil
#include <K9CalmAula.h>  // Biblioteca incluida en el curso.
K9CalmAula aula;         // Nuestro dispositivo.

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
