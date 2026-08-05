#!/usr/bin/env python3
"""Convert a structured Walker DOCX to this app's multi-book data file."""
import argparse, html, json, re, unicodedata
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

PAGE = re.compile(r"^\[(\d{1,4}|[ivxlcdm]+)\]$", re.I)
RUNNING_HEADINGS = {"contents"}

def slug(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:90] or "section"

def rich(p):
    out=[]
    for r in p.runs:
        s=html.escape(r.text, quote=False).replace("\n","<br>")
        if not s: continue
        if r.bold: s=f"<strong>{s}</strong>"
        if r.italic: s=f"<em>{s}</em>"
        if r.underline: s=f"<u>{s}</u>"
        if r.font.superscript: s=f"<sup>{s}</sup>"
        if r.font.subscript: s=f"<sub>{s}</sub>"
        out.append(s)
    return "".join(out)

def body(doc):
    for node in doc.element.body.iterchildren():
        if node.tag == qn("w:p"): yield Paragraph(node, doc)
        elif node.tag == qn("w:tbl"): yield Table(node, doc)

def convert(path, a):
    doc=Document(path); a.images.mkdir(parents=True, exist_ok=True); rels={}
    for n,(rid,rel) in enumerate(((k,v) for k,v in doc.part.rels.items() if "image" in v.reltype),1):
        ext=Path(rel.target_part.partname).suffix or ".png"; name=f"{a.slug}-{n}{ext}"
        (a.images/name).write_bytes(rel.target_part.blob); rels[rid]=f"assets/images/{name}"
    blocks=[]; toc=[]; used={}; running_sections={}; page=None; section=""
    for item in body(doc):
        if isinstance(item, Paragraph):
            text=" ".join(item.text.split()); pm=PAGE.fullmatch(text)
            if pm:
                marker = pm.group(1)
                page = int(marker) if marker.isdigit() else marker.lower()
                blocks.append({"type":"page","page":page}); continue
            style=item.style.name if item.style else "Normal"; hm=re.match(r"Heading\s+(\d+)",style)
            if hm and text:
                title=text.rstrip("."); base=slug(title)
                if base in RUNNING_HEADINGS and base in running_sections:
                    # A running heading may be repeated at the top of every
                    # printed contents page. Keep those pages in one section.
                    section=running_sections[base]
                    continue
                used[base]=used.get(base,0)+1
                section=base if used[base]==1 else f"{base}-{used[base]}"
                if base in RUNNING_HEADINGS: running_sections[base]=section
                b={"type":"heading","level":int(hm.group(1)),"id":section,"text":title,"html":rich(item),"page":page}
                blocks.append(b); toc.append({k:b[k] for k in ("level","id","text","page")})
            elif text: blocks.append({"type":"paragraph","html":rich(item) or html.escape(text),"text":text,"page":page,"section":section})
            for blip in item._p.xpath(".//a:blip"):
                src=rels.get(blip.get(qn("r:embed")))
                if src: blocks.append({"type":"image","src":src,"alt":f"Figure from {a.short_title}","page":page})
        else:
            rows=[["<br>".join(rich(p) for p in c.paragraphs) for c in row.cells] for row in item.rows]
            blocks.append({"type":"table","rows":rows,"page":page})
    return {"id":a.slug,"title":a.title,"shortTitle":a.short_title,"author":a.author,"year":a.year,"edition":a.edition,"description":a.description,"sourceFile":path.name,"blocks":blocks,"toc":toc}

def main():
    p=argparse.ArgumentParser(); p.add_argument("document",type=Path); p.add_argument("--output",type=Path,required=True); p.add_argument("--images",type=Path,required=True)
    for x in ("slug","title","short-title"): p.add_argument(f"--{x}",required=True)
    p.add_argument("--author",default="John Walker"); p.add_argument("--year",default="1822"); p.add_argument("--edition",default=""); p.add_argument("--description",default=""); p.add_argument("--append",action="store_true")
    a=p.parse_args(); book=convert(a.document,a); library=[]
    if a.append and a.output.exists():
        m=re.search(r"window\.WALKER_BOOKS\s*=\s*(\[.*\]);?\s*$",a.output.read_text(encoding="utf-8"),re.S)
        if m: library=[b for b in json.loads(m.group(1)) if b.get("id")!=book["id"]]
    library.append(book); a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text("/* Generated from source DOCX files. */\nwindow.WALKER_BOOKS = "+json.dumps(library,ensure_ascii=False,separators=(",",":"))+";\n",encoding="utf-8")
    print(f"Wrote {len(library)} book(s), {len(book['blocks'])} blocks, {len(book['toc'])} headings")
if __name__=="__main__": main()
