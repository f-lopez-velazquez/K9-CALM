# 02 · Medir movimiento

Encender el LED cuando el objeto se mueve lo suficiente.

[Inicio](../README.md) · [Configuración](00_Empezar.md) · [Archivo listo para abrir](../Codigo/02_Movimiento/02_Movimiento.ino)

## 1. Conecta sin USB

| Terminal | Conexión |
| --- | --- |
| Conserva P1 | LED y botón quedan en sus pines. |
| GY-521 / MPU6050 | VCC -> 3V3; GND y AD0 -> GND; SDA -> 4; SCL -> 5 |

## 2. Copia todo o abre el archivo

Borra el programa anterior del editor. Usa un solo sketch.

```cpp
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
```

## 3. Qué hace cada cosa

| Código | Qué hace |
| --- | --- |
| iniciar(2) | Agrega el sensor de movimiento. |
| actividad() | Devuelve cuánto cambia la aceleración; unidad: m/s². |
| > UMBRAL_MOV | Pregunta si la actividad supera el número elegido. |
| encender(seMueve) | En AUTO, prende el LED cuando la respuesta es sí. |

## 4. Haz la prueba

1. Sube P2 y espera 5 s sobre la mesa. Busca I2C 0x68 y a cerca de 9.81.
2. Sujeta el sensor al objeto o peluche; muévelo suave, sin golpear.
3. Observa act: aumenta. El LED enciende si supera 0.70.
4. Prueba el botón: MANUAL y la letra l siguen funcionando.

## 5. Cambia un valor y vuelve a subir

| Valor | Cambio | Qué observar |
| --- | --- | --- |
| UMBRAL_MOV | 0.70 -> 0.30 | Puede encender con movimientos menores. |
| UMBRAL_MOV | 0.70 -> 1.20 | Requiere una actividad mayor. |

**Si falla:** ¿No aparece 0x68? Revisa SDA=4, SCL=5 y AD0=GND. IMU:0 indica que no hay lecturas recientes; no significa reposo.

![Diagrama de la práctica](../Diagramas/H2_conexiones.png)

Se agregan solo las conexiones del MPU6050. El micrófono todavía no se monta.
