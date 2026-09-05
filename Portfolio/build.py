# -*- coding: utf-8 -*-
"""p*.md 를 순서대로 이어 붙여 인쇄용 portfolio.html 을 만든다.
사용: python build.py   (같은 폴더에서)
"""
import glob, html, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))

CSS = """
@page { size: A4; margin: 13mm 14mm 18mm 14mm; }
* { box-sizing: border-box; }
body {
  font-family: 'Malgun Gothic', '맑은 고딕', 'Apple SD Gothic Neo', sans-serif;
  font-size: 9.8pt; line-height: 1.5; color: #1a1a1a;
  margin: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
h1 {
  font-size: 15pt; line-height: 1.2; margin: 0 0 3mm 0; padding-bottom: 2mm;
  border-bottom: 2px solid #8c4a2f; break-before: page;
}
h1:first-of-type { break-before: auto; }
h2 { font-size: 11.5pt; margin: 5.5mm 0 2.2mm 0; color: #8c4a2f; break-after: avoid; }
h3 { font-size: 10.2pt; margin: 5mm 0 1.8mm 0; break-after: avoid; }
p { margin: 0 0 2.6mm 0; }
strong { font-weight: 700; }
hr { border: 0; border-top: 1px solid #ddd; margin: 5mm 0; }
ul { margin: 0 0 3.4mm 0; padding-left: 5.5mm; }
li { margin-bottom: 1.8mm; }
blockquote {
  margin: 3.4mm 0; padding: 2.5mm 3.5mm; border-left: 3px solid #8c4a2f;
  background: #faf8f6; break-inside: avoid;
}
blockquote p:last-child { margin-bottom: 0; }
code {
  font-family: Consolas, 'D2Coding', monospace; font-size: 9.2pt;
  background: #f2f1ef; padding: 0.3mm 1mm; border-radius: 2px;
}
pre {
  background: #f7f6f4; border: 1px solid #e2e0dc; border-radius: 3px;
  padding: 3mm; margin: 3mm 0; overflow: hidden; break-inside: avoid;
}
pre code { background: none; padding: 0; font-size: 8.6pt; line-height: 1.45; white-space: pre; }
table {
  width: 100%; border-collapse: collapse; margin: 3.6mm 0;
  font-size: 8.7pt; break-inside: avoid;
}
th, td { border: 1px solid #dcdad6; padding: 1.1mm 1.8mm; text-align: left; vertical-align: top; }
th { background: #f2f0ed; font-weight: 700; }
figure { margin: 2.5mm 0; break-inside: avoid; text-align: center; }
figure img { max-width: 72%; border: 1px solid #d8d5d0; }
figcaption { font-size: 8.6pt; color: #666; margin-top: 1.5mm; }
td img { max-width: 82%; border: 1px solid #d8d5d0; display: block; }
"""

CODE_RE = re.compile(r'`([^`]+)`')
IMG_RE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
BOLD_RE = re.compile(r'\*\*([^*]+)\*\*')
EM_RE = re.compile(r'(?<!\*)\*([^*]+)\*(?!\*)')
SEP_RE = re.compile(r'^\|[\s:\-|]+\|$')


def inline(text):
    text = html.escape(text).replace('&lt;br&gt;', '<br>')
    stash = []

    def keep(s):
        stash.append(s)
        return '\x00%d\x00' % (len(stash) - 1)

    text = IMG_RE.sub(lambda m: keep('<img src="%s" alt="%s">' % (m.group(2), m.group(1))), text)
    text = CODE_RE.sub(lambda m: keep('<code>%s</code>' % m.group(1)), text)
    text = BOLD_RE.sub(r'<strong>\1</strong>', text)
    text = EM_RE.sub(r'<em>\1</em>', text)
    text = LINK_RE.sub(r'\1', text)
    for i, s in enumerate(stash):
        text = text.replace('\x00%d\x00' % i, s)
    return text


def cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def convert(md):
    out, i = [], 0
    lines = md.split('\n')
    n = len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()

        if s.startswith('```'):
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith('```'):
                buf.append(html.escape(lines[i]))
                i += 1
            i += 1
            out.append('<pre><code>%s</code></pre>' % '\n'.join(buf))
            continue

        if not s:
            i += 1
            continue

        if s.startswith('#'):
            lvl = len(s) - len(s.lstrip('#'))
            out.append('<h%d>%s</h%d>' % (lvl, inline(s[lvl:].strip()), lvl))
            i += 1
            continue

        if s in ('---', '***', '___'):
            out.append('<hr>')
            i += 1
            continue

        if s.startswith('|'):
            rows = []
            while i < n and lines[i].strip().startswith('|'):
                rows.append(lines[i].strip())
                i += 1
            head, body = None, rows
            if len(rows) >= 2 and SEP_RE.match(rows[1]):
                head, body = rows[0], rows[2:]
            out.append('<table>')
            if head is not None and any(c for c in cells(head)):
                out.append('<tr>' + ''.join('<th>%s</th>' % inline(c) for c in cells(head)) + '</tr>')
            for r in body:
                out.append('<tr>' + ''.join('<td>%s</td>' % inline(c) for c in cells(r)) + '</tr>')
            out.append('</table>')
            continue

        if s.startswith('> '):
            buf = []
            while i < n and lines[i].strip().startswith('>'):
                buf.append(lines[i].strip()[1:].lstrip())
                i += 1
            out.append('<blockquote>%s</blockquote>' % convert('\n'.join(buf)))
            continue

        if s.startswith('- '):
            buf = []
            while i < n and lines[i].strip().startswith('- '):
                item = lines[i].strip()[2:]
                i += 1
                while i < n and lines[i].strip() and not lines[i].strip().startswith(('- ', '|', '#', '>', '```')) \
                        and lines[i].startswith((' ', '\t')):
                    item += ' ' + lines[i].strip()
                    i += 1
                buf.append('<li>%s</li>' % inline(item))
            out.append('<ul>%s</ul>' % ''.join(buf))
            continue

        m = IMG_RE.fullmatch(s)
        if m:
            out.append('<figure><img src="%s" alt="%s">%s</figure>' % (
                m.group(2), html.escape(m.group(1)),
                '<figcaption>%s</figcaption>' % html.escape(m.group(1)) if m.group(1) else ''))
            i += 1
            continue

        buf = [s]
        i += 1
        while i < n and lines[i].strip() and not lines[i].strip().startswith(('#', '|', '>', '- ', '```', '---')):
            buf.append(lines[i].strip())
            i += 1
        out.append('<p>%s</p>' % inline(' '.join(buf)))

    return '\n'.join(out)


def main():
    files = sorted(glob.glob(os.path.join(HERE, 'p*.md')))
    if not files:
        print('p*.md 를 못 찾았다'); return 1
    body = []
    for f in files:
        with open(f, encoding='utf-8') as fh:
            body.append(convert(fh.read()))
        print('  +', os.path.basename(f))
    # 쪽 나눔은 CSS 의 h1 { break-before: page } 가 한다.
    # 별도 분리자 div 를 쓰면 내용이 쪽 끝에 딱 맞을 때 빈 쪽이 하나 더 생긴다.
    full = '\n'.join(body)
    # h1 바로 앞의 <hr> 은 지운다. h1 이 새 쪽을 열므로 선은 앞 쪽에 홀로 남아
    # 빈 쪽처럼 보이는 페이지를 만든다.
    full = re.sub(r'<hr>\s*(?=<h1>)', '', full)
    doc = ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
           '<title>Portfolio</title><style>%s</style></head><body>\n%s\n</body></html>'
           % (CSS, full))
    out = os.path.join(HERE, 'portfolio.html')
    with open(out, 'w', encoding='utf-8') as fh:
        fh.write(doc)
    print('->', out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
