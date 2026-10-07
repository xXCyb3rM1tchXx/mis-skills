#!/usr/bin/env python3
"""Validate deterministic Stage 11 DOCX visual system."""
import sys
from docx import Document
from docx.oxml.ns import qn

EXPECTED = {
    "Normal": ("Aptos", 9.5, None),
    "Title": ("Aptos Display", 22.0, "1F4E79"),
    "Heading 1": ("Aptos Display", 15.0, "1F4E79"),
    "Heading 2": ("Aptos Display", 12.0, "2F5597"),
    "Heading 3": ("Aptos Display", 10.5, "4472C4"),
}

def rgb(font):
    try:
        return str(font.color.rgb) if font.color.rgb else None
    except Exception:
        return None

def close(a,b,tol=.03):
    return abs(a-b)<=tol

def main(path):
    doc=Document(path)
    errors=[]
    sec=doc.sections[0]
    dims=(sec.page_width.inches,sec.page_height.inches)
    if not (close(dims[0],8.5) and close(dims[1],11.0)):
        errors.append(f"Page size {dims} != Letter")
    for label,val,exp in [
        ("top",sec.top_margin.inches,.55),("bottom",sec.bottom_margin.inches,.55),
        ("left",sec.left_margin.inches,.62),("right",sec.right_margin.inches,.62)
    ]:
        if not close(val,exp,.04):
            errors.append(f"{label} margin {val:.2f} != ~{exp}")
    for name,(font,size,color) in EXPECTED.items():
        st=doc.styles[name]
        f=st.font
        if f.name and f.name != font:
            errors.append(f"{name} font {f.name} != {font}")
        if f.size and abs(f.size.pt-size)>.1:
            errors.append(f"{name} size {f.size.pt} != {size}")
        if color and rgb(f) and rgb(f).upper()!=color:
            errors.append(f"{name} color {rgb(f)} != {color}")
    header=' '.join(p.text for p in sec.header.paragraphs).strip()
    footer=' '.join(p.text for p in sec.footer.paragraphs).strip()
    if 'Prospect Intelligence Book' not in header:
        errors.append('Header missing Prospect Intelligence Book')
    if 'Uso interno comercial' not in footer:
        errors.append('Footer missing Uso interno comercial')
    for i,t in enumerate(doc.tables):
        if not t.rows:
            continue
        for c in t.rows[0].cells:
            shd=c._tc.get_or_add_tcPr().find(qn('w:shd'))
            fill=shd.get(qn('w:fill')) if shd is not None else None
            if fill and fill.upper()!='1F4E79':
                errors.append(f"Table {i} header fill {fill} != 1F4E79")
    if errors:
        print('FAIL: VISUAL_SYSTEM_GATE')
        for e in errors:
            print('-',e)
        raise SystemExit(1)
    print('PASS: VISUAL_SYSTEM_GATE')

if __name__=='__main__':
    if len(sys.argv)!=2:
        print('usage: validate_handoff_visual.py report.docx')
        raise SystemExit(2)
    main(sys.argv[1])
