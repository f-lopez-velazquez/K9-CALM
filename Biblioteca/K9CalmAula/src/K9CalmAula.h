// Hecho por el profesor Francisco López Velázquez. zolvek.com.mx
#pragma once
#include <Arduino.h>
// Ayuda de aula: la configuracion del hardware vive en el .cpp.
class K9CalmAula {
 public:
  void iniciar(uint8_t etapa);
  void actualizar();
  void ajustarSonido(float minimo);
  void ajustarCambio(float minimo);
  void prepararMedicion(bool activa, float calibracion=1.0f);
  void parpadear(uint32_t intervaloMs);
  void encender(bool estado);
  void alertar(uint32_t tiempoMs=1000);
  void mostrar();
  void enviar();
  void compararEvento();
  float actividad() const;
  float rms() const;
  float voltaje() const;
  bool impulso() const;
  bool movimientoOK() const;
  bool sonidoOK() const;
  bool automatico() const;
  int evento() const;
  int puntos() const;
 private:
  uint8_t etapa_=1;
};
