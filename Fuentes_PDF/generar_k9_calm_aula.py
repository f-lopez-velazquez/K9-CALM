#!/usr/bin/env python3
"""Genera guía fácil y prepara el repositorio público, sin publicarlo."""
from pathlib import Path
import sys,shutil,json
HERE=Path(__file__).resolve();ROOT=next((p for p in HERE.parents if (p/'scripts/project_cli.py').is_file()),None)
if ROOT is None:
 ROOT=HERE.parents[1];PUBLIC=ROOT
else:PUBLIC=ROOT/'projects/K9_Calm_Publico'
PUBLIC.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(HERE.parent))
from k9_guia_facil import build
if (ROOT/'projects/K9_Calm').exists():
 from k9_aula_fuentes import generate
 generate(ROOT,PUBLIC)
 original=ROOT/'projects/K9_Calm'
 for name in ['Diagramas','Fuentes_PDF/fonts','Fuentes_PDF/Licencias','Ilustraciones','Codigo']:
  target=PUBLIC/('Codigo_Referencia' if name=='Codigo' else name)
  shutil.copytree(original/name,target,dirs_exist_ok=True)
 for name in ['Referencias.md','Lista_de_Materiales.csv']:
  shutil.copyfile(original/name,PUBLIC/name)
 (PUBLIC/'Guia').mkdir(exist_ok=True)
 shutil.copyfile(ROOT/'docs/k9_calm/Evidencia_vibracion_y_bienestar.md',PUBLIC/'Guia/Evidencia_vibracion_y_bienestar.md')
 from k9_identidad import REPO_URL
 (PUBLIC/'identidad.json').write_text(json.dumps({'repositorio':REPO_URL,'autor':'Hecho por el profesor Francisco López Velázquez.','sitio':'https://zolvek.com.mx','colores':{'marino':'#12334d','teal':'#087f99','blanco':'#ffffff'}},ensure_ascii=False,indent=2))
 # Leer desde copia publica permite regenerar la guia sin dependencias del repositorio principal.
 for name in ['generar_k9_calm_aula.py','k9_guia_facil.py','k9_aula_fuentes.py','k9_identidad.py']:
  shutil.copyfile(HERE.parent/name,PUBLIC/'Fuentes_PDF'/name)
 for name in ['generar_k9_calm.py','k9_editorial.py','k9_detalles.py','k9_texto.py']:
  shutil.copyfile(HERE.parent/name,PUBLIC/'Fuentes_PDF'/name)
build(ROOT,PUBLIC)
