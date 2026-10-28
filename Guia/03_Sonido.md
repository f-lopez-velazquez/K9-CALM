# 03 · Detectar un sonido

Escucha un sonido moderado y compara su lectura con el ambiente.

[Inicio](../README.md) · [Configuración](00_Empezar.md) · [Archivo listo](../Codigo/03_Sonido/03_Sonido.ino)

## A · Conecta y comprueba

Con USB retirado: INMP441, 100 kohm de SD a GND y desacoplo si falta. Conserva P2.

![Circuito](../Diagramas/H3_conexiones.png)

| Desde | Conecta hasta |
| --- | --- |
| VDD / GND / L/R | 3V3 / GND / GND |
| SCK / WS | GPIO6 / GPIO7 |
| SD | GPIO1 y resistencia 100 kohm a GND |
| 100 nF, si falta en módulo | Entre VDD y GND, cerca del micrófono |

El micrófono ya entrega números digitales. SCK y WS son relojes; SD lleva los datos al C3. rms resume la amplitud en una ventana: no es una medida de dB.

L/R a GND elige el canal izquierdo, que es el que lee el código. No confundas SD del audio con SDA del acelerómetro. No tapes el orificio del micrófono.

**Comprobación:** Mide VDD-GND: cerca de 3.3 V. Después del arranque, habla suave y verifica que rms y pico cambien. Un reloj I2S no se comprueba con una lectura fija del multímetro.

## B · Copia el programa completo

Abre el archivo o borra el editor y pega todo. No lo agregues debajo del código anterior.

```cpp
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
```

| Línea o función | Qué hace |
| --- | --- |
| ajustarSonido(UMBRAL_SONIDO) | Configura el mínimo de amplitud antes de iniciar. |
| aula.impulso() | Pregunta si se detectó un sonido brusco en esta vuelta. |
| if (...) { alertar(...); } | Si hubo impulso, guarda una alerta de duración definida. |
| actualizar() / encender() | Sigue leyendo ambos sensores; no usa delay para sostener la luz. |

### Ejemplo antes de probar

| Caso | Cómo se interpreta |
| --- | --- |
| Ejemplo de ambiente | rms = 0.001; pequeño frente al mínimo 0.004 |
| Ejemplo de sonido brusco | rms = 0.012; puede activar si cumple las otras condiciones |

## C · Observa, predice y cambia

1. **Aprende el ambiente.** Sube P3 y espera 3 s. Habla suave: rms y pico deben variar. MIC:1 solo confirma datos recientes, no audio correcto.
2. **Reproduce el sonido.** Usa una palmada grabada a volumen moderado. Espera 3 s entre intentos. La alerta dura 1 s si detecta un impulso.
3. **Conserva lo anterior.** Mueve el objeto y observa act. El LED también puede encender por movimiento; deja el objeto quieto para probar solo sonido.

Fragmentos ilustrativos de salida; tus números pueden variar:

```text
modo:1 a:9.81 giro:0.02 act:0.10 IMU:1
rms:0.00100 pico:0.00300 MIC:1
```

### Cambia UMBRAL_SONIDO

| Prueba | Qué comparar |
| --- | --- |
| 0.008 | Sube el mínimo: puede detectar menos |
| 0.004 | Valor de partida |
| 0.002 | Baja el mínimo: comprueba falsas alertas |

El detector también considera ruido de fondo, ataque y pico/RMS. Superar 0.004 no garantiza una alerta. Después cambia ALERTA_MS=1500: solo debe durar más la luz.

**Si falla:** Audio siempre cero: revisa L/R a GND y SD=1. Pico cerca de 1 permanentemente: baja volumen y revisa formato/cables. Evita sonidos fuertes.

**Registra:** cambié ___; predije ___; observé ___. Avanza cuando puedas repetirlo y explicar por qué cambió la salida.
