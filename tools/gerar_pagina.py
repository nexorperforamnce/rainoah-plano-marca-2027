"""Gera o index.html (apresentação navegável) a partir dos arquivos em project/.

Uso: python tools/gerar_pagina.py
A página não inclui as notas do apresentador (<aside>).
"""
import json
import pathlib
import re

raiz = pathlib.Path(__file__).resolve().parent.parent
deck = json.loads((raiz / "project/deck.json").read_text(encoding="utf-8"))
css = (raiz / "project/deck.css").read_text(encoding="utf-8")

# id da imagem no claude.ai -> arquivo em assets/prints/
mapa = {}
for linha in (raiz / "assets/mapa-de-imagens.md").read_text(encoding="utf-8").splitlines():
    m = re.match(r"\|\s*([0-9a-f]{32})\s*\|\s*(\S+)\s*\|", linha)
    if m:
        mapa[m.group(1)] = m.group(2)

fontes = "\n".join(
    f'<link rel="stylesheet" href="{f["href"]}">' for f in deck["faces"].values() if "href" in f
)

slides = []
for sid in deck["order"]:
    texto = (raiz / f"project/slides/{sid}.html").read_text(encoding="utf-8")
    texto = re.sub(r"<aside>.*?</aside>", "", texto, flags=re.S)
    texto = re.sub(r"/_blob/([0-9a-f]{32})", lambda m: "assets/prints/" + mapa[m.group(1)], texto)
    texto = texto.replace("<a href=", '<a target="_blank" rel="noopener" href=')
    slides.append(f'<div class="slide" id="s-{sid}">\n{texto.strip()}\n</div>')

extra = """
html,body{margin:0;height:100%;background:#0B151C}
body{display:flex;align-items:center;justify-content:center;overflow:hidden}
body.lista{display:block;overflow:auto;padding:12px 0}
body.lista .slide{margin:0 auto 12px;display:block}
body:not(.lista) .slide{display:none}
body:not(.lista) .slide.on{display:block}
.slide{position:relative;overflow:hidden}
.slide>section{width:1920px;height:1080px;box-sizing:border-box;position:relative;overflow:hidden;transform-origin:0 0}
h1,h2,h3,p,ul{margin:0}
ul{padding-left:44px}
li{margin-top:8px}
x-shape{display:block}
x-shape[kind="arrow-down"]{clip-path:polygon(32% 0,68% 0,68% 52%,100% 52%,50% 100%,0 52%,32% 52%)}
table{border-collapse:collapse;width:100%}
th,td{padding:.35em .6em;text-align:left;border:1px solid #CFC7B5;vertical-align:top}
th{background:#E4DED0;font-weight:600}
a{color:inherit;text-decoration:underline}
img{display:block}
#ct{position:fixed;right:14px;bottom:10px;font:600 14px Inter,Arial,sans-serif;color:#B9C8D2;background:rgba(11,21,28,.7);padding:4px 10px;border-radius:12px;z-index:5}
body.lista #ct{display:none}
#dica{position:fixed;left:14px;bottom:10px;font:14px Inter,Arial,sans-serif;color:#B9C8D2;opacity:.8;z-index:5}
body.lista #dica{display:none}
"""

js = """
const slides=[...document.querySelectorAll('.slide')];
let i=0;
function ajustar(){
  const lista=innerWidth<innerHeight*0.9;
  document.body.classList.toggle('lista',lista);
  const s=lista?(innerWidth-24)/1920:Math.min(innerWidth/1920,innerHeight/1080);
  slides.forEach(el=>{
    el.style.width=(1920*s)+'px';el.style.height=(1080*s)+'px';
    el.firstElementChild.style.transform='scale('+s+')';
  });
}
function ir(n){
  i=Math.max(0,Math.min(slides.length-1,n));
  slides.forEach((el,k)=>el.classList.toggle('on',k===i));
  document.getElementById('ct').textContent=(i+1)+' / '+slides.length;
  history.replaceState(null,'','#'+(i+1));
}
addEventListener('resize',ajustar);
addEventListener('keydown',e=>{
  if(['ArrowRight','PageDown',' ','Enter'].includes(e.key)){e.preventDefault();ir(i+1);}
  else if(['ArrowLeft','PageUp','Backspace'].includes(e.key)){e.preventDefault();ir(i-1);}
  else if(e.key==='Home')ir(0);
  else if(e.key==='End')ir(slides.length-1);
  else if(e.key==='f'||e.key==='F'){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();}
});
addEventListener('click',e=>{
  if(document.body.classList.contains('lista')||e.target.closest('a'))return;
  ir(e.clientX<innerWidth*0.3?i-1:i+1);
});
let x0=null;
addEventListener('touchstart',e=>{x0=e.touches[0].clientX;},{passive:true});
addEventListener('touchend',e=>{
  if(x0===null||document.body.classList.contains('lista'))return;
  const dx=e.changedTouches[0].clientX-x0;
  if(Math.abs(dx)>50)ir(dx<0?i+1:i-1);
  x0=null;
});
ajustar();
ir((parseInt(location.hash.slice(1))||1)-1);
"""

pagina = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{deck["title"]}</title>
{fontes}
<style>
{css}
{extra}
</style>
</head>
<body>
{chr(10).join(slides)}
<div id="ct"></div>
<div id="dica">← → para navegar · F para tela cheia</div>
<script>
{js}
</script>
</body>
</html>
"""
(raiz / "index.html").write_text(pagina, encoding="utf-8")
(raiz / ".nojekyll").write_text("", encoding="utf-8")
print("index.html gerado com", len(slides), "slides")
