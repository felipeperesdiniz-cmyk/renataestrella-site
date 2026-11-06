#!/usr/bin/env python3
"""Generates the static site. Run from the project root: python3 _src/build.py"""
import json, os, math, re
from urllib.parse import quote

BASE = 'https://renataestrellapatisserie.com'
LASTMOD = '2026-11-04'
TEL = '+55-21-99982-1270'
EMAIL = 'renatacodina@gmail.com'
IG = 'https://www.instagram.com/renataestrella.patisserie/'
DIMS = json.load(open('_src/dims.json'))
import hashlib
ASSET_V = hashlib.md5(open('assets/site.css', 'rb').read() + open('assets/site.js', 'rb').read()).hexdigest()[:8]
WA = 'https://wa.me/5521999821270?text=' + quote('Olá, Renata! Gostaria de um orçamento para um evento.')
WA_NATAL = 'https://wa.me/5521999821270?text=' + quote('Olá, Renata! Gostaria de fazer uma encomenda do cardápio de Natal.')
WA_MENU = 'https://wa.me/5521999821270?text=' + quote('Olá, Renata! Pode me enviar o cardápio completo com valores?')
EXT = 'target="_blank" rel="noopener"'


def img(name, sizes='100vw', alt='', lazy=True, cls=''):
    d = DIMS[name]
    ws = d['w']
    w, h = d['r']
    mid = ws[min(1, len(ws) - 1)]
    src = ', '.join(f'/assets/img/{name}-{x}.webp {x}w' for x in ws)
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high"'
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} src="/assets/img/{name}-{mid}.webp" srcset="{src}" sizes="{sizes}" width="{w}" height="{h}" {load} alt="{alt}">'


def vid(name, alt, w=720, h=1280):
    return (f'<video data-auto muted loop playsinline preload="none" width="{w}" height="{h}" poster="/assets/video/{name}.webp" aria-label="{alt}">'
            f'<source src="/assets/video/{name}.mp4" type="video/mp4"></video>')


NAV = [('/trabalhos/', 'Trabalhos'), ('/cardapio/', 'Cardápio'), ('/cardapio-de-natal/', 'Natal'), ('/bolo-de-casamento-rio-de-janeiro/', 'Casamentos'),
       ('/doces-para-eventos-rio-de-janeiro/', 'Eventos'), ('/renata-estrella/', 'A Renata'),
       ('/perguntas-frequentes/', 'Perguntas'), ('/contato/', 'Contato')]

BUSINESS = {
    '@type': ['Bakery', 'LocalBusiness'], '@id': BASE + '/#negocio', 'name': 'Renata Estrella Pâtisserie',
    'alternateName': 'Renata Estrella', 'url': BASE + '/', 'telephone': TEL, 'email': EMAIL,
    'description': 'Confeitaria artesanal sob encomenda no Rio de Janeiro. Bolos, mesas de doces, brigadeiros belgas, macarons e sobremesas para casamentos, festas e eventos corporativos. Ateliê na Barra da Tijuca.',
    'image': BASE + '/assets/og.jpg', 'logo': BASE + '/assets/logo.png',
    'address': {'@type': 'PostalAddress', 'addressLocality': 'Rio de Janeiro', 'addressRegion': 'RJ', 'addressCountry': 'BR', 'streetAddress': 'Barra da Tijuca'},
    'areaServed': [{'@type': 'City', 'name': 'Rio de Janeiro'}, {'@type': 'Country', 'name': 'Brasil'}],
    'servesCuisine': ['Confeitaria', 'Pâtisserie'], 'hasMenu': BASE + '/cardapio/', 'paymentAccepted': 'Pix, depósito bancário',
    'founder': {'@id': BASE + '/renata-estrella/#pessoa'}, 'sameAs': [IG],
    'contactPoint': {'@type': 'ContactPoint', 'telephone': TEL, 'contactType': 'customer service', 'availableLanguage': 'Portuguese', 'contactOption': []},
}
BUSINESS['contactPoint'].pop('contactOption')
PERSON = {
    '@type': 'Person', '@id': BASE + '/renata-estrella/#pessoa', 'name': 'Renata Estrella', 'jobTitle': 'Chef pâtissière',
    'url': BASE + '/renata-estrella/', 'image': BASE + '/assets/img/renata-estrella-dolma-ferrandi-chocolate-801.webp',
    'alumniOf': [{'@type': 'EducationalOrganization', 'name': 'Le Cordon Bleu'}, {'@type': 'EducationalOrganization', 'name': 'Ferrandi Paris'}, {'@type': 'EducationalOrganization', 'name': 'École Ritz Escoffier'}],
    'knowsAbout': ['Pâtisserie', 'Confeitaria', 'Chocolate belga', 'Bolos de casamento', 'Mesas de doces'],
    'worksFor': {'@id': BASE + '/#negocio'}, 'sameAs': [IG],
}
SITE = {'@type': 'WebSite', '@id': BASE + '/#site', 'url': BASE + '/', 'name': 'Renata Estrella Pâtisserie', 'inLanguage': 'pt-BR', 'publisher': {'@id': BASE + '/#negocio'}}


def crumbs_ld(path, title):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': BASE + '/'},
        {'@type': 'ListItem', 'position': 2, 'name': title, 'item': BASE + path}]}


def crumbs(title):
    return f'<nav class="crumb cap" aria-label="Você está em"><ol><li><a href="/">Início</a></li><li aria-current="page">{title}</li></ol></nav>'


def service_ld(name, desc, path):
    return {'@type': 'Service', 'name': name, 'description': desc, 'url': BASE + path, 'provider': {'@id': BASE + '/#negocio'},
            'areaServed': {'@type': 'City', 'name': 'Rio de Janeiro'}}


FOOT_END = f'''<div class="ft grid">
    <nav aria-label="Rodapé">{''.join(f'<a href="{h}">{t}</a>' for h, t in NAV)}</nav>
    <address>Renata Estrella Pâtisserie<br>Ateliê na Barra da Tijuca, Rio de Janeiro, RJ<br><a href="tel:+5521999821270">(21) 99982-1270</a> · <a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="{IG}" {EXT}>Instagram</a></address>
    <p class="ft__c">© 2026 Renata Estrella Pâtisserie<br>Site por <a href="https://www.thedinizstudio.com/pt" {EXT}>The Diniz Studio</a></p>
  </div>'''


def end(title='Conte a sua data.', lead='Envie a data, o número de convidados e o que você imagina. A resposta vem pelo WhatsApp.'):
    return f'''<footer>
  <section class="end">
    <h2>{title}</h2>
    <p class="end__p">{lead}</p>
    <a class="btn" href="{WA}" {EXT}>Pedir orçamento no WhatsApp</a>
  </section>
  {FOOT_END}
</footer>'''


def shell(path, title, desc, main, lds=(), motion=False, og=None, preload='', foot=None):
    graph = [BUSINESS, SITE] + list(lds)
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, separators=(',', ':'))
    head_motion = "<script>document.documentElement.classList.add('js')</script>"
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{BASE}{path}">
<link rel="alternate" hreflang="pt-BR" href="{BASE}{path}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1">
<meta name="author" content="Renata Estrella">
<meta name="geo.region" content="BR-RJ"><meta name="geo.placename" content="Rio de Janeiro">
<meta name="theme-color" content="#F1EDE6">
<meta property="og:type" content="website"><meta property="og:locale" content="pt_BR"><meta property="og:site_name" content="Renata Estrella Pâtisserie">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{BASE}{path}">
<meta property="og:image" content="{BASE}/assets/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="A chef Renata Estrella derramando chocolate em sua cozinha">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{BASE}/assets/og.jpg">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/italiana-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/host-grotesk-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
{preload}{head_motion}
<link rel="stylesheet" href="/assets/site.css?v={ASSET_V}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<header class="hd">
  <a class="brand" href="/" aria-label="Renata Estrella Pâtisserie, início"><i></i><span>Renata Estrella</span></a>
  <nav aria-label="Principal">{''.join(f'<a href="{h}">{t}</a>' for h, t in NAV[:6])}</nav>
  <a class="hd__cta" href="{WA}" {EXT}>Pedir orçamento</a>
  <button class="burger" id="burger" aria-expanded="false" aria-controls="ov">Menu</button>
</header>
<div class="ov" id="ov">{''.join(f'<a href="{h}">{t}</a>' for h, t in NAV)}</div>
<main id="conteudo">
{main}
</main>
{foot if foot is not None else end()}
<script src="/assets/site.js?v={ASSET_V}" defer></script>
</body>
</html>
'''


STAR_D = 'M50 0C53 30 70 47 100 50C70 53 53 70 50 100C47 70 30 53 0 50C30 47 47 30 50 0Z'


def star(color):
    return f'<svg class="star" viewBox="0 0 100 100" aria-hidden="true"><path fill="{color}" d="{STAR_D}"/></svg><div class="flood" style="background:{color}" aria-hidden="true"></div>'


# ------------------------------------------------------------------ HOME
HERO_IMG = 'renata-estrella-chef-patissiere-chocolate-belga'
HERO_DESK = 'renata-estrella-chef-patissiere-chocolate-belga-cozinha'
MENU_ROWS = [('brigadeiros', 'Brigadeiros', 'Belgas ao leite, branco, 70%, gold e rose; trufas com praliné de pistache e avelã'),
             ('doces', 'Doces finos', 'Crème brûlée, cocadinha cremosa, flor de pistache, nozes crocantes'),
             ('macarons-e-brownies', 'Macarons e brownies', 'Macarons por unidade e brownies belgas recheados'),
             ('bolos', 'Bolos', 'Espatulados ou naked, com massa branca, chocolate ou red velvet'),
             ('sobremesas', 'Sobremesas', 'Pavlova de morangos, tartaletes, mil-folhas, charlotes, Floresta Negra'),
             ('cha-e-cafe', 'Chá e café', 'Bolos de chá, madeleines, quiches e alumettes')]


def F(cls, media):
    return f'<figure class="{cls}" data-r>{media}</figure>'


def event(anchor, name, tag, text, figs, tagname='h3', link=True, items=None):
    more = f'<a class="more" href="/trabalhos/#{anchor}">Ver o trabalho completo</a>' if link else ''
    lst = f'<ul class="ev__l">{"".join(f"<li>{x}</li>" for x in items)}</ul>' if items else ''
    return f"""<article class="ev" id="{anchor}">
    <div class="ev__h grid" data-r><{tagname}>{name}</{tagname}><div class="ev__t"><p class="ev__tag">{tag}</p><p>{text}</p>{lst}{more}</div></div>
    <div class="ev__m">{''.join(figs)}</div>
  </article>"""


I_ = lambda n, s, a: img(n, s, a)
S12, S8, S6, S4, S3 = '(max-width:760px) 100vw, 100vw', '(max-width:760px) 100vw, 66vw', '(max-width:760px) 100vw, 50vw', '(max-width:760px) 100vw, 33vw', '(max-width:760px) 50vw, 25vw'
CAS_VID = vid('mesa-de-doces-casamento', 'Vídeo da mesa de doces de um casamento: brigadeiros, beijinhos e flores brancas', 1024, 576)
FIG = {
 'ct_ap': F('x8 l32', I_('aparador-doces-flores-casa-tua', S8, 'Aparador com doces, velas e arranjo de flores vermelhas no jantar Casa Tua')),
 'ct_ro': F('x4 f', I_('doces-em-forma-de-rosa-prato-de-vidro', S4, 'Doces artesanais em forma de rosa em um prato de vidro')),
 'ct_do': F('x4 p45', I_('doces-dourados-taca-de-cristal', S4, 'Doces dourados em uma taça de cristal')),
 'ct_ca': F('x4 p45', I_('cartao-de-lugar-casa-tua', S4, 'Cartão Casa Tua sobre o prato, com flores secas')),
 'ct_me': F('x4 p45', I_('mesa-jantar-casa-tua-velas', S4, 'Mesa posta com velas e flores vermelhas no jantar Casa Tua')),
 'cm_vi': F('x8 l169', CAS_VID),
 'cm_fl': F('x4 f', I_('flores-e-doces-casamento', S4, 'Doces em taças de vidro entre flores brancas e verdes')),
 'cm_be': F('x4 p45', I_('beijinhos-casamento', S4, 'Beijinhos de coco em um prato de vidro')),
 'cm_tr': F('x4 p45', I_('trufas-de-chocolate-casamento', S4, 'Trufas de chocolate polvilhadas com cacau')),
 'cm_ca': F('x4 p45', I_('doces-de-caramelo-casamento', S4, 'Doces de caramelo em fileiras')),
 'cb_fl': F('x7 p45', I_('doces-flor-carol-bassi-10-anos', '(max-width:760px) 100vw, 58vw', 'Docinhos em forminhas de flor em bandejas douradas, festa de 10 anos Carol Bassi')),
 'cb_ta': F('x5 f', I_('taca-personalizada-carol-bassi-10-anos', '(max-width:760px) 100vw, 42vw', 'Taças personalizadas com o logo Carol Bassi 10 anos')),
 'dd_pi': F('x3 p45', I_('macarons-e-joias-dassa-danna', S3, 'Pilha de macarons com anéis de diamante')),
 'dd_pu': F('x3 p45', I_('macarons-pastel-pulseira-dassa-danna', S3, 'Macarons em tons pastel com uma pulseira de pedras')),
 'dd_jo': F('x3 p45', I_('macarons-e-joias-coloridas-dassa-danna', S3, 'Macarons coloridos com joias de pedras')),
 'dd_an': F('x3 p45', I_('macarons-e-aneis-dassa-danna', S3, 'Macarons empilhados com anéis')),
 'jp_bo': F('x8 l32', I_('bolo-monograma-jantar-privado', S8, 'Bolo branco com monograma entre velas')),
 'jp_mo': F('x4 f', I_('monograma-bolo-detalhe', S4, 'Detalhe do monograma no bolo')),
 'jp_ve': F('x6 l32', I_('bolo-monograma-velas-jantar', S6, 'Bolo e doces entre velas altas em uma sala de tijolo aparente')),
 'jp_me': F('x6 l32', I_('jantar-privado-mesa-longa', S6, 'Mesa longa posta para um jantar privado')),
}
HOME_EVENTS = ''.join([
 event('casa-tua', 'Casa Tua', 'Jantar à luz de velas', 'A mesa de doces ocupou um aparador de madeira, entre velas e um grande arranjo de flores vermelhas. Havia bolo com flores, doces em forma de rosa, doces em forma de flor e doces dourados em taças de cristal.', [FIG[k] for k in ('ct_ap', 'ct_ro', 'ct_do', 'ct_ca', 'ct_me')]),
 event('casamento', 'Casamento', 'Mesa de doces e bolo em andares', 'Uma mesa longa sob lustres de cristal, com bolo branco em andares e arranjos de flores brancas e verdes. Os doces vieram em taças e pratos de vidro: brigadeiros, beijinhos, trufas, crème brûlée e caramelo.', [FIG[k] for k in ('cm_vi', 'cm_fl', 'cm_be', 'cm_tr', 'cm_ca')]),
 event('carol-bassi', 'Carol Bassi, 10 anos', 'Festa de marca', 'Para os 10 anos da Carol Bassi, os docinhos vieram em forminhas de flor, em tons de rosa, sobre bandejas douradas. As taças levaram o nome da marca.', [FIG[k] for k in ('cb_fl', 'cb_ta')]),
 event('dassa-danna', 'Dassa Danna', 'Ensaio de joias', 'Macarons em tons pastel para um ensaio da joalheria: anéis entre as camadas e pulseiras sobre os doces.', [FIG[k] for k in ('dd_pi', 'dd_pu', 'dd_jo', 'dd_an')]),
 event('jantar-privado', 'Jantar privado', 'Bolo com monograma', 'Bolo branco com monograma em uma sala de tijolo aparente, com velas altas, folhagens e doces em taças ao redor.', [FIG[k] for k in ('jp_bo', 'jp_mo', 'jp_ve', 'jp_me')]),
])

home = f"""<section class="hero" aria-labelledby="h1">
  <div class="hero__m"><picture><source media="(min-width:861px)" srcset="{', '.join(f'/assets/img/{HERO_DESK}-{x}.webp {x}w' for x in DIMS[HERO_DESK]['w'])}" sizes="72vw" width="{DIMS[HERO_DESK]['r'][0]}" height="{DIMS[HERO_DESK]['r'][1]}">{img(HERO_IMG, '100vw', 'A chef Renata Estrella, de dólmã branco, derrama chocolate de uma espátula em sua cozinha', lazy=False)}</picture></div>
  <div class="hero__c">
    <p class="hero__k">Pâtisserie <span aria-hidden="true">·</span> Rio de Janeiro</p>
    <p class="wm" aria-label="Renata Estrella"><span aria-hidden="true">Renata</span> <span aria-hidden="true">Estrella</span></p>
    <div class="hero__f">
      <h1 id="h1">Doces, bolos e sobremesas sob encomenda para casamentos, festas e eventos no Rio de Janeiro.</h1>
      <p class="hero__p">Chef formada em Paris pela Ferrandi, Ritz Escoffier e Le Cordon Bleu.</p>
    </div>
  </div>
</section>

<section class="intro sect grid" aria-label="Sobre o ateliê">
  <p class="intro__l m-mute">Ateliê na Barra da Tijuca</p>
  <p data-r>Renata Estrella Pâtisserie é uma confeitaria artesanal no Rio de Janeiro. Tudo é produzido no ateliê, sob encomenda, com técnica aprendida em Paris e seleção rigorosa de ingredientes.</p>
</section>

<section class="film sect grid" aria-labelledby="film">
  <div class="film__t" data-r>
    <h2 id="film">Uma pavlova de morangos, do começo ao fim.</h2>
    <p>Neste vídeo, a Renata faz uma pavlova na própria cozinha: bate o merengue, desenha a base com a manga de confeitar, leva ao forno, cobre com creme e coloca os morangos um a um.</p>
    <p>A pavlova de morangos está no <a href="/cardapio/#sobremesas">cardápio de sobremesas</a>, feita sob encomenda.</p>
  </div>
  <figure class="film__v" data-r>{vid('renata-estrella-pavlova-de-morangos', 'Renata Estrella preparando uma pavlova de morangos, do merengue ao prato')}<button class="vbtn" type="button">Pausar</button></figure>
</section>

<section class="sect" aria-labelledby="trab">
  <div class="sh"><h2 id="trab">Trabalhos</h2><a class="more" href="/trabalhos/">Ver todos</a></div>
  {HOME_EVENTS}
</section>

<section class="nt sect" aria-labelledby="natal">
  <div class="ev__h grid" data-r><h2 id="natal">Cardápio de Natal</h2><div class="ev__t"><p class="ev__tag">Sobremesas e presentes</p><p>Bolo Pinheiro, Bûche de Noël, pavlovas, tartaletes, casinhas de noz-pecan e caixas de brigadeiros belgas, sob encomenda para o Natal no Rio de Janeiro.</p><a class="more" href="/cardapio-de-natal/">Ver o cardápio de Natal</a></div></div>
  <div class="ev__m">{F('x3 s11', I_('natal-bolo-pinheiro', S3, 'Bolo Pinheiro de Natal com açúcar de confeiteiro e calda'))}{F('x3 s11', I_('natal-buche-de-noel', S3, 'Bûche de Noël coberta de chocolate'))}{F('x3 s11', I_('presente-natal-casinha-single-noz-pecan', S3, 'Casinha de Natal com noz-pecan caramelizada'))}{F('x3 s11', I_('presente-natal-caixas-trilogia', S3, 'Caixas trilogia com brigadeiros belgas em formato de Natal'))}</div>
</section>

<section class="sect grid" aria-labelledby="card">
  <div class="mn__l" data-r>
    <h2 id="card">Cardápio</h2>
    <figure>{vid('madeleine-com-chocolate', 'Madeleine aberta com as mãos, com recheio de chocolate', 464, 832)}</figure>
  </div>
  <div class="mn__r" data-r>
    {''.join(f'<a class="row" href="/cardapio/#{s}"><h3>{t}</h3><p>{d}</p></a>' for s, t, d in MENU_ROWS)}
    <p class="mn__n">Mínimo de 20 unidades por sabor de doce. Retirada no ateliê. <a href="/cardapio/">Ver cardápio completo</a>.</p>
  </div>
</section>

<section class="rn sect grid" aria-labelledby="ren">
  <figure data-r>{img('renata-estrella-chef-patissiere-mesa-de-doces', '(max-width:760px) 100vw, 42vw', 'Renata Estrella de vermelho ao lado de um bolo em uma mesa de doces à noite')}</figure>
  <div class="rn__t" data-r>
    <h2 id="ren">“Minhas lembranças da querida vovó Marilu despertaram minha paixão pela pâtisserie.”</h2>
    <p>Renata Estrella estudou no Le Cordon Bleu, na Ferrandi e na École Ritz Escoffier. Esteve no Salon du Chocolat de Paris em 2024 e tem mais de 8 anos em alta confeitaria.</p>
    <a class="more" href="/renata-estrella/">A história da Renata</a>
  </div>
</section>

<section class="sect" aria-labelledby="como">
  <div class="sh"><h2 id="como">Como funciona um evento</h2></div>
  <ol class="st grid">
    <li data-r><span>1</span><h3>Conversa</h3><p>Você conta a data, o número de convidados e o que imagina.</p></li>
    <li data-r><span>2</span><h3>Proposta</h3><p>A Renata prepara o conceito e o orçamento para aprovação.</p></li>
    <li data-r><span>3</span><h3>Degustação</h3><p>Vocês provam e escolhem os sabores juntos.</p></li>
    <li data-r><span>4</span><h3>Montagem</h3><p>Tudo é feito na semana do evento e montado no local.</p></li>
    <li class="st__n" style="border:0;padding:0;grid-column:1/-1">Casamentos: fale de 6 a 12 meses antes. Festas e eventos corporativos: pelo menos 60 dias. Veja <a href="/bolo-de-casamento-rio-de-janeiro/">casamentos</a> e <a href="/doces-para-eventos-rio-de-janeiro/">eventos</a>.</li>
  </ol>
</section>
"""

faqs = [
    ('Onde fica a Renata Estrella Pâtisserie?', 'O ateliê fica na Barra da Tijuca, no Rio de Janeiro. As encomendas são retiradas lá, com horário marcado. O endereço completo é enviado na confirmação do pedido.'),
    ('O que a Renata Estrella faz?', 'Bolos espatulados e naked, mesas de doces, brigadeiros belgas, macarons, brownies belgas, sobremesas como pavlova e tartalete de morangos, bolos para chá e café, madeleines e quiches, sempre sob encomenda.'),
    ('Com quanto tempo de antecedência devo encomendar?', 'Doces e sobremesas do cardápio: 3 dias úteis, conforme a agenda. Festas e eventos corporativos com mesa completa: pelo menos 60 dias. Casamentos: de 6 a 12 meses, para dar tempo de criar o conceito e fazer a degustação.'),
    ('Qual é o pedido mínimo de doces?', 'O mínimo é de 20 unidades por sabor.'),
    ('Vocês entregam?', 'Encomendas do cardápio são retiradas no ateliê, na Barra da Tijuca, ou enviadas por um Uber chamado pelo cliente. Em eventos contratados, a montagem no local faz parte do projeto.'),
    ('Como funciona o pagamento?', 'Por Pix ou depósito bancário. Não trabalhamos com cartão de crédito. O pedido é confirmado após o envio do comprovante. Em eventos de maior porte, 50% são pagos na reserva e o restante 10 dias antes da data.'),
    ('Quanto custa um bolo de casamento ou uma mesa de doces?', 'Cada evento é orçado à parte, de acordo com a complexidade, o número de convidados e o local. Os valores dos doces e bolos avulsos estão no cardápio completo, enviado pelo WhatsApp.'),
    ('Como funcionam as encomendas de Natal?', 'Os pedidos são confirmados conforme a agenda, com o envio do comprovante de pagamento. A retirada é no ateliê, das 10h às 15h ou em horário agendado. Não há entregas nos dias 22, 23 e 24 de dezembro, e o ateliê não abre no dia 25.'),
    ('Vocês atendem fora do Rio de Janeiro?', 'Sim, em eventos em todo o Brasil e, em projetos especiais, em outros países. Deslocamento e logística entram no orçamento. Já foram feitos eventos no Rio de Janeiro, em Florianópolis, em Trancoso e em Portugal.'),
    ('Existem opções para restrições alimentares?', 'Sim, há opções sem glúten, sem lactose e veganas. Conte as restrições na primeira conversa para que entrem no projeto.'),
    ('Como funciona a criação de um evento?', 'Começa com uma conversa sobre a data, os convidados e a sua ideia. Depois vêm a proposta com o conceito e o orçamento, a degustação e, na semana do evento, a produção e a montagem no local.'),
]


def faq_ld(items):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}


def faq_html(items):
    return '<div class="faq">' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in items) + '</div>'


REL = lambda *ps: '<nav class="rel" aria-label="Veja também">' + ''.join(f'<a href="{h}">{t}</a>' for h, t in ps) + '</nav>'
R_CAS = ('/bolo-de-casamento-rio-de-janeiro/', 'Bolo e mesa de doces para casamento no Rio')
R_EVT = ('/doces-para-eventos-rio-de-janeiro/', 'Doces para festas e eventos corporativos')
R_MEN = ('/cardapio/', 'Cardápio de doces, bolos e sobremesas')
R_TRA = ('/trabalhos/', 'Trabalhos recentes')
R_REN = ('/renata-estrella/', 'A chef Renata Estrella')
R_FAQ = ('/perguntas-frequentes/', 'Perguntas frequentes')
R_CON = ('/contato/', 'Como fazer uma encomenda')
R_NAT = ('/cardapio-de-natal/', 'Cardápio de Natal')

pages = {}
pages['/'] = shell('/', 'Renata Estrella Pâtisserie | Bolos e doces sob encomenda no Rio de Janeiro',
    'Confeitaria artesanal na Barra da Tijuca, Rio de Janeiro. Bolos de casamento, mesas de doces, brigadeiros belgas e macarons sob encomenda, pela chef Renata Estrella, formada em Paris.',
    home, [PERSON, {'@type': 'VideoObject', 'name': 'Renata Estrella prepara uma pavlova de morangos', 'description': 'A chef Renata Estrella faz uma pavlova de morangos, do merengue à finalização com morangos frescos.', 'thumbnailUrl': BASE + '/assets/video/renata-estrella-pavlova-de-morangos.webp', 'contentUrl': BASE + '/assets/video/renata-estrella-pavlova-de-morangos.mp4', 'uploadDate': '2026-06-08', 'duration': 'PT55S', 'inLanguage': 'pt-BR'}, {'@type': 'WebPage', '@id': BASE + '/#pagina', 'url': BASE + '/', 'name': 'Renata Estrella Pâtisserie', 'isPartOf': {'@id': BASE + '/#site'}, 'about': {'@id': BASE + '/#negocio'}, 'primaryImageOfPage': BASE + '/assets/og.jpg'}],
    preload=f'<link rel="preload" as="image" type="image/webp" media="(max-width:860px)" imagesrcset="' + ', '.join(f'/assets/img/{HERO_IMG}-{x}.webp {x}w' for x in DIMS[HERO_IMG]['w']) + '" imagesizes="100vw" fetchpriority="high">\n'
            + f'<link rel="preload" as="image" type="image/webp" media="(min-width:861px)" imagesrcset="' + ', '.join(f'/assets/img/{HERO_DESK}-{x}.webp {x}w' for x in DIMS[HERO_DESK]['w']) + '" imagesizes="72vw" fetchpriority="high">\n',
    foot=end())

# ------------------------------------------------------------------ TRABALHOS
EXTRA = {
 'ct_lo': F('x12 l21', I_('mesa-longa-jantar-casa-tua', S12, 'Mesa longa posta para o jantar Casa Tua, com vista para o jardim')),
 'ct_re': F('x5 p45', I_('renata-estrella-chef-patissiere-mesa-de-doces', '(max-width:760px) 100vw, 42vw', 'Renata Estrella ao lado do bolo no jantar Casa Tua')),
 'ct_ja': F('x7 f', I_('renata-estrella-e-convidada-jantar', '(max-width:760px) 100vw, 58vw', 'Renata Estrella e uma convidada diante da mesa posta')),
 'cm_me': F('x8 l32', I_('mesa-de-doces-casamento-rio-de-janeiro', S8, 'Mesa de doces de casamento com bolo branco em andares sob lustres de cristal')),
 'cm_cr': F('x4 f', I_('creme-brulee-docinhos-casamento', S4, 'Docinhos de crème brûlée com açúcar queimado')),
 'cm_br': F('x4 p45', I_('brigadeiros-belgas-casamento', S4, 'Brigadeiros em um prato de vidro, com flores')),
 'cm_co': F('x4 p45', I_('docinhos-de-coco-e-chocolate-casamento', S4, 'Docinhos de coco com chocolate')),
 'cm_re': F('x4 p45', I_('creme-brulee-prato-redondo-casamento', S4, 'Prato redondo de docinhos de crème brûlée')),
 'jp_vl': F('x6 l32', I_('jantar-privado-mesa-velas', S6, 'Mesa de jantar com velas vista de perto')),
 'jp_na': F('x6 f', I_('bolo-naked-chocolate-belga', S6, 'Bolo naked de chocolate com raspas por cima')),
 'n_ca': F('x3 p45', I_('bolo-casinha-natal', S3, 'Bolo de Natal em forma de casinha em uma caixa vermelha')),
 'n_pa': F('x3 p45', I_('pavlova-de-morangos', S3, 'Pavlova de morangos sobre pano vermelho')),
 'n_mi': F('x3 p45', I_('mini-pavlovas-pascoa', S3, 'Coroa de mini pavlovas com frutas')),
 'n_cx': F('x3 p45', I_('bolo-pascoa-caixa-presente', S3, 'Bolo de Páscoa em caixa transparente com laço')),
}
ALLF = {**FIG, **EXTRA}
PROJ = [
 ('casa-tua', 'Casa Tua', 'Jantar à luz de velas', 'Para este jantar no Rio de Janeiro, a mesa de doces e a mesa posta seguiram a mesma paleta: madeira escura, velas e flores vermelhas. Cada lugar recebeu um cartão com flores secas, e os doces ficaram em um aparador de madeira.', ['Bolo com cobertura dourada e flores', 'Doces em forma de rosa', 'Doces em forma de flor', 'Doces dourados em taças de cristal'], ['ct_ap', 'ct_ro', 'ct_lo', 'ct_do', 'ct_ca', 'ct_me', 'ct_re', 'ct_ja']),
 ('casamento', 'Casamento', 'Mesa de doces e bolo em andares', 'Uma mesa longa, sob lustres de cristal, com o bolo branco em andares no centro. Os doces foram distribuídos em taças e pratos de vidro de alturas diferentes, entre flores brancas e verdes.', ['Bolo branco em andares', 'Brigadeiros', 'Beijinhos', 'Trufas de chocolate', 'Crème brûlée', 'Doce de caramelo', 'Docinhos de coco com chocolate'], ['cm_vi', 'cm_fl', 'cm_me', 'cm_cr', 'cm_be', 'cm_tr', 'cm_ca', 'cm_br', 'cm_co', 'cm_re']),
 ('carol-bassi', 'Carol Bassi, 10 anos', 'Festa de marca', 'Para comemorar os 10 anos da Carol Bassi, os doces entraram na identidade da festa. Os docinhos vieram em forminhas de flor, em tons de rosa, sobre bandejas douradas, e as taças levaram o nome da marca.', ['Docinhos em forminhas de flor', 'Taças personalizadas com a marca'], ['cb_fl', 'cb_ta']),
 ('dassa-danna', 'Dassa Danna', 'Ensaio de joias', 'Macarons feitos para um ensaio da joalheria Dassa Danna. Os doces, em tons pastel, serviram de cenário para as peças: anéis entre as camadas e pulseiras sobre os macarons.', ['Macarons em tons pastel'], ['dd_pi', 'dd_pu', 'dd_jo', 'dd_an']),
 ('jantar-privado', 'Jantar privado', 'Bolo com monograma', 'Um jantar em sala de tijolo aparente, com mesa longa. O bolo branco levou um monograma feito para a ocasião e ficou no centro de um aparador, entre velas altas, folhagens e doces em taças.', ['Bolo branco com monograma', 'Doces em taças', 'Bolo naked de chocolate'], ['jp_bo', 'jp_mo', 'jp_ve', 'jp_me', 'jp_vl', 'jp_na']),
 ('natal-e-pascoa', 'Natal e Páscoa', 'Coleções da temporada', 'Encomendas feitas para as datas do ano, algumas em caixas para presente. Veja o <a href="/cardapio-de-natal/">cardápio de Natal</a> ou pergunte pelas datas da Páscoa pelo WhatsApp.', ['Bolo de Natal em forma de casinha', 'Pavlova de morangos', 'Coroa de mini pavlovas', 'Bolo de Páscoa em caixa para presente'], ['n_ca', 'n_pa', 'n_mi', 'n_cx']),
]
trab = f"""<div class="ph">{crumbs('Trabalhos')}<h1><span class="m-mute">Trabalhos de Renata Estrella.</span><span>Mesas de doces, bolos e sobremesas para casamentos, marcas e jantares no Rio de Janeiro.</span></h1></div>
""" + ''.join(event(s, n, g, d, [ALLF[k] for k in ks], 'h2', False, it) for s, n, g, d, it, ks in PROJ) + REL(R_CAS, R_EVT, R_MEN)
pages['/trabalhos/'] = shell('/trabalhos/', 'Trabalhos: mesas de doces e bolos no Rio de Janeiro | Renata Estrella',
    'Mesas de doces, bolos e sobremesas de Renata Estrella para casamentos, marcas e jantares no Rio de Janeiro: Casa Tua, Carol Bassi, Dassa Danna e outros.',
    trab, [crumbs_ld('/trabalhos/', 'Trabalhos'), {'@type': 'CollectionPage', 'name': 'Trabalhos de Renata Estrella', 'url': BASE + '/trabalhos/', 'about': {'@id': BASE + '/#negocio'}, 'hasPart': [{'@type': 'CreativeWork', 'name': n, 'description': re.sub(r'<[^>]+>', '', d), 'url': f'{BASE}/trabalhos/#{s}', 'creator': {'@id': BASE + '/renata-estrella/#pessoa'}} for s, n, g, d, it, ks in PROJ]}])

# ------------------------------------------------------------------ CARDÁPIO
DISHES = [
 ('brigadeiros', 'Brigadeiros', 'brigadeiros-belgas-casamento', 'Brigadeiros belgas em prato de vidro', 'Feitos com chocolate belga. Mínimo de 20 unidades por sabor.',
  ['Belga ao leite', 'Belga branco', 'Belga 70%', 'Belga gold', 'Belga rose', 'Churros com doce de leite', 'Nutella com avelã', 'Leite Ninho com Nutella', 'Cookies and cream', 'Oreo', 'Limão-siciliano com suspiro', 'Trufas de chocolate belga com praliné de pistache e avelã']),
 ('doces', 'Doces finos', 'creme-brulee-docinhos-casamento', 'Docinhos de crème brûlée', 'Mínimo de 20 unidades por sabor.',
  ['Cocadinha cremosa', 'Crème brûlée', 'Amêndoas laminadas', 'Concha de damasco', 'Doce de caramelo com biscoito amanteigado', 'Romeu e Julieta', 'Flor de pistache', 'Ouriço de pistache', 'Nozes crocantes', 'Mini waffle de Nutella com chocolate']),
 ('macarons-e-brownies', 'Macarons e brownies belgas', 'macarons-pastel-pulseira-dassa-danna', 'Macarons em tons pastel', 'Macarons por unidade, com sabores a consultar. Brownies belgas recheados:',
  ['Chocolate com doce de leite', 'Chocolate com brigadeiro belga', 'Brownie belga branco', 'Brownie belga de limão-siciliano', 'Brownie belga cookies and cream']),
 ('bolos', 'Bolos espatulados ou naked', 'bolo-naked-chocolate-belga', 'Bolo naked de chocolate belga', 'Valores por fatia. Massa branca, de chocolate ou red velvet. Topo de frutas vermelhas, flores ou macarons, cobrado à parte. Recheios:',
  ['Chocolate belga ao leite', 'Chocolate belga branco', 'Limão-siciliano', 'Doce de leite', 'Crème brûlée', 'Nozes', 'Amêndoas']),
 ('sobremesas', 'Sobremesas', 'tartalete-de-morangos', 'Tartalete de morangos', '',
  ['Pavlova de morangos', 'Tartalete de morangos', 'Flor de tartalete de morangos', 'Tartalete de limão-siciliano', 'Mil-folhas de morango', 'Torta de mousse de cacau com tangerina e crumble de amêndoas', 'Charlote de peras, de morangos ou de framboesas', 'Floresta Negra com cerejas', 'Bolo de sorvete com calda quente de chocolate belga e profiteroles']),
 ('cha-e-cafe', 'Chá e café', 'bolo-com-calda-de-doce-de-leite', 'Bolo com calda e açúcar de confeiteiro', 'Para o salgado: quiches de 23 cm e alumettes de massa folhada com grana padano.',
  ['Bolo de cenoura com calda de chocolate belga', 'Bolo de chocolate belga com calda', 'Cinnamon roll cake', 'Bolo de laranja-bahia', 'Bolo de baunilha', 'Bolo fit de cacau 100% Callebaut', 'Madeleines', 'Quiche de três queijos', 'Quiche de alho-poró', 'Quiche de brie com damasco']),
]
card = f'''<div class="ph">{crumbs('Cardápio')}<h1><span class="m-mute">Cardápio de Renata Estrella.</span><span>Brigadeiros belgas, macarons, bolos e sobremesas sob encomenda no Rio de Janeiro.</span></h1></div>
<div class="dishes">''' + ''.join(f'''<section class="dish" id="{s}"><figure>{img(i, '(max-width:760px) 25vw, 16vw', a)}</figure><h2>{t}</h2><div class="dish__b">{f'<p>{n}</p>' if n else ''}<ul>{''.join(f'<li>{x}</li>' for x in it)}</ul></div></section>''' for s, t, i, a, n, it in DISHES) + f'''</div>
<section class="sec" aria-labelledby="como"><h2 id="como">Como encomendar</h2><div class="sec__b"><p>Peça o <a href="{WA_MENU}" {EXT}>cardápio completo com valores pelo WhatsApp</a>. Informe nome, telefone, data e horário da retirada, o pedido e se a retirada será pessoal ou por Uber.</p><ul><li>Antecedência de 3 dias úteis, ou conforme a agenda</li><li>Mínimo de 20 unidades por sabor de doce</li><li>Retirada no ateliê, na Barra da Tijuca, com horário marcado</li><li>Não fazemos entrega; a retirada por Uber fica a cargo do cliente</li><li>Pagamento por Pix ou depósito; o pedido é confirmado com o comprovante</li></ul></div></section>
''' + REL(R_NAT, R_CAS, R_EVT, R_FAQ)
pages['/cardapio/'] = shell('/cardapio/', 'Cardápio: brigadeiros belgas, macarons e bolos sob encomenda | Renata Estrella',
    'Cardápio de Renata Estrella no Rio de Janeiro: brigadeiros belgas, doces finos, macarons, brownies, bolos naked, pavlova, tartaletes e quiches. Retirada na Barra da Tijuca.',
    card, [crumbs_ld('/cardapio/', 'Cardápio'), {'@type': 'Menu', '@id': BASE + '/cardapio/#menu', 'name': 'Cardápio Renata Estrella Pâtisserie', 'url': BASE + '/cardapio/', 'inLanguage': 'pt-BR', 'hasMenuSection': [{'@type': 'MenuSection', 'name': t, 'url': f'{BASE}/cardapio/#{s}', 'hasMenuItem': [{'@type': 'MenuItem', 'name': x} for x in it]} for s, t, _, _, _, it in DISHES]}])

# ------------------------------------------------------------------ NATAL
SOBREM = [
 ('natal-bolo-pinheiro', 'Bolo Pinheiro', 'Uma criação natalina em formato de pinheiro, que une sabor e delicadeza.', '245,00'),
 ('natal-bolo-sorvete', 'Bolo Sorvete', 'Uma sobremesa cremosa e refrescante para os encontros de Natal.', '255,00'),
 ('natal-bolo-casinha-de-chocolate', 'Bolo casinha de chocolate', 'Uma casinha de chocolate com apresentação encantadora. Calda extra de chocolate, 300 ml: R$ 48,00.', '255,00'),
 ('natal-torta-de-coco-gelada', 'Torta de coco gelada', 'Sabor, textura e leveza em uma só sobremesa. Serve de 10 a 12 fatias.', '295,00'),
 ('natal-buche-de-noel', 'Bûche de Noël', 'O tradicional tronco de Natal em uma versão sofisticada.', '310,00'),
 ('natal-pavlova-de-morangos', 'Pavlova de morangos', 'Merengue crocante por fora e macio por dentro, com creme e morangos frescos.', '320,00'),
 ('natal-pavlova-de-frutas-amarelas', 'Pavlova de frutas amarelas', 'A leveza do merengue com a cremosidade e o frescor das frutas amarelas.', '335,00'),
 ('natal-flor-de-tartalete', 'Flor de tartalete', 'Doce e fresca. Rende de 20 a 25 fatias.', '350,00'),
 ('natal-tartalete-de-morango', 'Tartalete de morango', 'Massa pâte sucré com creme delicado de baunilha e morangos frescos. Rende de 10 a 12 fatias.', '295,00'),
 ('natal-tartalete-de-limao-siciliano', 'Tartalete de limão-siciliano', 'Massa pâte sucré com crème de limão-siciliano e merengue suíço.', '295,00'),
 ('natal-charlotte-de-morangos', 'Charlotte de morangos', 'Uma sobremesa elegante, com morangos e cremosidade, para a sua mesa natalina.', '350,00'),
 ('natal-torta-de-noz-pecan', 'Torta de noz-pecan', 'Massa crocante e amanteigada, com recheio cremoso de noz-pecan caramelizada e toque de baunilha.', '320,00'),
]
PRESENTES = [
 ('presente-natal-casinha-ginger', 'Casinha Ginger de noz-pecan caramelizada', 'Uma casinha recheada de nozes-pecan caramelizadas, nas cores branca ou vermelha.', '115,00'),
 ('presente-natal-tubo-lata-brownies', 'Tubo lata com brownies bites', 'Brownies artesanais de chocolate belga em bites, para compartilhar ou presentear. 100 g.', '85,00'),
 ('presente-natal-bolas-brownie-bites', 'Bolas de Natal com brownie bites', 'Bolas artesanais com brownie bites de chocolate belga, para pendurar na árvore. 50 g.', '35,00'),
 ('presente-natal-noel-collection-pao-de-mel', 'Noel Collection', 'O clássico pão de mel artesanal. Receita de família para a sua família.', '52,00'),
 ('presente-natal-casinha-single-noz-pecan', 'Casinha Single de noz-pecan', 'Nozes-pecan crocantes e caramelizadas em uma casinha natalina. 70 g.', '45,00'),
 ('presente-natal-casinha-dupla-emocao', 'Casinha com Dupla Emoção', 'Dois sabores na mesma casinha: Crock Crock com chocolate belga e nuts, e noz-pecan caramelizada.', '88,00'),
 ('presente-natal-caixas-trilogia', 'Caixas trilogia', '6 brigadeiros de pistache em formato de pinheiro, 3 de chocolate ao leite belga em formato de boneco de neve e 3 belgas branco e preto em formato de Papai Noel.', '130,00'),
 ('presente-natal-lata-papai-noel', 'Lata Papai Noel', '12 brigadeiros belgas em formato de Papai Noel.', '79,00'),
]


def nt_cards(items):
    return '<div class="ng">' + ''.join(f"""<article class="nc" data-r><figure>{img(i, '(max-width:760px) 50vw, 33vw', n + ', cardápio de Natal de Renata Estrella')}</figure><h3>{n}</h3><p>{d}</p><p class="nc__p">R$ {pr}</p></article>""" for i, n, d, pr in items) + '</div>'


NT_FAQ = [x for x in faqs if 'Natal' in x[0]]
nat = f"""<div class="ph">{crumbs('Cardápio de Natal')}<h1><span class="m-mute">Cardápio de Natal de Renata Estrella.</span><span>Sobremesas e presentes de Natal sob encomenda no Rio de Janeiro.</span></h1></div>
<section class="nts" aria-labelledby="sob"><div class="sh"><h2 id="sob">Sobremesas</h2><a class="more" href="{WA_NATAL}" {EXT}>Encomendar pelo WhatsApp</a></div>{nt_cards(SOBREM)}</section>
<section class="nts" aria-labelledby="pre"><div class="sh"><h2 id="pre">Presentes</h2><a class="more" href="{WA_NATAL}" {EXT}>Encomendar pelo WhatsApp</a></div>{nt_cards(PRESENTES)}</section>
<section class="sec" aria-labelledby="com"><h2 id="com">Como encomendar no Natal</h2><div class="sec__b"><ul><li>Pedidos confirmados conforme a disponibilidade da agenda, com o envio do comprovante de pagamento</li><li>Retirada no ateliê, na Barra da Tijuca, das 10h às 15h ou em horário agendado</li><li>Entrega mediante consulta, com valor calculado conforme a localidade</li><li>Nos dias 22, 23 e 24 de dezembro, apenas retiradas</li><li>No dia 25 de dezembro, o ateliê não abre</li></ul><p><a class="btn" style="color:var(--paper)" href="{WA_NATAL}" {EXT}>Encomendar pelo WhatsApp</a></p></div></section>
""" + REL(R_MEN, R_TRA, R_CON)
d_nat = 'Cardápio de Natal de Renata Estrella no Rio de Janeiro: Bolo Pinheiro, Bûche de Noël, pavlovas, tartaletes, casinhas de noz-pecan e caixas de brigadeiros belgas, com preços.'
pages['/cardapio-de-natal/'] = shell('/cardapio-de-natal/', 'Cardápio de Natal: sobremesas e presentes no Rio de Janeiro | Renata Estrella', d_nat, nat,
    [crumbs_ld('/cardapio-de-natal/', 'Cardápio de Natal'), faq_ld(NT_FAQ), {'@type': 'Menu', '@id': BASE + '/cardapio-de-natal/#menu', 'name': 'Cardápio de Natal Renata Estrella Pâtisserie', 'url': BASE + '/cardapio-de-natal/', 'inLanguage': 'pt-BR', 'hasMenuSection': [{'@type': 'MenuSection', 'name': sn, 'hasMenuItem': [{'@type': 'MenuItem', 'name': n, 'description': de, 'image': f"{BASE}/assets/img/{i}-1000.webp", 'offers': {'@type': 'Offer', 'price': pr.replace(',', '.'), 'priceCurrency': 'BRL'}} for i, n, de, pr in its]} for sn, its in (('Sobremesas', SOBREM), ('Presentes', PRESENTES))]}])

# ------------------------------------------------------------------ CASAMENTOS
cas_faq = [faqs[2], faqs[6], faqs[8], faqs[9]]
cas = f'''<div class="ph">{crumbs('Casamentos')}<h1><span class="m-mute">Bolo e mesa de doces para casamento no Rio de Janeiro.</span><span>Da primeira conversa à montagem no local, pela chef Renata Estrella.</span></h1></div>
<div class="bleed" data-r>{img('mesa-de-doces-casamento-rio-de-janeiro', '100vw', 'Mesa de doces de casamento no Rio de Janeiro com bolo em andares sob lustres de cristal', lazy=False)}</div>
<section class="sec" aria-labelledby="o-que"><h2 id="o-que">O que entra em um casamento</h2><div class="sec__b"><p>A Renata Estrella cria o bolo e a mesa de doces do casamento a partir da personalidade do casal, do local e do número de convidados. Cada projeto é desenvolvido do zero, sem encomenda padrão.</p><h3>Bolos</h3><p>Bolos espatulados ou naked, com massa branca, de chocolate ou red velvet, e recheios como chocolate belga, limão-siciliano, doce de leite e crème brûlée.</p><h3>Mesa de doces</h3><p>Brigadeiros belgas, trufas com praliné de pistache e avelã, beijinhos, crème brûlée, caramelo com biscoito amanteigado, flores de pistache e macarons. Veja o <a href="/cardapio/">cardápio completo</a>.</p></div></section>
<div class="gal"><figure class="g4 ar-p" data-r>{img('brigadeiros-belgas-casamento', '(max-width:760px) 100vw, 33vw', 'Brigadeiros belgas em prato de vidro em mesa de casamento')}</figure><figure class="g4 ar-p" data-r>{vid('mesa-de-doces-casamento', 'Vídeo de mesa de doces de casamento com flores', 1024, 576)}</figure><figure class="g4 ar-p" data-r>{img('doces-de-caramelo-casamento', '(max-width:760px) 100vw, 33vw', 'Doces de caramelo em mesa de casamento')}</figure></div>
<section class="sec" aria-labelledby="como-c"><h2 id="como-c">Como funciona</h2><div class="sec__b"><ul><li><b>Conversa:</b> você conta a data, o local, o número de convidados e a sua ideia.</li><li><b>Proposta:</b> a Renata prepara o conceito e o orçamento para aprovação.</li><li><b>Degustação:</b> vocês provam e escolhem os sabores juntos.</li><li><b>Produção e montagem:</b> tudo é feito na semana do casamento e montado pela Renata no local.</li></ul><p>Recomendamos o contato de 6 a 12 meses antes. Em casamentos, 50% são pagos na reserva e o restante 10 dias antes da data. <a href="/trabalhos/#casamento">Veja um casamento recente</a>.</p></div></section>
<section class="sec" aria-labelledby="f-c"><h2 id="f-c">Perguntas sobre casamentos</h2><div class="sec__b">{faq_html(cas_faq)}</div></section>
''' + REL(R_TRA, R_MEN, R_REN)
d_cas = 'Bolo de casamento e mesa de doces no Rio de Janeiro pela chef Renata Estrella, formada em Paris. Conceito, degustação e montagem no local. Peça um orçamento.'
pages['/bolo-de-casamento-rio-de-janeiro/'] = shell('/bolo-de-casamento-rio-de-janeiro/', 'Bolo de casamento e mesa de doces no Rio de Janeiro | Renata Estrella', d_cas, cas,
    [crumbs_ld('/bolo-de-casamento-rio-de-janeiro/', 'Casamentos'), service_ld('Bolo e mesa de doces para casamento', d_cas, '/bolo-de-casamento-rio-de-janeiro/'), faq_ld(cas_faq)],
    foot=end('Conte a sua data.', 'Envie a data do casamento, o local e o número de convidados. A resposta vem pelo WhatsApp.'))

# ------------------------------------------------------------------ EVENTOS
evt_faq = [faqs[2], faqs[5], faqs[7]]
evt = f'''<div class="ph">{crumbs('Eventos')}<h1><span class="m-mute">Doces para festas e eventos corporativos no Rio de Janeiro.</span><span>Mesas de doces e peças com a sua marca, feitas sob encomenda.</span></h1></div>
<div class="bleed" data-r>{img('doces-flor-carol-bassi-10-anos', '100vw', 'Doces em forma de flor em bandejas douradas na festa de 10 anos da Carol Bassi', lazy=False)}</div>
<section class="sec" aria-labelledby="ev-a"><h2 id="ev-a">Para marcas e empresas</h2><div class="sec__b"><p>Lançamentos, aniversários de marca, apresentações e confraternizações. A Renata Estrella desenvolve doces personalizados, como as taças com o logo feitas para os <a href="/trabalhos/#carol-bassi">10 anos da Carol Bassi</a> e os macarons do <a href="/trabalhos/#dassa-danna">ensaio de joias da Dassa Danna</a>.</p></div></section>
<div class="gal"><figure class="g5 ar-p" data-r>{img('taca-personalizada-carol-bassi-10-anos', '(max-width:760px) 100vw, 42vw', 'Taças personalizadas com o logo Carol Bassi 10 anos')}</figure><figure class="g7 ar-p" data-r>{img('macarons-e-joias-dassa-danna', '(max-width:760px) 100vw, 58vw', 'Macarons com anéis para ensaio da joalheria Dassa Danna')}</figure></div>
<section class="sec" aria-labelledby="ev-b"><h2 id="ev-b">Para festas e jantares</h2><div class="sec__b"><p>Aniversários, formaturas, jantares em casa e datas especiais. A mesa pode ter brigadeiros belgas, doces finos, macarons, sobremesas e bolo com monograma.</p><p>Para mesas completas, fale com pelo menos 60 dias de antecedência. Para doces avulsos, veja o <a href="/cardapio/">cardápio</a>: basta 3 dias úteis, conforme a agenda.</p></div></section>
<section class="sec" aria-labelledby="f-e"><h2 id="f-e">Perguntas sobre eventos</h2><div class="sec__b">{faq_html(evt_faq)}</div></section>
''' + REL(R_TRA, R_CAS, R_MEN)
d_evt = 'Doces para eventos corporativos, festas e jantares no Rio de Janeiro. Mesas de doces, macarons e peças com a sua marca pela chef Renata Estrella. Peça um orçamento.'
pages['/doces-para-eventos-rio-de-janeiro/'] = shell('/doces-para-eventos-rio-de-janeiro/', 'Doces para eventos e festas no Rio de Janeiro | Renata Estrella', d_evt, evt,
    [crumbs_ld('/doces-para-eventos-rio-de-janeiro/', 'Eventos'), service_ld('Doces para festas e eventos corporativos', d_evt, '/doces-para-eventos-rio-de-janeiro/'), faq_ld(evt_faq)])

# ------------------------------------------------------------------ SOBRE
sob = f'''<div class="ph">{crumbs('A Renata')}<h1><span class="m-mute">Renata Estrella, chef pâtissière.</span><span>Formada no Le Cordon Bleu, na Ferrandi e na École Ritz Escoffier, com ateliê no Rio de Janeiro.</span></h1></div>
<div class="gal"><figure class="g7 ar-l" data-r>{img('renata-estrella-e-convidada-jantar', '(max-width:760px) 100vw, 58vw', 'Renata Estrella em uma mesa de jantar posta com velas', lazy=False)}</figure><figure class="g5 ar-l" data-r>{img('renata-estrella-preparando-bandeja', '(max-width:760px) 100vw, 42vw', 'Renata Estrella arrumando uma bandeja de frutas e doces')}</figure></div>
<section class="sec" aria-labelledby="hist"><h2 id="hist">A história</h2><div class="sec__b"><blockquote>“Minhas lembranças da querida vovó Marilu despertaram minha paixão pela pâtisserie, inspirando-me a buscar excelência.”</blockquote><p>Renata Estrella estudou em escolas internacionais de confeitaria: Le Cordon Bleu, Ferrandi e École Ritz Escoffier. Também esteve no Salon du Chocolat de 2024, em Paris, e no congresso de confeitaria Diego Lozano. São mais de 8 anos em alta confeitaria.</p><blockquote>“O segredo disso tudo é combinar técnicas e alta qualidade dos insumos. Minha maior alegria é o grande privilégio de adoçar seus momentos felizes e tornar sua vida mais saborosa.”</blockquote><p>Hoje, ela produz tudo no próprio ateliê, na Barra da Tijuca, no Rio de Janeiro. Faz <a href="/bolo-de-casamento-rio-de-janeiro/">bolos e mesas de doces para casamentos</a>, <a href="/doces-para-eventos-rio-de-janeiro/">doces para eventos</a> e as encomendas do <a href="/cardapio/">cardápio</a>.</p></div></section>
<div class="gal"><figure class="g4 ar-p" data-r>{img('renata-estrella-cozinha-profissional-chefs', '(max-width:760px) 100vw, 33vw', 'Renata Estrella em cozinha profissional com dois chefs')}</figure><figure class="g4 ar-p" data-r>{img('renata-estrella-certificado-ferrandi-paris', '(max-width:760px) 100vw, 33vw', 'Renata Estrella segurando o certificado, com dólmã da Ferrandi')}</figure><figure class="g4 ar-p" data-r>{img('renata-estrella-dolma-ferrandi-chocolate', '(max-width:760px) 100vw, 33vw', 'Renata Estrella com dólmã da Ferrandi segurando chocolate')}</figure></div>
''' + REL(R_TRA, R_MEN, R_CON)
pages['/renata-estrella/'] = shell('/renata-estrella/', 'Renata Estrella, chef pâtissière no Rio de Janeiro | Formação em Paris',
    'Renata Estrella é chef pâtissière no Rio de Janeiro, formada no Le Cordon Bleu, na Ferrandi e na École Ritz Escoffier. Conheça a história e o ateliê na Barra da Tijuca.',
    sob, [crumbs_ld('/renata-estrella/', 'A Renata'), PERSON, {'@type': 'ProfilePage', 'url': BASE + '/renata-estrella/', 'mainEntity': {'@id': BASE + '/renata-estrella/#pessoa'}}])

# ------------------------------------------------------------------ FAQ
fq = f'''<div class="ph">{crumbs('Perguntas frequentes')}<h1><span class="m-mute">Perguntas frequentes.</span><span>Prazos, pedido mínimo, retirada, pagamento e eventos da Renata Estrella Pâtisserie.</span></h1></div>
<section class="sec"><h2>Antes de encomendar</h2><div class="sec__b">{faq_html(faqs)}</div></section>
''' + REL(R_MEN, R_CAS, R_CON)
pages['/perguntas-frequentes/'] = shell('/perguntas-frequentes/', 'Perguntas frequentes sobre encomendas | Renata Estrella Pâtisserie',
    'Prazos, pedido mínimo de 20 unidades, retirada na Barra da Tijuca, pagamento por Pix, casamentos, eventos e restrições alimentares na Renata Estrella Pâtisserie.',
    fq, [crumbs_ld('/perguntas-frequentes/', 'Perguntas frequentes'), faq_ld(faqs)])

# ------------------------------------------------------------------ CONTATO
con = f'''<div class="ph">{crumbs('Contato')}<h1><span class="m-mute">Contato.</span><span>Fale com a Renata Estrella pelo WhatsApp (21) 99982-1270. Ateliê na Barra da Tijuca, Rio de Janeiro.</span></h1></div>
<section class="sec" aria-labelledby="ct"><h2 id="ct">Como pedir</h2><div class="sec__b"><p><a class="btn" style="color:var(--paper)" href="{WA}" {EXT}>Pedir orçamento no WhatsApp</a></p><p>Para eventos, envie a data, o local, o número de convidados e a sua ideia. Para encomendas do <a href="/cardapio/">cardápio</a>, informe nome, telefone, data e horário da retirada, o pedido e se a retirada será pessoal ou por Uber.</p><h3>Contato</h3><ul><li>WhatsApp e telefone: <a href="tel:+5521999821270">(21) 99982-1270</a></li><li>E-mail: <a href="mailto:{EMAIL}">{EMAIL}</a></li><li>Instagram: <a href="{IG}" {EXT}>@renataestrella.patisserie</a></li><li>Ateliê: Barra da Tijuca, Rio de Janeiro, RJ (retirada com horário marcado)</li></ul></div></section>
''' + REL(R_FAQ, R_CAS, R_EVT)
pages['/contato/'] = shell('/contato/', 'Contato e encomendas | Renata Estrella Pâtisserie, Rio de Janeiro',
    'Fale com a Renata Estrella pelo WhatsApp (21) 99982-1270 e peça um orçamento de bolo, mesa de doces ou encomenda. Ateliê na Barra da Tijuca, Rio de Janeiro.',
    con, [crumbs_ld('/contato/', 'Contato'), {'@type': 'ContactPage', 'url': BASE + '/contato/', 'about': {'@id': BASE + '/#negocio'}}])

# ------------------------------------------------------------------ WRITE
for path, html in pages.items():
    d = '.' + path
    os.makedirs(d, exist_ok=True)
    open(d + 'index.html', 'w', encoding='utf8').write(html)

nf = shell('/404', 'Página não encontrada | Renata Estrella Pâtisserie', 'Esta página não existe. Veja o cardápio e os trabalhos de Renata Estrella.',
    f'<div class="ph"><h1><span class="m-mute">Esta página não existe.</span><span>Volte para o <a href="/">início</a> ou veja o <a href="/cardapio/">cardápio</a>.</span></h1></div>')
nf = nf.replace('content="index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1"', 'content="noindex"').replace(f'<link rel="canonical" href="{BASE}/404">\n', '').replace(f'<link rel="alternate" hreflang="pt-BR" href="{BASE}/404">\n', '')
open('404.html', 'w', encoding='utf8').write(nf)

open('sitemap.xml', 'w', encoding='utf8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{BASE}{p}</loc><lastmod>{LASTMOD}</lastmod></url>\n' for p in pages) + '</urlset>\n')
open('robots.txt', 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n')
open('llms.txt', 'w', encoding='utf8').write(f'''# Renata Estrella Pâtisserie

> Confeitaria artesanal sob encomenda da chef Renata Estrella, com ateliê na Barra da Tijuca, Rio de Janeiro, Brasil. Bolos, mesas de doces, brigadeiros belgas, macarons e sobremesas para casamentos, festas e eventos corporativos.

- Formação: Le Cordon Bleu, Ferrandi e École Ritz Escoffier
- Contato: WhatsApp (21) 99982-1270, {EMAIL}, Instagram @renataestrella.patisserie
- Encomendas: mínimo de 20 unidades por sabor de doce, 3 dias úteis de antecedência, retirada no ateliê, pagamento por Pix ou depósito
- Eventos: casamentos de 6 a 12 meses antes; festas e eventos corporativos com pelo menos 60 dias

## Páginas

- [Cardápio]({BASE}/cardapio/): brigadeiros belgas, doces finos, macarons, brownies, bolos, sobremesas, quiches
- [Casamentos]({BASE}/bolo-de-casamento-rio-de-janeiro/): bolo e mesa de doces para casamento no Rio de Janeiro
- [Eventos]({BASE}/doces-para-eventos-rio-de-janeiro/): doces para festas e eventos corporativos
- [Cardápio de Natal]({BASE}/cardapio-de-natal/): sobremesas e presentes de Natal com preços
- [Trabalhos]({BASE}/trabalhos/): Casa Tua, Carol Bassi, Dassa Danna e outros
- [A Renata]({BASE}/renata-estrella/): história e formação da chef
- [Perguntas frequentes]({BASE}/perguntas-frequentes/): prazos, retirada, pagamento e restrições alimentares
- [Contato]({BASE}/contato/): como fazer uma encomenda
''')
REDIRECTS = [('/casamentos', '/bolo-de-casamento-rio-de-janeiro/'), ('/eventos-corporativos', '/doces-para-eventos-rio-de-janeiro/'), ('/celebracoes-privadas', '/doces-para-eventos-rio-de-janeiro/'), ('/sobre', '/renata-estrella/'), ('/galeria', '/trabalhos/')]
json.dump({'trailingSlash': True, 'redirects': [{'source': s + suf, 'destination': d, 'permanent': True} for s, d in REDIRECTS for suf in ('', '/')], 'headers': [
    {'source': '/assets/(.*)', 'headers': [{'key': 'Cache-Control', 'value': 'public, max-age=2592000'}]},
    {'source': '/(.*)', 'headers': [{'key': 'X-Content-Type-Options', 'value': 'nosniff'}, {'key': 'Referrer-Policy', 'value': 'strict-origin-when-cross-origin'}]}]},
    open('vercel.json', 'w'), indent=2)
keep = ['index.html', '404.html', 'favicon.ico', 'google282dbca09aa8dbe7.html', 'robots.txt', 'sitemap.xml', 'llms.txt', 'vercel.json', 'assets', 'assets/**'] + [p.strip('/') + '/**' for p in pages if p != '/'] + [p.strip('/') for p in pages if p != '/']
open('.vercelignore', 'w').write('*\n' + ''.join(f'!{k}\n' for k in keep))
print(len(pages), 'pages')
