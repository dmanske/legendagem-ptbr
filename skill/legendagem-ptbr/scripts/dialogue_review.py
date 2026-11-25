#!/usr/bin/env python3
"""Apoio à revisão de diálogo: juntar, conferir gênero e ler lado a lado.

  dialogue_review.py juntar entrada.srt saida.srt [--nomes Ana,Pescadora]
  dialogue_review.py genero legenda.srt --aux sdh.srt --aux frances.srt
  dialogue_review.py lado-a-lado legenda.srt original.srt

Os resultados são candidatos: quem fala, o sentido e a cena são conferidos por quem
revisa. Regras em references/approved-dialogue-review-rules.md. Não usar em música.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_srt import read_subtitle, seconds  # noqa: E402

FRACAS = set(
    "a o as os um uma de do da dos das e que em no na nos nas com por pelo pela pra "
    "para pro à ao seu sua meu minha não se me te eu ele ela você é foi está são ser "
    "mais tão muito muita este esta esse essa aquele aquela algum alguma algumas ou nem "
    "mas toda todo sem só até já nunca vai vou quem quando onde tem pode".split()
)
ABRE = set("e ou mas que para pra porque se quando antes onde até desde".split())
GENERO = re.compile(
    r"\b(?:obrigad|sozinh|bêbad|animad|ousad|cansad|convidad|ocupad|preocupad|"
    r"intrigad|angustiad|feit|vist|ouvid|casad|pront|perdid|amig|parceir|menin|"
    r"velh|prim|vizinh|noiv|outr|tod|algum|el|del|nel|quant|ambos|ambas|mesm)"
    r"[oae]?s?\b|\w+-l[oa]s?\b|\b(?:dois|duas)\b",
    re.IGNORECASE,
)


def ler(caminho):
    """Lista de (início, fim, linhas), tempos em segundos."""
    cues = []
    for bloco in re.split(r"\n\s*\n", read_subtitle(Path(caminho)).strip()):
        linhas = bloco.splitlines()
        pos = next((i for i, l in enumerate(linhas) if "-->" in l), None)
        if pos is None or pos + 1 >= len(linhas):
            continue
        ini, fim = (p.strip().split()[0] for p in linhas[pos].split("-->"))
        texto = [re.sub(r"<[^>]+>", "", l).strip() for l in linhas[pos + 1:]]
        cues.append((seconds(ini), seconds(fim), [l for l in texto if l]))
    return cues


def marca(t):
    ms = round(t * 1000)
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


def quebrar(texto, largura=42):
    """Melhor quebra em até duas linhas; None se não houver quebra aceitável."""
    if len(texto) <= largura:
        return [texto]
    palavras = texto.split()
    melhor = None
    for k in range(1, len(palavras)):
        a, b = " ".join(palavras[:k]), " ".join(palavras[k:])
        if max(len(a), len(b)) > largura or palavras[k - 1].lower() in FRACAS:
            continue
        custo = abs(len(a) - len(b)) * 0.8
        custo -= 26 if a[-1] in ".!?" else 18 if a[-1] in ",:…" else 0
        custo -= 14 if palavras[k].lower() in ABRE else 0
        if melhor is None or custo < melhor[0]:
            melhor = (custo, [a, b])
    return melhor[1] if melhor else None


def cps(ini, fim, texto):
    return len(texto) / max(fim - ini, 0.001)


def juntar(cues, nomes=(), intervalo=0.15, maximo=7.0, limite=17.0):
    """Une pares de cues da mesma frase quando um deles está rápido demais."""
    saida, feitas, i = [], [], 0
    while i < len(cues):
        if i + 1 < len(cues):
            (a0, a1, al), (b0, b1, bl) = cues[i], cues[i + 1]
            ta, tb = " ".join(al), " ".join(bl)
            pico = max(cps(a0, a1, ta), cps(b0, b1, tb))
            duplo = ta.startswith("-") or tb.startswith("-")
            if (ta and tb and not duplo and ta[-1] not in '.!?:…"'
                    and 0 <= b0 - a1 < intervalo and b1 - a0 <= maximo and pico > limite):
                if tb.split()[0].strip(",.!?") not in nomes:
                    tb = tb[0].lower() + tb[1:]
                texto = f"{ta} {tb}"
                linhas = quebrar(texto)
                if linhas and cps(a0, b1, texto) < pico:
                    saida.append((a0, b1, linhas))
                    feitas.append((a0, linhas))
                    i += 2
                    continue
        saida.append(cues[i])
        i += 1
    return saida, feitas


def no_tempo(cues, ini, fim):
    """Texto dos cues auxiliares que coincidem com o intervalo."""
    return " ".join(
        " ".join(l) for a, b, l in cues
        if min(b, fim) - max(a, ini) > (fim - ini) * 0.35 or ini <= (a + b) / 2 <= fim
    )


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="modo", required=True)
    j = sub.add_parser("juntar")
    j.add_argument("entrada")
    j.add_argument("saida")
    j.add_argument("--nomes", default="", help="palavras que mantêm a maiúscula, separadas por vírgula")
    g = sub.add_parser("genero")
    g.add_argument("legenda")
    g.add_argument("--aux", action="append", required=True)
    l = sub.add_parser("lado-a-lado")
    l.add_argument("legenda")
    l.add_argument("original")
    args = p.parse_args()

    if args.modo == "juntar":
        if Path(args.saida).exists():
            p.error(f"{args.saida} já existe; escolha outro nome")
        cues, feitas = juntar(ler(args.entrada), set(filter(None, args.nomes.split(","))))
        Path(args.saida).write_text(
            "\n\n".join(f"{n}\n{marca(a)} --> {marca(b)}\n" + "\n".join(t)
                        for n, (a, b, t) in enumerate(cues, 1)) + "\n", encoding="utf-8")
        for a, t in feitas:
            print(marca(a)[:8], " / ".join(t))
        print(f"{len(feitas)} junções, {len(cues)} cues")
        return 0

    legenda = ler(args.legenda)
    fontes = [ler(x) for x in (args.aux if args.modo == "genero" else [args.original])]
    total = 0
    for n, (a, b, t) in enumerate(legenda, 1):
        texto = " / ".join(t)
        if args.modo == "genero" and not GENERO.search(texto):
            continue
        total += 1
        print(n, marca(a)[:8], "|", texto, "|", " | ".join(no_tempo(f, a, b) for f in fontes))
    print(f"{total} de {len(legenda)} falas listadas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
