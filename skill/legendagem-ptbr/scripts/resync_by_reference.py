#!/usr/bin/env python3
"""Ressincronizar: usa os tempos de uma legenda de referência (sincronia boa,
geralmente o inglês extraído do próprio vídeo) com o texto de outra legenda
(geralmente a tradução PT-BR com tempo errado, de outro lançamento).

O texto da tradução nunca muda. Cada fala recebe o tempo da(s) fala(s) da
referência que diz(em) a mesma coisa. Uso:

  python3 resync_by_reference.py REFERENCIA.srt TRADUCAO.srt SAIDA.srt [--relatorio rel.json]

A tradução pode estar em UTF-8 ou Windows-1252; a saída sai em UTF-8 (CRLF).
"""
import argparse
import json, re, statistics

def ts(s):
    h, m, r = s.split(":"); sec, ms = r.split(",")
    return int(h) * 3600000 + int(m) * 60000 + int(sec) * 1000 + int(ms)

def fmt(t):
    t = max(0, int(round(t)))
    return f"{t//3600000:02}:{t//60000%60:02}:{t//1000%60:02},{t%1000:03}"

def abrir(caminho):
    dados = open(caminho, "rb").read()
    try:
        texto = dados.decode("utf-8-sig")
    except UnicodeDecodeError:
        texto = dados.decode("cp1252")
    return texto.replace("\r\n", "\n").replace("\r", "\n")

def ler(caminho):
    blocos = re.split(r"\n\s*\n", abrir(caminho).strip())
    cues = []
    for b in blocos:
        ls = b.split("\n")
        i = next(k for k, l in enumerate(ls) if "-->" in l)
        a, z = [x.strip() for x in ls[i].split("-->")]
        cues.append({"s": ts(a), "e": ts(z[:12]), "txt": "\n".join(ls[i + 1:])})
    return cues

SDH = re.compile(r"\([^)]*\)|\[[^\]]*\]|♪|^[A-Z][A-Z .'\-]+:", re.M)
def falado(txt):
    t = re.sub(r"<[^>]+>", "", txt)
    t = SDH.sub("", t)
    return bool(re.search(r"[A-Za-z]{2,}", t))

ap = argparse.ArgumentParser(description="Ressincroniza uma tradução pelos tempos de uma legenda de referência.")
ap.add_argument("referencia"); ap.add_argument("traducao"); ap.add_argument("saida")
ap.add_argument("--relatorio", help="JSON com contagens e falas sem par")
args = ap.parse_args()
en_all, pt = ler(args.referencia), ler(args.traducao)
en = [c for c in en_all if falado(c["txt"])]

# 1) deslocamento local: para cada PT, o melhor par EN (ordem preservada) dá um offset
def offsets(desl_global):
    pares = []
    j = 0
    for p in pt:
        alvo = p["s"] + desl_global
        while j < len(en) - 1 and en[j]["s"] < alvo - 3000:
            j += 1
        cand = [c for c in en[j:j + 8] if abs(c["s"] - alvo) < 1500]
        if cand:
            c = min(cand, key=lambda c: abs(c["s"] - alvo))
            pares.append((p["s"], c["s"] - p["s"]))
    return pares

pares = offsets(830)
def desl_local(t, janela=300000):
    vs = [d for (x, d) in pares if abs(x - t) < janela]
    return statistics.median(vs) if len(vs) >= 5 else 830

for p in pt:
    d = desl_local(p["s"])
    p["d"], p["ss"], p["se"] = d, p["s"] + d, p["e"] + d

# 2) grafo de sobreposição PT<->EN (com o PT já deslocado)
def sobre(a, b):
    return min(a["se"], b["e"]) - max(a["ss"], b["s"])

liga = {}
j0 = 0
for i, p in enumerate(pt):
    while j0 < len(en) and en[j0]["e"] < p["ss"] - 2000:
        j0 += 1
    for j in range(j0, min(j0 + 12, len(en))):
        c = en[j]
        ov = sobre(p, c)
        menor = min(p["se"] - p["ss"], c["e"] - c["s"])
        if ov > 0 and ov >= 0.3 * menor:
            liga.setdefault(i, []).append(j)

# componentes conexos
pai = {}
def acha(x):
    while pai.setdefault(x, x) != x:
        pai[x] = pai[pai[x]]; x = pai[x]
    return x
for i, js in liga.items():
    for j in js:
        pai[acha(("p", i))] = acha(("e", j))
grupos = {}
for i in liga:
    grupos.setdefault(acha(("p", i)), {"p": set(), "e": set()})["p"].add(i)
for i, js in liga.items():
    for j in js:
        grupos[acha(("p", i))]["e"].add(j)

tipos = {"1:1": 0, "1:N (PT juntou falas EN)": 0, "N:1 (PT dividiu fala EN)": 0, "N:M": 0, "sem par (só deslocado)": 0}
novo = [None] * len(pt)
for g in grupos.values():
    ps, es = sorted(g["p"]), sorted(g["e"])
    S, E = en[es[0]]["s"], max(en[j]["e"] for j in es)
    if len(ps) == 1:
        novo[ps[0]] = (S, E)
        tipos["1:1" if len(es) == 1 else "1:N (PT juntou falas EN)"] += 1
        continue
    tipos["N:1 (PT dividiu fala EN)" if len(es) == 1 else "N:M"] += len(ps)
    # bordas EN disponíveis para encaixar as bordas internas do PT
    bordas = sorted({en[j]["s"] for j in es} | {en[j]["e"] for j in es})
    PS, PE = pt[ps[0]]["ss"], pt[ps[-1]]["se"]
    escala = (E - S) / max(1, PE - PS)
    mapa = lambda t: S + (t - PS) * escala
    for k, i in enumerate(ps):
        a = S if k == 0 else mapa(pt[i]["ss"])
        z = E if k == len(ps) - 1 else mapa(pt[i]["se"])
        if 0 < k:
            b = min(bordas, key=lambda x: abs(x - a))
            if abs(b - a) < 400: a = b
        if k < len(ps) - 1:
            b = min(bordas, key=lambda x: abs(x - z))
            if abs(b - z) < 400: z = b
        novo[i] = (a, z)

for i, p in enumerate(pt):
    if novo[i] is None:
        novo[i] = (p["ss"], p["se"])
        tipos["sem par (só deslocado)"] += 1

# 3) limpeza: sem sobreposição, sem duração ridícula
for i in range(len(novo)):
    a, z = novo[i]
    if z - a < 500: z = a + 500
    novo[i] = [a, z]
for i in range(len(novo) - 1):
    if novo[i][1] > novo[i + 1][0] - 1:
        if novo[i][0] < novo[i + 1][0] - 300:
            novo[i][1] = novo[i + 1][0] - 1
        else:
            novo[i + 1][0] = novo[i][1] + 1
            novo[i + 1][1] = max(novo[i + 1][1], novo[i + 1][0] + 300)

with open(args.saida, "w", encoding="utf-8", newline="\r\n") as f:
    for k, (p, (a, z)) in enumerate(zip(pt, novo), 1):
        f.write(f"{k}\n{fmt(a)} --> {fmt(z)}\n{p['txt']}\n\n")

semPar = [(fmt(p["s"]), p["txt"].replace("\n", " ")) for i, p in enumerate(pt) if i not in liga]
desl = [p["d"] for p in pt]
rel = {"en_total": len(en_all), "en_falado": len(en), "pt": len(pt), "tipos": tipos,
           "desl_min": min(desl), "desl_max": max(desl), "sem_par": semPar}
if args.relatorio:
    json.dump(rel, open(args.relatorio, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(tipos, ensure_ascii=False), "desl", min(desl), max(desl))
