// Hecho por el profesor Francisco López Velázquez.
// zolvek.com.mx | K9 CALM - guia facil
#include <K9CalmAula.h>  // Biblioteca incluida en el curso.
K9CalmAula aula;         // Nuestro dispositivo.

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
