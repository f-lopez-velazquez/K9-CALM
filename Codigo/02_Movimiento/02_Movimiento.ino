// Hecho por el profesor Francisco López Velázquez.
// zolvek.com.mx | K9 CALM - guia facil
#include <K9CalmAula.h>  // Biblioteca incluida en el curso.
K9CalmAula aula;         // Nuestro dispositivo.

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
