# 須以而重集 · Juvenilia

**A collection of poems, fragments, and prose written between the ages of 9 and 16, typeset vertically in the style of Republican-era (民國) letterpress books.**

![License](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)

---

## Basic Information

- **Author**: **Jie Song**
- **Western name**: **Alexandra Chieh Sloan Sung**
- **Courtesy name & sobriquet (字 / 號)**: 字：**行之**；號：**生白無一人**
- **Collection name**: **須以而重集** *Juvenilia*
- **Writing age range**: **9–16**
- **Edition**: 二〇二六年修訂版 — 11 pieces in five volumes (卷一–卷五), arranged by theme rather than by date; includes three recovered pieces from 《知見集》 and 《金銀燈花錄》

---

## Files

| File | What it is |
|---|---|
| `poems.md` | The text of the collection — edit this to change the book |
| `style.css` | Page design (A5, vertical, Minguo letterpress style) |
| `build.py` | Turns `poems.md` + `style.css` into a PDF |
| `fonts/` | 朱雀仿宋 Zhuque Fangsong (body) and a small 霞鶩文楷 LXGW WenKai TC subset (fallback glyphs, seal); both SIL OFL 1.1 |

### Text conventions in `poems.md`

- `# 卷` starts a new volume (numbered automatically)
- `## 題目` starts a poem; `## *` is an untitled poem
- `——出處` as the last line of a poem prints its source in small type at the end
- `字{注音}` puts a phonetic annotation beside a character, e.g. `乾{ㄑㄧㄢˊ}`

### Building

```
pip install playwright
python -m playwright install chromium
python build.py            # digital edition (paper-tone background) → dist/book.pdf
python build.py --print    # print edition (white background)       → dist/book-print.pdf
```

---

## License

This collection is released under **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)**.

- Please refer to: `LICENSE`
- Human-readable summary: https://creativecommons.org/licenses/by-nc-nd/4.0/

Fonts in `fonts/` are under the SIL Open Font License 1.1 (see the `*-OFL.txt` files).

---

## Citation

When citing this collection, please include (as applicable):

- Title (or filename)
- Date (if available)
- Collection name: **Juvenilia**
- Repository URL: `https://github.com/kq7m3x/xu-yi-er-zhong-ji-juvenilia`
- [DOI: 10.5281/zenodo.21618038](https://doi.org/10.5281/zenodo.21618038)

---

## Contact

- Email: alexandra.sung@protonmail.com
- Website/GitHub: https://github.com/kq7m3x
