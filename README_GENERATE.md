# Instrucciones para generar PNGs y PPTX (dist/)

Sigue estos pasos en tu máquina local (o en un runner CI) para generar los PNG y PPTX finales y subirlos al repo.

1) Generar PNGs a partir de SVGs

- Instala Inkscape o librsvg (rsvg-convert). En Ubuntu:
  - sudo apt-get update && sudo apt-get install -y inkscape

- Ejecuta el script:
  - bash scripts/generate_images.sh

Las imágenes se crearán en dist/images/ con los nombres: banner_capacitacion_gemini.png, card_slack_gemini.png, infographic_ruta_aprendizaje.png y slide_title_sesionXX.png

2) Generar PPTX a partir de los markdown de slides

- Crea un entorno Python e instala dependencias:
  - python3 -m venv venv
  - source venv/bin/activate
  - pip install python-pptx markdown

- Ejecuta:
  - python3 scripts/generate_pptx.py

Los PPTX se crearán en dist/pptx/ (plantilla maestra + session_01.pptx ... session_08.pptx)

3) Revisión y commiteo

- Revisa los archivos en dist/
- Añade y commitea los binarios al repo en la rama training/ia-gemini-package:
  - git add dist/
  - git commit -m "Add generated PNGs and PPTX for IA Gemini training"
  - git push origin training/ia-gemini-package

Si quieres, puedo ejecutar estos pasos por ti si me das acceso a un runner (por ejemplo, un servidor con SSH o un workflow de GitHub Actions que yo pueda disparar). Si prefieres que yo ejecute todo y suba los binarios desde aquí, dime y te doy las opciones para autorizar un workflow (por ejemplo, yo puedo add a GitHub Action workflow that runs these scripts on push to a special branch; you will need to approve the action in your repo settings).