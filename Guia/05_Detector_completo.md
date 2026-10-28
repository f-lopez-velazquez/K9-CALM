# 05 · Relacionar sonido y movimiento

Un ruido no basta: observa qué pasó antes y después.

[Inicio](../README.md) · [Configuración](00_Empezar.md) · [Archivo listo](../Codigo/05_Detector_completo/05_Detector_completo.ino)

## A · Conecta y comprueba

Con USB retirado: No agregues componentes. Ahora cambia la forma de decidir.

![Circuito](../Diagramas/08_estados.png)

| Desde | Conecta hasta |
| --- | --- |
| Montaje | Conserva P4 y USB |
| Objeto | Sensor sujeto: no debe quedar colgando |
| Sonido | Grabación moderada, misma distancia |
| Personas y animales | Pruebas en mesa o peluche; sin perros |

El programa conserva 2 s de actividad previa. Si detecta un impulso, observa 1.5 s posteriores. Compara las medias (promedios de las lecturas) y comprueba que haya suficientes datos.

Las categorías describen ensayos: E0 sin evento pendiente, E1 sonido, E2 posible cambio posterior, E3 datos insuficientes. Ninguna mide miedo con certeza.

**Comprobación:** Al iniciar, deja el objeto quieto 5 s. Revisa IMU:1, MIC:1 y que rms cambie con sonido. E0 por sí solo no demuestra que los sensores estén bien.

## B · Copia el programa completo

Abre el archivo o borra el editor y pega todo. No lo agregues debajo del código anterior.

```cpp
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
```

| Línea o función | Qué hace |
| --- | --- |
| ajustarCambio(CAMBIO_MOV) | Fija la diferencia mínima de actividad que compararás. |
| compararEvento() | Gestiona historia previa, ventana posterior y espera. |
| aula.evento() == 2 | Comprueba si la categoría actual es E2. |
| encender(...) / enviar() | Muestra la decisión mediante LED y BLE. |

### Ejemplo antes de probar

| Caso | Cómo se interpreta |
| --- | --- |
| Antes: 0.10 / después: 0.20 | E1 si hubo impulso y datos válidos. |
| Antes: 0.10 / después: 1.20 | Puede producir E2; requiere datos válidos y cambio suficiente. |

## C · Observa, predice y cambia

1. **Control: solo sonido.** Tras 5 s quieto, reproduce el sonido sin mover nada. Debe producir E1 si detecta un impulso.
2. **Añade movimiento posterior.** Repite el mismo sonido y mueve el objeto durante el siguiente segundo y medio. Puede producir E2 si cambia suficiente.
3. **Prueba MANUAL.** Pulsa el botón: sigue midiendo y transmitiendo, pero P5 muestra M y E0; desarma la comparación automática.

Fragmentos ilustrativos de salida; tus números pueden variar:

```text
A E1 B0 Q20
A E2 B0 Q80
M E0 B0 Q0
```

### Cambia CAMBIO_MOV

| Prueba | Qué comparar |
| --- | --- |
| 0.30 | Reduce el mínimo; observa falsas alertas |
| 0.70 | Valor de partida |
| 1.20 | Aumenta el mínimo de cambio |

También cuenta la variación previa: se usa el mayor entre CAMBIO_MOV y tres veces esa variación. Q es una puntuación experimental, no un porcentaje de miedo.

**Si falla:** Siempre E1: revisa cuándo mueves el objeto y observa act. E3: espera 5 s y revisa lecturas recientes. No quites las condiciones de calidad para forzar E2.

**Registra:** cambié ___; predije ___; observé ___. Avanza cuando puedas repetirlo y explicar por qué cambió la salida.
