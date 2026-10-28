// Hecho por el profesor Francisco López Velázquez.
// zolvek.com.mx | K9 CALM - guia facil
#include <K9CalmAula.h>  // Biblioteca incluida en el curso.
K9CalmAula aula;         // Nuestro dispositivo.

const int PARPADEO_MS = 500; // Cambia SOLO este numero.

void setup() {               // Se ejecuta una vez.
  aula.iniciar(1);            // Prepara LED, boton y Serial.
}

void loop() {                // Se repite continuamente.
  aula.actualizar();          // Lee el boton sin detener el programa.
  aula.parpadear(PARPADEO_MS); // AUTO: enciende y apaga el LED.
  aula.mostrar();             // Muestra el modo cada 250 ms.
}
