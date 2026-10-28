"""Identidad editorial compartida de los dos manuales de Francisco López Velázquez."""
from pathlib import Path
import json
from reportlab.lib import colors
NAVY='#12334d'; TEAL='#087f99'; INK='#223d50'; PALE='#edf4f6'
AUTHOR='Hecho por el profesor Francisco López Velázquez.'
WEBSITE='zolvek.com.mx'
REPO_URL='https://github.com/f-lopez-velazquez/K9-CALM'
def furniture(c,d,label='MANUAL COMPLETO'):
 c.saveState()
 # Marca de agua tenue detrás del contenido; texto real, seleccionable.
 c.setFillColor(colors.HexColor(NAVY));c.setFillAlpha(.025)
 c.translate(306,396);c.rotate(36);c.setFont('Bold',20)
 c.drawCentredString(0,0,AUTHOR);c.setFont('Body',17);c.drawCentredString(0,-27,WEBSITE)
 c.restoreState();c.saveState()
 c.setFillColor(colors.HexColor(NAVY));c.rect(0,778,612,14,fill=1,stroke=0)
 c.setFont('Bold',8);c.drawString(50,758,'ZOLVEK  /  K9 CALM')
 c.setFont('Body',7.8);c.drawRightString(562,758,label)
 c.setStrokeColor(colors.HexColor(TEAL));c.setLineWidth(.75);c.line(50,747,562,747)
 c.setStrokeColor(colors.HexColor('#cddde4'));c.line(50,44,562,44)
 c.setFont('Body',7.6);c.drawString(50,30,AUTHOR)
 c.setFont('Bold',8);c.drawString(50,17,WEBSITE)
 c.linkURL('https://'+WEBSITE,(50,14,125,27),relative=0)
 c.setFont('Body',8);c.drawRightString(562,23,f'{d.page:02d}')
 c.restoreState()
def cover_asset(project):
 p=Path(project)/'Ilustraciones'/'K9_Calm_concepto.png'
 return p if p.exists() else None
