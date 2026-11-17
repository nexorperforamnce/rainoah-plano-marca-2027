# Rainoah — Plano de Marca 2027

Cópia versionada dos arquivos-fonte da apresentação **"Rainoah — Plano de Marca 2027"** (32 slides), feita em 16/11/2026.

**Apresentação online (abre como link):** https://nexorperforamnce.github.io/rainoah-plano-marca-2027/
Setas do teclado ou toque para trocar de slide, tecla F para tela cheia.

A versão editável, com as notas do apresentador, fica em: https://claude.ai/artifact/PSjpAnXWTbTMc7nDovNtnt (privada, só abre na conta que a criou).

> **Repositório público.** Os slides trazem dados internos da Rainoah (auditorias de Instagram e resumos de reuniões), e qualquer pessoa com o link consegue ver esse conteúdo.

## Estrutura

```
project/
  deck.json          índice do deck: título, ordem dos slides, seções e fontes
  deck.css           estilo compartilhado por todos os slides
  slides/<id>.html   um arquivo por slide; as notas do apresentador ficam no <aside>
assets/
  prints/            prints dos posts de referência (01 a 21)
  mapa-de-imagens.md qual arquivo de print corresponde a cada imagem usada nos slides
```

A ordem dos slides está em `project/deck.json`, no campo `order`.

## Como as imagens funcionam

Nos slides, as imagens aparecem como `/_blob/<id>`. Esse endereço só existe dentro do claude.ai, onde as imagens foram enviadas. Os mesmos arquivos estão em `assets/prints/`, e o `assets/mapa-de-imagens.md` diz qual id é qual arquivo.

## Limites desta cópia

- O `index.html` é uma página de apresentação gerada a partir dos arquivos de `project/` (rode `python tools/gerar_pagina.py`). Ela não inclui as notas do apresentador.
- Para atualizar o deck, edite o conteúdo no próprio claude.ai, copie os arquivos de novo para cá e gere o `index.html` outra vez.
- Números e prints são do Instagram em 16/11/2026 e mudam com o tempo.

## Fontes dos dados

- Auditorias de Instagram de @rainoahbemestar e @rainoah_empreendedor (31/10/2026).
- Resumos das reuniões de 5 e 6/11/2026.
- Perfis e posts públicos do Instagram, com link no rodapé de cada slide de referência.
