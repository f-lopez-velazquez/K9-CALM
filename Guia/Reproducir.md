# Reproducir materiales y verificar programas

Para hacer las prácticas **no necesitas Python ni compilar los PDF**. Usa Arduino IDE y los archivos .ino.

## Volver a crear la guía fácil

En una copia independiente del repositorio:

```sh
python -m venv .venv
# Activa el entorno según tu sistema operativo.
python -m pip install reportlab PyMuPDF Pillow
python Fuentes_PDF/generar_k9_calm_aula.py
```

Lee los esquemas, imágenes y fuentes TTF que ya están incluidos. Crea `output/pdf/K9_Calm/Manual_K9_Calm_Guia_Facil.pdf`. El contenido de las lecciones vive en `Fuentes_PDF/k9_guia_facil.py`; el código breve está en `Codigo/`. No necesitas generar imágenes otra vez.

## Compilar desde terminal

Instala Arduino CLI desde Arduino; sigue primero la configuración del IDE para instalar el core 3.3.4 y las siete bibliotecas incluidas. Después:

```sh
arduino-cli compile --fqbn esp32:esp32:esp32c3:CDCOnBoot=cdc Codigo/01_Luz_y_boton
```

Cambia la carpeta para compilar las demás. `Verificacion/` conserva los resultados de la entrega; no sustituye las nuevas pruebas si cambias versiones o fuentes.

## Qué se ha verificado

- Los cinco programas de aula se compilan contra una extracción limpia de `Librerias/Instalar_todas.zip`.
- El manual completo conserva sus programas de referencia y registros anteriores.
- Se revisan PDF renderizados, marcas de agua, enlaces y coincidencia de los códigos impresos.
- No se ha probado hardware ni la eficacia terapéutica de vibración. El motor sigue como extensión de banco.

El entorno instalado del compilador no forma parte del repositorio: depende del sistema operativo y se instala desde las distribuciones oficiales.
