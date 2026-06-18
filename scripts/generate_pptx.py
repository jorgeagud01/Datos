# scripts/generate_pptx.py
# Genera PPTX para cada sesión a partir de slides/session_*.md y las imágenes en dist/images/
# Requisitos: python3, pip install python-pptx markdown

from pptx import Presentation
from pptx.util import Inches, Pt
import glob
import os
import markdown
from pathlib import Path

INPUT_DIR = 'slides'
IMAGES_DIR = 'dist/images'
OUTPUT_DIR = 'dist/pptx'

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Convierte un archivo markdown simple en una lista de slides.
# Espera que el markdown tenga secciones separadas por títulos H1 o H2,
# o usa líneas en formato 'Slide Title\n- bullet1\n- bullet2'. Este es un generador simple.

def md_to_slides(md_text):
    slides = []
    # Separar por líneas '---' o por líneas que comiencen con '# '
    parts = []
    if '---' in md_text:
        parts = [p.strip() for p in md_text.split('---') if p.strip()]
    else:
        # split by lines that look like '1) ' numbering slide headings present in our md
        lines = md_text.splitlines()
        current = []
        for line in lines:
            if line.strip().endswith(':') and len(current) > 0 and len(current) < 2:
                # heurística: treat as continuation
                current.append(line)
            elif line.strip().startswith('1)') or line.strip().startswith('1)'):
                if current:
                    parts.append('\n'.join(current))
                current = [line]
            elif line.strip().startswith('1)'):
                if current:
                    parts.append('\n'.join(current))
                current = [line]
            else:
                current.append(line)
        if current:
            parts.append('\n'.join(current))

    for p in parts:
        title = ''
        bullets = []
        lines = p.splitlines()
        # first non-empty line is title
        for i,l in enumerate(lines):
            l = l.strip()
            if not l:
                continue
            title = l[:100]
            bullets = [ln.strip('- ').strip() for ln in lines[i+1:] if ln.strip()]
            break
        slides.append({'title': title, 'bullets': bullets})
    # fallback: if no parts parsed, create single slide with whole text
    if not slides:
        slides.append({'title': 'Contenido', 'bullets': md_text.splitlines()[:10]})
    return slides


def create_pptx_from_md(md_path, output_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    prs = Presentation()
    # usar layout 0 title slide
    title_slide_layout = prs.slide_layouts[0]
    body_layout = prs.slide_layouts[1]

    # portadilla
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    session_title = Path(md_path).stem.replace('_', ' ').title()
    title.text = session_title
    subtitle.text = 'IA práctica con Gemini — Capacitación'

    slides_content = md_to_slides(md_text)
    for s in slides_content:
        slide = prs.slides.add_slide(body_layout)
        title = slide.shapes.title
        title.text = s['title'][:200]
        body = slide.shapes.placeholders[1].text_frame
        for b in s['bullets']:
            p = body.add_paragraph()
            p.text = b
            p.level = 0
            p.font.size = Pt(18)

    # intentar incrustar imagen de portada de sesión si existe
    base = Path(md_path).stem
    possible_img = Path(IMAGES_DIR) / f"slide_title_{base}.png"
    if possible_img.exists():
        # añadir slide con la imagen
        img_slide = prs.slides.add_slide(prs.slide_layouts[6])
        left = top = Inches(0)
        pic = img_slide.shapes.add_picture(str(possible_img), left, top, width=prs.slide_width)

    prs.save(output_path)
    print(f'Generado {output_path}')


if __name__ == '__main__':
    md_files = sorted(glob.glob(os.path.join(INPUT_DIR, 'session_*.md')) + glob.glob(os.path.join(INPUT_DIR, 'sesion_*.md')))
    if not md_files:
        md_files = sorted(glob.glob(os.path.join(INPUT_DIR, '*.md')))

    for md in md_files:
        out_filename = Path(md).stem + '.pptx'
        out_path = os.path.join(OUTPUT_DIR, out_filename)
        create_pptx_from_md(md, out_path)

    print('PPTX generados en', OUTPUT_DIR)
