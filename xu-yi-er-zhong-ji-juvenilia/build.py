"""須以而重集 排版腳本：poems.md → book.html → PDF。

用法： python build.py            （數位版，米黃紙底）
      python build.py --print    （印刷版，白底）
"""
import sys
import html
import re
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "dist"
LINES_FIRST = 8   # 有題目的那一頁最多幾行
LINES_MORE = 10   # 續頁最多幾行
CN = "〇一二三四五六七八九"


def cn_num(n):
    """數字轉漢字：12 -> 一二 -> 十二"""
    if n <= 10:
        return "十" if n == 10 else CN[n]
    if n < 20:
        return "十" + (CN[n % 10] if n % 10 else "")
    if n < 100:
        return CN[n // 10] + "十" + (CN[n % 10] if n % 10 else "")
    return "".join(CN[int(d)] for d in str(n))


def parse(path):
    meta, sections, cur, poem = {}, [], None, None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if line.startswith("@"):
            k, _, v = line[1:].partition(" ")
            meta[k] = v.strip()
        elif line.startswith("## "):
            poem = {"title": line[3:].strip(), "lines": []}
            cur["poems"].append(poem)
        elif line.startswith("# "):
            cur = {"name": line[2:].strip(), "poems": [], "text": []}
            sections.append(cur)
            poem = None
        elif line.strip():
            (poem["lines"] if poem else cur["text"]).append(line)
    return meta, sections


def esc(s):
    return html.escape(s)


def ruby(s):
    """乾{qián} -> 旁注小字"""
    return re.sub(r"(.)\{([^}]+)\}", r"<ruby>\1<rt>\2</rt></ruby>", s)


def seal(chars, cls="seal"):
    # 印文由右至左讀：右欄第一字
    a, b = chars
    return f'<div class="{cls}"><span>{esc(b)}</span><span>{esc(a)}</span></div>'


def build(print_mode=False):
    meta, sections = parse(ROOT / "poems.md")
    pre = next((s for s in sections if s["name"] == "序"), None)
    post = next((s for s in sections if s["name"] == "跋"), None)
    vols = [s for s in sections if s["name"] not in ("序", "跋")]
    title = meta["書名"]

    pages = []  # (kind, html, numbered)

    # 書名頁
    pages.append(("title", f'''
<div class="frame"></div>
<div class="tp v">
  <div class="tp-sub">{esc(meta["寫作年齡"])}</div>
  <div class="tp-title">{esc(title)}</div>
  <div class="tp-latin">{esc(meta.get("副題", ""))}</div>
  <div class="tp-author">{esc(meta["作者"])}　著<br><small>{esc(meta["字號"])}</small></div>
</div>{seal("行之", "seal tp-seal")}''', False))

    if pre:
        body = "".join(f"<p>{esc(t)}</p>" for t in pre["text"])
        pages.append(("prose", f'<div class="frame"></div><div class="text v"><h2>序</h2>{body}</div>', False))

    # 先排正文，記下頁碼供目次用
    body_pages, toc = [], []
    n = 0
    for vi, vol in enumerate(vols, 1):
        n += 1
        label = f"卷{cn_num(vi)}"
        body_pages.append(("vol", f'<div class="frame"></div><div class="vol v"><div class="vol-name">{label}</div></div>', n, label))
        toc.append(("vol", label, n))
        for poem in vol["poems"]:
            t = "" if poem["title"] == "*" else poem["title"]
            ls = [l for l in poem["lines"] if not l.startswith("——")]
            src = next((l for l in poem["lines"] if l.startswith("——")), "")
            chunks = [ls[:LINES_FIRST]]
            rest = ls[LINES_FIRST:]
            while rest:
                chunks.append(rest[:LINES_MORE])
                rest = rest[LINES_MORE:]
            toc.append(("poem", t or "（無題）", n + 1))
            for ci, ch in enumerate(chunks):
                n += 1
                lines = "".join(f"<p>{ruby(esc(l)).replace('　', '<span class=sp></span>')}</p>" for l in ch)
                if src and ci == len(chunks) - 1:
                    lines += f'<p class="src">{esc(src)}</p>'
                head = f'<h3>{esc(t)}</h3>' if ci == 0 and t else ('<h3 class="blank"></h3>' if ci == 0 else "")
                body_pages.append(("poem", f'<div class="frame"></div><div class="poem v">{head}{lines}</div>', n, label))

    if post:
        n += 1
        lines = "".join(f"<p>{esc(t)}</p>" for t in post["text"][:-1])
        attr = esc(post["text"][-1]) if post["text"] else ""
        body_pages.append(("coda", f'<div class="frame"></div><div class="coda v">{lines}<p class="attr">{attr}</p></div>', n, ""))

    # 目次
    per_page = 11  # 每頁目次最多幾行
    for start in range(0, len(toc), per_page):
        rows = "".join(
            f'<div class="toc-row r-{k}"><span class="toc-t">{esc(t)}</span><span class="toc-dots">{"・" * 60}</span><span class="toc-n">{cn_num(p)}</span></div>'
            for k, t, p in toc[start:start + per_page])
        h = "<h2>目次</h2>" if start == 0 else '<h2 class="cont"></h2>'
        pages.append(("toc", f'<div class="frame"></div><div class="toc v">{h}{rows}</div>', False))

    for kind, h, num, vol in body_pages:
        pages.append((kind, h + f'<div class="folio">{cn_num(num)}</div><div class="rh">{esc(title)}{"　" + esc(vol) if vol else ""}</div>', True))

    # 版權頁
    rows = [("著作者", meta.get("著作者", meta["作者"])), ("字號", meta["字號"]), ("西文名", meta.get("英文名", "")),
            ("寫作", meta["寫作年齡"].replace("寫作年齡", "")), ("版次", meta["版本"]),
            ("授權", meta["授權"]), ("DOI", meta["DOI"])]
    cells = "".join(f'<div class="cp-col"><span class="cp-k">{esc(k)}</span><span class="cp-v">{esc(v)}</span></div>' for k, v in rows if v)
    pages.append(("colophon", f'''
<div class="cp">
  <div class="cp-stamp">{seal("行之", "seal cp-seal")}<div class="cp-stamp-l">著者印</div></div>
  <div class="cp-box v"><div class="cp-head">{esc(title)}</div>{cells}<div class="cp-col cp-note">本書可自由轉載分享，惟須署名、不得商用、不得改作。</div></div>
</div>''', False))

    css = (ROOT / "style.css").read_text(encoding="utf-8")
    body = "\n".join(f'<section class="page k-{k}">{h}</section>' for k, h, _ in pages)
    doc = f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><title>{esc(title)}</title>
<style>{css}</style></head><body class="{'print' if print_mode else 'digital'}">{body}</body></html>'''
    OUT.mkdir(exist_ok=True)
    name = "book-print" if print_mode else "book"
    (OUT / f"{name}.html").write_text(doc, encoding="utf-8")

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto((OUT / f"{name}.html").resolve().as_uri())
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(300)
        pg.pdf(path=str(OUT / f"{name}.pdf"), prefer_css_page_size=True, print_background=True)
        b.close()
    print("ok", OUT / f"{name}.pdf", len(pages), "pages")


if __name__ == "__main__":
    build("--print" in sys.argv)
